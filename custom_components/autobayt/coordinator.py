"""Autobayt coordinator for managing API communication."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict, List

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import discovery_flow

from .const import (
    CONF_USER_ID,
    DEFAULT_SCAN_INTERVAL,
    DEVICE_DETAIL_URL,
    DEVICE_TYPES,
    DOMAIN,
    USER_DEVICE_LIST_URL,
)

_LOGGER = logging.getLogger(__name__)


class AutobaytCoordinator(DataUpdateCoordinator):
    """Autobayt data coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.user_id = entry.data.get(CONF_USER_ID)
        self.device_id = entry.data.get("device_id")
        self._session: aiohttp.ClientSession | None = None
        self._discovered_devices: Dict[str, Dict[str, Any]] = {}
        self._added_devices: set[str] = set()
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Fetch data from Autobayt API."""
        if not self._session:
            self._session = aiohttp.ClientSession()
        
        try:
            device_data = {}
            
            # For device-specific coordinator, fetch device details using Device GET API
            if self.device_id:
                device = await self._fetch_device_details(self.device_id)
                if device:
                    device_data[self.device_id] = device
                return {"device_data": device_data}
            
            # For main coordinator with user_id
            if self.user_id:
                user_devices = await self._fetch_user_devices()
                
                # Fetch detailed data for each added device using Device GET API
                if user_devices:
                    for device_id in self._added_devices:
                        device = await self._fetch_device_details(device_id)
                        if device:
                            device_data[device_id] = device
                
                return {
                    "user_devices": user_devices,
                    "device_data": device_data,
                }
            
            return {"device_data": {}}
            
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Autobayt API: {err}") from err

    async def _fetch_user_devices(self) -> List[Dict[str, Any]]:
        """Fetch all devices for the user."""
        if not self.user_id:
            return []
            
        return await self._fetch_user_devices_by_id(self.user_id)

    async def _fetch_user_devices_by_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetch all devices for a specific user_id."""
        url = f"{USER_DEVICE_LIST_URL}{user_id}"
        
        try:
            async with self._session.get(url, timeout=30) as response:
                response.raise_for_status()
                data = await response.json()
                return data if isinstance(data, list) else []
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching user devices: %s", err)
            return []

    async def _fetch_device_details(self, device_id: str) -> Dict[str, Any] | None:
        """Fetch detailed information for a specific device."""
        url = f"{DEVICE_DETAIL_URL}{device_id}"
        
        try:
            async with self._session.get(url, timeout=30) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("API response for device %s: %s", device_id, data)
                # API returns a single device object
                if isinstance(data, dict):
                    _LOGGER.debug("Returning dict device data for %s", device_id)
                    return data
                _LOGGER.warning("Unexpected data type for device %s: %s", device_id, type(data))
                return None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching device details for %s: %s", device_id, err)
            return None

    async def async_start_discovery(self) -> None:
        """Start the device discovery process."""
        await self._async_discover_devices()

    async def _async_discover_devices(self) -> None:
        """Discover new devices and create discovery flows."""
        if not self.data or "user_devices" not in self.data:
            return

        user_devices = self.data["user_devices"]
        
        for device in user_devices:
            device_id = device.get("device_id")
            if not device_id:
                continue
                
            if device_id in self._discovered_devices:
                continue
                
            self._discovered_devices[device_id] = device
            
            discovery_flow.async_create_flow(
                self.hass,
                DOMAIN,
                context={"source": "discovery"},
                data={
                    "device_id": device_id,
                    "device_data": device,
                    "user_id": self.user_id,
                },
            )
            
            _LOGGER.info("Discovered Autobayt device: %s (%s)", 
                        device.get("name", "Unknown"), device_id)

    async def async_add_device(self, device_id: str) -> None:
        """Add a device to be monitored."""
        self._added_devices.add(device_id)
        await self.async_request_refresh()

    async def async_remove_device(self, device_id: str) -> None:
        """Remove a device from monitoring."""
        self._added_devices.discard(device_id)

    def reset_device_discovery(self, device_id: str) -> None:
        """Reset device discovery status to allow rediscovery."""
        self._discovered_devices.pop(device_id, None)
        _LOGGER.debug("Reset discovery for device: %s", device_id)

    def get_device_type_info(self, model_name: str) -> Dict[str, Any] | None:
        """Get device type information from model name."""
        for device_type in DEVICE_TYPES:
            if device_type["device_type_code"] == model_name:
                return device_type
        return None

    def get_discovered_device(self, device_id: str) -> Dict[str, Any] | None:
        """Get discovered device data."""
        return self._discovered_devices.get(device_id)

    async def async_shutdown(self) -> None:
        """Shutdown coordinator and cleanup resources."""
        if self._session:
            await self._session.close()
            self._session = None
