# 051-api-response-mapping.md — API ENDPOINT DEFINITIONS

This document defines and explains the Autobayt API endpoints used by the integration, their parameters, responses, and field definitions.

---

## Device GET Method

### Purpose
Retrieves detailed information about a specific device by its device ID. This endpoint is used to fetch the current state and configuration of a single device.

### Endpoint
```
GET https://api.autobayt.com/v1/device?device_id={device_id}
```

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `device_id` | string | Yes | Unique identifier for the device |

### Response Structure
Returns an array containing a single device object with the following fields:

#### Core Device Information
- **`device_id`** (string): Unique device identifier (MAC address without colons `:`)
- **`name`** (string): User-defined device name
- **`model_name`** (string): Device model (e.g., "SW100HV1", "SW200LV1")
- **`firmware_version`** (string): Current firmware version (e.g., "1.9.11")

#### Connection & Network
- **`connection_status`** (boolean): Device online/offline status
  - `true` = Device is connected and reachable
  - `false` = Device is offline or unreachable
- **`sstr`** (string): Signal strength in dBm (e.g., "-49")
- **`is_hub`** (boolean): Whether device acts as a network hub
  - `true` = Device is a primary hub
  - `false` = Device is a slave connected to a hub
- **`slave_id`** (string): ID of the hub device if this is a slave (empty if hub)

#### Firmware & Update Information
- **`is_updating`** (boolean): Whether firmware update is in progress
  - `true` = Device is currently updating
  - `false` = Device is idle
- **`perc`** (number): Update progress percentage (0-100)
- **`next_firmware`** (array): Available firmware updates
  - **`version_name`** (string): Next firmware version
  - **`file_name`** (string): Firmware file name
  - **`version_code`** (number): Internal version code
  - **`require_client_update`** (boolean): Whether app update is needed
  - **`app_version_code`** (number): Required app version

#### Location & Organization
- **`room_id`** (string): Room identifier
- **`room_name`** (string): Room name (optional field)
- **`loc_id`** (string): Location identifier

#### Button Configuration
- **`buttons`** (array): Array of button/switch configurations
  - **`button_id`** (number): Button identifier (0-based index)
  - **`name`** (string): User-defined button name
  - **`switch_state`** (boolean): Current button state
    - `true` = Switch is ON
    - `false` = Switch is OFF
  - **`dpb_state`** (number): Double-press button state
  - **`power_on_state`** (string): Behavior when power is restored
    - `"Off"` = Turn off when power restored
    - `"On"` = Turn on when power restored
    - `"Same"` = Restore previous state
  - **`mode`** (number): Button operation mode
  - **`toggle_delay`** (number): Delay in milliseconds for toggle operations

#### System Fields
- **`period`** (number): Polling period in milliseconds (typically 20000)
- **`pat_period`** (number): Pattern period (typically 30)

### Example Request
```bash
curl --location 'https://api.autobayt.com/v1/device?device_id=341876rt9sm3'
```

### Example Response
```json
[
  {
    "device_id": "341876rt9sm3",
    "name": "Pumps Room",
    "model_name": "SW200LV1",
    "firmware_version": "1.9.11",
    "connection_status": true,
    "sstr": "-49",
    "is_hub": true,
    "slave_id": "",
    "is_updating": false,
    "perc": 0,
    "buttons": [
      {
        "button_id": 0,
        "name": "Inside",
        "switch_state": false,
        "power_on_state": "Off"
      },
      {
        "button_id": 1,
        "name": "Outside",
        "switch_state": false,
        "power_on_state": "Off"
      }
    ]
  }
]
```

### Usage in Integration
This endpoint is called by the coordinator during:
- Initial device setup in config flow
- Periodic refresh to update device state
- Manual refresh requested by user

---

## SWITCH On/Off POST Method

### Purpose
Controls device buttons/switches by sending state change commands. This endpoint toggles switch states and returns the updated device information.

### Endpoint
```
POST https://api.autobayt.com/v1/device/trigger
```

### Request Headers
```
Content-Type: application/json
```

### Request Body Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `device_id` | string | Yes | Unique identifier for the target device |
| `btnIds` | array[number] | Yes | Array of button IDs to control (0-based) |
| `btnStates` | array[boolean] | Yes | Array of desired states (true=ON, false=OFF) |

### Request Body Structure
```json
{
  "device_id": "341876rt9sm3",
  "btnIds": [0],
  "btnStates": [true]
}
```

### Multi-Button Control
To control multiple buttons simultaneously:
```json
{
  "device_id": "341876rt9sm3",
  "btnIds": [0, 1],
  "btnStates": [true, false]
}
```

