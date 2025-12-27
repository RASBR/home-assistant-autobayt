"""Autobayt binary sensor platform."""
from __future__ import annotations

import logging
from typing import Any, Dict
from packaging import version

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_FIRMWARE_VERSION,
    ATTR_IS_HUB,
    ATTR_MODEL_NAME,
    ATTR_NEXT_FIRMWARE,
    ATTR_SLAVE_ID,
    DOMAIN,
)
from .coordinator import AutobaytCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Autobayt binary sensors."""
    coordinator: AutobaytCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities: list[BinarySensorEntity] = []
    
    # Binary sensor entities can be added here in the future
    # Firmware update is now handled by the update platform
    
    async_add_entities(entities)


class AutobaytBinarySensorEntity(CoordinatorEntity, BinarySensorEntity):
    """Base Autobayt binary sensor entity."""

    def __init__(
        self,
        coordinator: AutobaytCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{device_id}_{sensor_type}"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        model_name = device_data.get(ATTR_MODEL_NAME, "Unknown")
        firmware_version = device_data.get(ATTR_FIRMWARE_VERSION, "Unknown")
        
        info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Autobayt",
            "model": model_name,
            "sw_version": firmware_version,
            "connections": {("mac", self._device_id)},
        }
        
        # Add via_device for slave devices connected to a hub
        is_hub = device_data.get(ATTR_IS_HUB, False)
        slave_id = device_data.get(ATTR_SLAVE_ID, "")
        
        if not is_hub and slave_id:
            info["via_device"] = (DOMAIN, slave_id)
        
        return info

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data.get("device_data", {})
        )

    def _get_device_data(self) -> Dict[str, Any]:
        """Get current device data."""
        return self.coordinator.data.get("device_data", {}).get(self._device_id, {})


class AutobaytFirmwareUpdateSensor(AutobaytBinarySensorEntity):
    """Autobayt firmware update available sensor."""

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "firmware_update")
        self._attr_name = f"{device_name} Firmware Update"
        self._attr_device_class = BinarySensorDeviceClass.UPDATE
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self) -> bool:
        """Return true if firmware update is available."""
        device_data = self._get_device_data()
        current_version = device_data.get(ATTR_FIRMWARE_VERSION)
        next_firmware = device_data.get(ATTR_NEXT_FIRMWARE)
        
        if not current_version or not next_firmware:
            return False
            
        if isinstance(next_firmware, list) and len(next_firmware) > 0:
            next_version = next_firmware[0].get("version_name")
            if next_version:
                try:
                    # Compare versions using packaging.version
                    return version.parse(current_version) < version.parse(next_version)
                except Exception as e:
                    _LOGGER.warning(
                        "Error comparing versions %s and %s: %s",
                        current_version,
                        next_version,
                        e
                    )
                    return False
        
        return False

    @property
    def extra_state_attributes(self) -> Dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        next_firmware = device_data.get(ATTR_NEXT_FIRMWARE)
        
        attributes = {
            "current_version": device_data.get(ATTR_FIRMWARE_VERSION),
        }
        
        if next_firmware and isinstance(next_firmware, list) and len(next_firmware) > 0:
            firmware_info = next_firmware[0]
            attributes["available_version"] = firmware_info.get("version_name")
            attributes["firmware_file"] = firmware_info.get("file_name")
            attributes["version_code"] = firmware_info.get("version_code")
            attributes["requires_app_update"] = firmware_info.get("require_client_update", False)
        
        return attributes
