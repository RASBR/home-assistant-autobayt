"""Config flow for Autobayt integration."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_USER_ID,
    DEVICE_DETAIL_URL,
    DEVICE_TYPES,
    DOMAIN,
    USER_DEVICE_LIST_URL,
)

_LOGGER = logging.getLogger(__name__)

USER_SCHEMA = vol.Schema({
    vol.Required(CONF_USER_ID): cv.string,
})


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Autobayt."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovered_device: Dict[str, Any] | None = None

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            user_id = user_input[CONF_USER_ID]
            
            if len(user_id) != 24:
                errors[CONF_USER_ID] = "invalid_user_id_length"
            else:
                try:
                    devices = await self._async_get_user_devices(user_id)
                    
                    if devices is None:
                        errors["base"] = "cannot_connect"
                    elif len(devices) == 0:
                        errors["base"] = "no_devices_found"
                    else:
                        return self.async_create_entry(
                            title="Autobayt",
                            data={CONF_USER_ID: user_id},
                        )
                        
                except Exception:
                    _LOGGER.exception("Unexpected exception")
                    errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=USER_SCHEMA,
            errors=errors,
        )

    async def async_step_discovery(
        self, discovery_info: Dict[str, Any]
    ) -> FlowResult:
        """Handle discovery of a new device."""
        device_id = discovery_info["device_id"]
        device_data = discovery_info["device_data"]
        user_id = discovery_info.get("user_id")
        
        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()
        
        self._discovered_device = device_data
        
        model_name = device_data.get("model_name", "")
        device_name = device_data.get("name", f"Autobayt {model_name}")
        
        # Set context for discovery UI and store user_id
        self.context["title_placeholders"] = {
            "name": device_name,
            "model": model_name,
        }
        self.context["user_id"] = user_id
        
        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery of the device."""
        if user_input is not None:
            device_data = self._discovered_device
            device_id = device_data["device_id"]
            device_name = device_data.get("name", f"Autobayt {device_data.get('model_name', '')}")
            
            # Get user_id from discovery_info context
            user_id = self.context.get("user_id")
            
            return self.async_create_entry(
                title=device_name,
                data={
                    "device_id": device_id,
                    "device_data": device_data,
                    "user_id": user_id,  # Pass user_id to device entry
                },
            )

        if not self._discovered_device:
            return self.async_abort(reason="no_device_data")

        # Fetch latest device info from API
        device_id = self._discovered_device.get("device_id")
        if device_id:
            latest_device_data, device_exists = await self._async_get_device_info(device_id)
            if device_exists and latest_device_data:
                # Update stored device data with latest info
                self._discovered_device = latest_device_data
                _LOGGER.info("Fetched latest device info for %s", device_id)
            elif not device_exists:
                # Device was deleted, abort the flow
                _LOGGER.warning("Device %s no longer exists, aborting", device_id)
                return self.async_abort(reason="device_deleted")
            else:
                # Network error or other issue, use discovery data as fallback
                _LOGGER.warning("Could not fetch latest device info for %s, using discovery data", device_id)

        device_data = self._discovered_device
        model_name = device_data.get("model_name", "")
        device_type_info = self._get_device_type_info(model_name)
        device_name = device_data.get("name", f"Autobayt {model_name}")
        firmware_version = device_data.get("firmware_version", "Unknown")
        
        device_type_name = "Unknown"
        button_count = 1
        if device_type_info:
            device_type_name = device_type_info.get("type_info", {}).get("device_type_name", "Unknown")
            button_count = device_type_info.get("type_info", {}).get("buttons", 1)
        
        # Get connection status
        connection_status = "Online" if device_data.get("connection_status", False) else "Offline"
        
        placeholders = {
            "device_name": device_name,
            "model_name": model_name,
            "device_type": device_type_name,
            "device_id": device_data.get("device_id", ""),
            "firmware_version": firmware_version,
            "button_count": str(button_count),
            "connection_status": connection_status,
        }

        return self.async_show_form(
            step_id="discovery_confirm",
            description_placeholders=placeholders,
        )

    async def async_step_ignore(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Ignore the discovered device."""
        return self.async_create_entry(
            title="Ignored Device",
            data={},
        )

    async def _async_get_user_devices(self, user_id: str) -> list[Dict[str, Any]] | None:
        """Get devices for user ID."""
        url = f"{USER_DEVICE_LIST_URL}{user_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data if isinstance(data, list) else []
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching user devices: %s", err)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err)
            return None

    async def _async_get_device_info(self, device_id: str) -> tuple[Dict[str, Any] | None, bool]:
        """Get latest device information from API.
        
        Returns:
            Tuple of (device_data, device_exists)
            - device_data: Device information dict or None
            - device_exists: False if device was deleted (404), True otherwise
        """
        url = f"{DEVICE_DETAIL_URL}{device_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    if response.status == 404:
                        # Device not found - was deleted
                        _LOGGER.info("Device %s not found (404)", device_id)
                        return None, False
                    
                    response.raise_for_status()
                    data = await response.json()
                    
                    # Check if response is empty or null (device deleted)
                    if not data or (isinstance(data, dict) and not data):
                        _LOGGER.info("Device %s returned empty data", device_id)
                        return None, False
                    
                    return (data if isinstance(data, dict) else None), True
        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching device info for %s: %s", device_id, err)
            return None, True  # Network error, device may still exist
        except Exception as err:
            _LOGGER.error("Unexpected error fetching device info: %s", err)
            return None, True  # Unknown error, device may still exist

    def _get_device_type_info(self, model_name: str) -> Dict[str, Any] | None:
        """Get device type information from model name."""
        for device_type in DEVICE_TYPES:
            if device_type["device_type_code"] == model_name:
                return device_type
        return None

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Autobayt config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
        )
