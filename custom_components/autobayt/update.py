"""Update platform for Autobayt integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AutobaytCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Autobayt update entities."""
    coordinator: AutobaytCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    device_data_dict = coordinator.data.get("device_data", {})
    for device_id, device_data in device_data_dict.items():
        # Skip invalid entries
        if not device_id or not isinstance(device_data, dict):
            _LOGGER.warning("Skipping invalid device entry: %s", device_id)
            continue
            
        device_name = device_data.get("name")
        if not device_name:
            _LOGGER.warning("Skipping device with no name: %s", device_id)
            continue
            
        entities.append(AutobaytUpdateEntity(coordinator, device_id, device_name))

    async_add_entities(entities)


class AutobaytUpdateEntity(CoordinatorEntity, UpdateEntity):
    """Representation of an Autobayt device update entity."""

    _attr_has_entity_name = True
    _attr_supported_features = UpdateEntityFeature.PROGRESS

    def __init__(
        self, coordinator: AutobaytCoordinator, device_id: str, device_name: str
    ) -> None:
        """Initialize the update entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name
        self._attr_unique_id = f"{device_id}_firmware_update"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, device_id)},
        }
        self._attr_name = "Firmware"

    def _get_device_data(self) -> dict[str, Any]:
        """Get device data from coordinator."""
        return self.coordinator.data.get("device_data", {}).get(self._device_id, {})

    @property
    def installed_version(self) -> str | None:
        """Return the current installed version."""
        device_data = self._get_device_data()
        return device_data.get("firmware_version")

    @property
    def latest_version(self) -> str | None:
        """Return the latest available version."""
        device_data = self._get_device_data()
        next_firmware = device_data.get("next_firmware", [])
        
        if next_firmware and len(next_firmware) > 0:
            latest = next_firmware[0].get("version_name")
            # Only return if different from installed version
            if latest and latest != self.installed_version:
                return latest
        
        return self.installed_version

    @property
    def in_progress(self) -> bool | int:
        """Update installation progress."""
        device_data = self._get_device_data()
        is_updating = device_data.get("is_updating", False)
        
        if is_updating:
            perc = device_data.get("perc", 0)
            if perc > 0:
                return perc
            return True
        
        return False

    @property
    def title(self) -> str | None:
        """Return the title of the update."""
        device_data = self._get_device_data()
        model = device_data.get("model_name", "Autobayt Device")
        return f"{model} Firmware"

    @property
    def release_summary(self) -> str | None:
        """Return the release summary."""
        device_data = self._get_device_data()
        next_firmware = device_data.get("next_firmware", [])
        
        if next_firmware and len(next_firmware) > 0:
            firmware_info = next_firmware[0]
            file_name = firmware_info.get("file_name", "")
            return f"Firmware update available: {file_name}"
        
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._device_id in self.coordinator.data.get("device_data", {})
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        device_data = self._get_device_data()
        next_firmware = device_data.get("next_firmware", [])
        
        attrs = {}
        
        if next_firmware and len(next_firmware) > 0:
            firmware_info = next_firmware[0]
            attrs.update({
                "file_name": firmware_info.get("file_name"),
                "version_code": firmware_info.get("version_code"),
                "requires_client_update": firmware_info.get("require_client_update", False),
            })
        
        if device_data.get("is_updating"):
            attrs["update_percentage"] = device_data.get("perc", 0)
        
        return attrs if attrs else None
