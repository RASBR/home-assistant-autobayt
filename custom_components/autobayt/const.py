"""Constants for the Autobayt integration."""
from typing import Final

DOMAIN: Final = "autobayt"

# API Configuration
USER_DEVICE_LIST_URL: Final = "https://api.autobayt.com/v1/user/get-things?user_id="
DEVICE_DETAIL_URL: Final = "https://api.autobayt.com/v1/device?device_id="
DEVICE_TRIGGER_URL: Final = "https://api.autobayt.com/v1/device/trigger"

# Device Types Configuration
DEVICE_TYPES: Final = [
    {
        "device_type_code": "SW100HV1",
        "type_info": {
            "device_type_name": "Smart Switch Single",
            "device_generation": "V1",
            "buttons": 1
        },
        "docs_url": "https://github.com/RASBR/home-assistant-autobayt/wiki/sw100hv1"
    },
    {
        "device_type_code": "SW100PMV1",
        "type_info": {
            "device_type_name": "Smart Switch Single PM",
            "device_generation": "V1",
            "buttons": 1
        },
        "docs_url": "https://github.com/RASBR/home-assistant-autobayt/wiki/sw100pmv1"
    },
    {
        "device_type_code": "SW200LV1",
        "type_info": {
            "device_type_name": "Smart Switch Double",
            "device_generation": "V1",
            "buttons": 2
        },
        "docs_url": "https://github.com/RASBR/home-assistant-autobayt/wiki/sw200lv1"
    },
    {
        "device_type_code": "SW300LV1",
        "type_info": {
            "device_type_name": "Smart Switch Triple",
            "device_generation": "V1",
            "buttons": 3
        },
        "docs_url": "https://github.com/RASBR/home-assistant-autobayt/wiki/sw300lv1"
    },
]

# Configuration Keys
CONF_USER_ID: Final = "user_id"

# Update Intervals
DEFAULT_SCAN_INTERVAL: Final = 290  # seconds

# Entity Keys
ATTR_ROOM_ID: Final = "room_id"
ATTR_CONNECTION_STATUS: Final = "connection_status"
ATTR_SLAVE_ID: Final = "slave_id"
ATTR_IS_HUB: Final = "is_hub"
ATTR_IS_UPDATING: Final = "is_updating"
ATTR_PERC: Final = "perc"
ATTR_PERIOD: Final = "period"
ATTR_PAT_PERIOD: Final = "pat_period"
ATTR_DEVICE_ID: Final = "device_id"
ATTR_NAME: Final = "name"
ATTR_FIRMWARE_VERSION: Final = "firmware_version"
ATTR_MODEL_NAME: Final = "model_name"
ATTR_SSTR: Final = "sstr"
ATTR_LOC_ID: Final = "loc_id"
ATTR_NEXT_FIRMWARE: Final = "next_firmware"
ATTR_BUTTONS: Final = "buttons"
ATTR_ROOM_NAME: Final = "room_name"

# Button Keys
BTN_SWITCH_STATE: Final = "switch_state"
BTN_DPB_STATE: Final = "dpb_state"
BTN_POWER_ON_STATE: Final = "power_on_state"
BTN_MODE: Final = "mode"
BTN_TOGGLE_DELAY: Final = "toggle_delay"
BTN_NAME: Final = "name"
BTN_BUTTON_ID: Final = "button_id"
