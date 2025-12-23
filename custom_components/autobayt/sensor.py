"""Autobayt sensor platform."""
from __future__ import annotations

import logging
from typing import Any, Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, SIGNAL_STRENGTH_DECIBELS_MILLIWATT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_CONNECTION_STATUS,
    ATTR_FIRMWARE_VERSION,
    ATTR_IS_UPDATING,
    ATTR_MODEL_NAME,
    ATTR_NEXT_FIRMWARE,
    ATTR_ROOM_NAME,
    ATTR_SSTR,
    ATTR_BUTTONS,
    DOMAIN,
)
from .coordinator import AutobaytCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Autobayt sensors."""
    coordinator: AutobaytCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities: list[SensorEntity] = []
    
    if "device_id" in config_entry.data:
        device_id = config_entry.data["device_id"]
        device_data = config_entry.data.get("device_data", {})
        
        await coordinator.async_add_device(device_id)
        
        entities.extend(_create_device_sensors(coordinator, device_id, device_data))
    
    async_add_entities(entities)


def _create_device_sensors(
    coordinator: AutobaytCoordinator, device_id: str, device_data: Dict[str, Any]
) -> list[SensorEntity]:
    """Create sensors for Autobayt device."""
    device_name = device_data.get("name", "Autobayt Device")
    
    return [
        AutobaytConnectionSensor(coordinator, device_id, device_name),
        AutobaytSignalStrengthSensor(coordinator, device_id, device_name),
        AutobaytFirmwareSensor(coordinator, device_id, device_name),
        AutobaytUpdateStatusSensor(coordinator, device_id, device_name),
    ]


class AutobaytSensorEntity(CoordinatorEntity, SensorEntity):
    """Base Autobayt sensor entity."""

    def __init__(
        self,
        coordinator: AutobaytCoordinator,
        device_id: str,
        device_name: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
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
        
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Autobayt",
            "model": model_name,
            "sw_version": firmware_version,
            "connections": {("mac", self._device_id)},
        }

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


class AutobaytConnectionSensor(AutobaytSensorEntity):
    """Autobayt connection status sensor."""

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "connection")
        self._attr_name = f"{device_name} Connection"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["connected", "disconnected"]

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        connection_status = device_data.get(ATTR_CONNECTION_STATUS)
        
        if connection_status is True:
            return "connected"
        elif connection_status is False:
            return "disconnected"
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        return {
            "is_hub": device_data.get("is_hub"),
            "slave_id": device_data.get("slave_id"),
            "room_name": device_data.get(ATTR_ROOM_NAME),
        }


class AutobaytSignalStrengthSensor(AutobaytSensorEntity):
    """Autobayt signal strength sensor."""

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "signal_strength")
        self._attr_name = f"{device_name} Signal Strength"
        self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
        self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        sstr = device_data.get(ATTR_SSTR)
        
        if sstr is not None:
            try:
                return int(sstr)
            except (ValueError, TypeError):
                return None
        return None


class AutobaytFirmwareSensor(AutobaytSensorEntity):
    """Autobayt firmware version sensor."""

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "firmware")
        self._attr_name = f"{device_name} Firmware"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        return device_data.get(ATTR_FIRMWARE_VERSION)

    @property
    def extra_state_attributes(self) -> Dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        next_firmware = device_data.get(ATTR_NEXT_FIRMWARE)
        
        attributes = {
            "model_name": device_data.get(ATTR_MODEL_NAME),
        }
        
        if next_firmware and isinstance(next_firmware, list) and len(next_firmware) > 0:
            firmware_info = next_firmware[0]
            attributes["next_version"] = firmware_info.get("version_name")
            attributes["next_file"] = firmware_info.get("file_name")
            attributes["version_code"] = firmware_info.get("version_code")
        
        return attributes


class AutobaytUpdateStatusSensor(AutobaytSensorEntity):
    """Autobayt update status sensor."""

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name, "update_status")
        self._attr_name = f"{device_name} Update Status"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["idle", "updating"]

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        device_data = self._get_device_data()
        is_updating = device_data.get(ATTR_IS_UPDATING)
        
        if is_updating is True:
            return "updating"
        elif is_updating is False:
            return "idle"
        return None

    @property
    def extra_state_attributes(self) -> Dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        return {
            "update_percentage": device_data.get("perc"),
        }
