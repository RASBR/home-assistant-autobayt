"""Autobayt switch platform."""
from __future__ import annotations

import logging
from typing import Any, Dict

import aiohttp
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    DEVICE_TRIGGER_URL,
    ATTR_BUTTONS,
    BTN_SWITCH_STATE,
    BTN_BUTTON_ID,
    BTN_NAME,
)
from .coordinator import AutobaytCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Autobayt switches."""
    coordinator: AutobaytCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities: list[SwitchEntity] = []
    
    if "device_id" in config_entry.data:
        device_id = config_entry.data["device_id"]
        device_data = config_entry.data.get("device_data", {})
        device_name = device_data.get("name", "Autobayt Device")
        
        await coordinator.async_add_device(device_id)
        
        buttons = device_data.get(ATTR_BUTTONS, [])
        for button in buttons:
            button_id = button.get(BTN_BUTTON_ID, 0)
            button_name = button.get(BTN_NAME, f"Button {button_id}")
            entities.append(
                AutobaytSwitchEntity(
                    coordinator, 
                    device_id, 
                    device_name, 
                    button_id, 
                    button_name
                )
            )
    
    async_add_entities(entities)


class AutobaytSwitchEntity(CoordinatorEntity, SwitchEntity):
    """Autobayt switch entity."""

    def __init__(
        self,
        coordinator: AutobaytCoordinator,
        device_id: str,
        device_name: str,
        button_id: int,
        button_name: str,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name
        self._button_id = button_id
        self._button_name = button_name
        self._attr_unique_id = f"{device_id}_button_{button_id}"
        self._attr_name = f"{device_name} {button_name}"

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        model_name = device_data.get("model_name", "Unknown")
        firmware_version = device_data.get("firmware_version", "Unknown")
        
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

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        device_data = self.coordinator.data.get("device_data", {}).get(self._device_id, {})
        buttons = device_data.get(ATTR_BUTTONS, [])
        
        for button in buttons:
            if button.get(BTN_BUTTON_ID) == self._button_id:
                switch_state = button.get(BTN_SWITCH_STATE)
                return switch_state if isinstance(switch_state, bool) else None
        
        return None

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._async_set_switch_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._async_set_switch_state(False)

    async def _async_set_switch_state(self, state: bool) -> None:
        """Set the switch state."""
        payload = {
            "btnStates": [state],
            "btnIds": [self._button_id],
            "device_id": self._device_id
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    DEVICE_TRIGGER_URL, 
                    json=payload, 
                    headers={"Content-Type": "application/json"},
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    _LOGGER.debug(
                        "Successfully set switch state for device %s button %s to %s", 
                        self._device_id, self._button_id, state
                    )
                    
                    await self.coordinator.async_request_refresh()
                    
        except aiohttp.ClientError as err:
            _LOGGER.error(
                "Failed to set switch state for device %s button %s: %s", 
                self._device_id, self._button_id, err
            )
        except Exception as err:
            _LOGGER.error(
                "Unexpected error setting switch state for device %s button %s: %s", 
                self._device_id, self._button_id, err
            )