### Response Structure
Returns an object with a nested `device` object containing extended device information:

#### Additional Fields (Not in GET Response)
- **`_id`** (string): MongoDB document ID
- **`device_status`** (string): Device configuration status (e.g., "conf_done")
- **`on_gogl`** (boolean): Google Home integration status
- **`on_alexa`** (boolean): Amazon Alexa integration status
- **`model_code`** (string): Lowercase model code (e.g., "sw200lv1")
- **`updated`** (string): Last update timestamp (ISO 8601)
- **`user_id`** (string): Owner user ID
- **`added_by`** (string): User ID who added the device
- **`connected`** (string): Last connection timestamp (ISO 8601)
- **`ram`** (string): Available RAM on device
- **`__v`** (number): MongoDB version key

### Example Request
```bash
curl --location 'https://api.autobayt.com/v1/device/trigger' \
--header 'Content-Type: application/json' \
--data '{
  "device_id": "341876rt9sm3",
  "btnIds": [0],
  "btnStates": [true]
}'
```

### Example Response
```json
{
  "device": {
    "_id": "68f749c5a211ac001359119b",
    "device_id": "341876rt9sm3",
    "name": "Pumps Room",
    "model_name": "SW200LV1",
    "firmware_version": "1.9.11",
    "connection_status": true,
    "sstr": "-49",
    "is_hub": true,
    "is_updating": false,
    "on_gogl": false,
    "on_alexa": false,
    "updated": "2025-10-21T08:52:21.616Z",
    "connected": "2025-12-23T04:34:30.742Z"
  }
}
```

### Usage in Integration
This endpoint is called when:
- User toggles a switch entity in Home Assistant
- `turn_on()` service is called on a switch entity
- `turn_off()` service is called on a switch entity
- Automation triggers a switch state change

### Important Notes
1. **Array Alignment**: `btnIds` and `btnStates` arrays must have the same length
2. **Button ID**: Button IDs are 0-based (first button = 0, second = 1, etc.)
3. **State Values**: `true` = ON/activated, `false` = OFF/deactivated
4. **Response Nesting**: Response wraps device data in a `device` object (unlike GET method)
5. **Extra Fields**: POST response includes additional database and integration fields

---

## Response Comparison

### GET vs POST Response Differences

| Field | GET Response | POST Response | Notes |
|-------|--------------|---------------|-------|
| Root structure | Array `[{}]` | Object `{device: {}}` | Different wrapping |
| `_id` | ❌ Not included | ✅ Included | MongoDB document ID |
| `device_status` | ❌ Not included | ✅ Included | Configuration status |
| `on_gogl` | ❌ Not included | ✅ Included | Google integration |
| `on_alexa` | ❌ Not included | ✅ Included | Alexa integration |
| `model_code` | ❌ Not included | ✅ Included | Lowercase model |
| `updated` | ❌ Not included | ✅ Included | Update timestamp |
| `user_id` | ❌ Not included | ✅ Included | Owner ID |
| `added_by` | ❌ Not included | ✅ Included | Added by user ID |
| `connected` | ❌ Not included | ✅ Included | Connection timestamp |
| `ram` | ❌ Not included | ✅ Included | Device RAM |
| `buttons` | ✅ Included | ❌ Not included | Button configuration |
| `next_firmware` | ✅ Included | ❌ Not included | Firmware update info |
| `room_name` | ✅ Sometimes | ❌ Not included | Room name |

---

## Error Handling

### Common Error Scenarios
1. **Invalid device_id**: Device not found
2. **Device offline**: `connection_status: false` in response
3. **Invalid button_id**: Button ID exceeds available buttons
4. **Network timeout**: Device not responding
5. **Authentication failure**: Invalid credentials or token

### Integration Response
- Failed requests trigger coordinator error state
- Entities become unavailable during connection issues
- Retry logic handles transient failures
- User is notified via Home Assistant notifications

---

## Rate Limiting & Best Practices

1. **Polling Interval**: Respect the `period` field (typically 20000ms = 20 seconds)
2. **Batch Operations**: When possible, control multiple buttons in single request
3. **State Verification**: Check response to confirm state change was successful
4. **Error Recovery**: Implement exponential backoff for failed requests
5. **Connection Status**: Monitor `connection_status` before sending commands

---

## See Also
- [050-api-response-samples.md](../agent/050-api-response-samples.md) → Full API response samples
- [052-entities.md](docs/project/052-entities.md) → Entity mapping reference
- [040-api-usage.md](../agent/040-api-usage.md) → API usage guidelines
