# 051-entities.md — ENTITY MAPPING

This document maps all JSON fields from the device GET response to their corresponding Home Assistant entities created by the Autobayt integration.

---

## Device-Level Entities

### Sensor Entities

#### Connection Status Sensor
- **Entity Type:** `sensor`
- **Entity ID:** `sensor.{device_name}_connection`
- **Unique ID:** `{device_id}_connection`
- **Primary JSON Field:** `connection_status`
- **Device Class:** `enum`
- **Possible Values:** `connected`, `disconnected`
- **Additional Attributes:**
  - `is_hub` (from JSON: `is_hub`)
  - `slave_id` (from JSON: `slave_id`)
  - `room_name` (from JSON: `room_name`)

#### Signal Strength Sensor
- **Entity Type:** `sensor`
- **Entity ID:** `sensor.{device_name}_signal_strength`
- **Unique ID:** `{device_id}_signal_strength`
- **Primary JSON Field:** `sstr`
- **Device Class:** `signal_strength`
- **Unit:** `dBm`
- **State Class:** `measurement`

#### Firmware Version Sensor
- **Entity Type:** `sensor`
- **Entity ID:** `sensor.{device_name}_firmware`
- **Unique ID:** `{device_id}_firmware`
- **Primary JSON Field:** `firmware_version`
- **Additional Attributes:**
  - `model_name` (from JSON: `model_name`)
  - `next_version` (from JSON: `next_firmware[0].version_name`)
  - `next_file` (from JSON: `next_firmware[0].file_name`)
  - `version_code` (from JSON: `next_firmware[0].version_code`)

#### Update Status Sensor
- **Entity Type:** `sensor`
- **Entity ID:** `sensor.{device_name}_update_status`
- **Unique ID:** `{device_id}_update_status`
- **Primary JSON Field:** `is_updating`
- **Device Class:** `enum`
- **Possible Values:** `idle`, `updating`
- **Additional Attributes:**
  - `update_percentage` (from JSON: `perc`)

---

## Button-Level Entities

### Switch Entities

#### Button Switch
- **Entity Type:** `switch`
- **Entity ID:** `switch.{device_name}_{button_name}`
- **Unique ID:** `{device_id}_button_{button_id}`
- **Primary JSON Field:** `buttons[n].switch_state`
- **Additional Attributes:**
  - `button_id` (from JSON: `buttons[n].button_id`)
  - `dpb_state` (from JSON: `buttons[n].dpb_state`)
  - `power_on_state` (from JSON: `buttons[n].power_on_state`)
  - `mode` (from JSON: `buttons[n].mode`)
  - `toggle_delay` (from JSON: `buttons[n].toggle_delay`)

---

## JSON Field Categories

### Core Device Information
- `device_id` → Used as device identifier
- `name` → Used as device name
- `model_name` → Device model (shown in device info)
- `firmware_version` → Current firmware version (sensor + device info)

### Connection & Network
- `connection_status` → Connection Status Sensor (primary value)
- `sstr` → Signal Strength Sensor (primary value)
- `is_hub` → Connection Status Sensor (attribute)
- `slave_id` → Connection Status Sensor (attribute)

### Firmware & Updates
- `firmware_version` → Firmware Version Sensor (primary value)
- `next_firmware` → Firmware Version Sensor (attributes)
  - `version_name`
  - `file_name`
  - `version_code`
  - `require_client_update`
  - `app_version_code`
- `is_updating` → Update Status Sensor (primary value)
- `perc` → Update Status Sensor (attribute)

### Location & Organization
- `room_id` → Not currently used
- `room_name` → Connection Status Sensor (attribute)
- `loc_id` → Not currently used

### Switch/Button Configuration
- `buttons[]` → Array of button configurations
  - `switch_state` → Switch Entity (state)
  - `button_id` → Switch Entity (identifier + attribute)
  - `name` → Switch Entity (name)
  - `dpb_state` → Switch Entity (attribute)
  - `power_on_state` → Switch Entity (attribute)
  - `mode` → Switch Entity (attribute)
  - `toggle_delay` → Switch Entity (attribute)

### Internal/System Fields (Not Exposed)
- `period` → Internal polling period
- `pat_period` → Internal pattern period

---

## Entity Summary by Category

| Category | Entity Type | Count per Device |
|----------|-------------|------------------|
| **Device Status** | Sensor | 4 (connection, signal, firmware, update) |
| **Switch Controls** | Switch | 1-N (depends on buttons array) |

---

## Notes
- All entities share the same device info (linked by `device_id`)
- Button count varies by model (SW100 = 1 button, SW200 = 2 buttons, etc.)
- Entity availability depends on `connection_status` and coordinator update success
- Unique IDs ensure entities persist across restarts and config changes
