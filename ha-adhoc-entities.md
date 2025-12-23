# Home Assistant Ad-Hoc Autobayt Entities Guide

This guide shows you how to create Autobayt device entities in Home Assistant without installing the full integration. This approach uses manual configuration through YAML files to create sensors, switches, and device trackers that communicate with the Autobayt API.

## Prerequisites

- Home Assistant instance with YAML configuration access
- Autobayt API credentials (user_id)
- Network access to `api.autobayt.com`

## Overview

The Autobayt API provides access to smart devices through REST endpoints. We'll create Home Assistant entities that:
- Fetch device states via REST API calls
- Control devices through POST requests
- Display device information and connection status

## API Endpoints Reference

### Get User Devices
```
GET https://api.autobayt.com/v1/user/get-things?user_id={user_id}
```

### Get Single Device
```
GET https://api.autobayt.com/v1/device/get-things?device_id={device_id}
```

### Control Device
```
POST https://api.autobayt.com/v1/device/trigger
Content-Type: application/json
{
  "btnStates": [true],
  "btnIds": [0],
  "device_id": "device_id_here"
}
```

## Device Data Structure

Each Autobayt device returns this JSON structure:
```json
{
  "room_id": "67b1b9cbc53b260012fe10f7",
  "connection_status": true,
  "slave_id": "",
  "is_hub": true,
  "is_updating": false,
  "perc": 0,
  "period": 20000,
  "pat_period": 30,
  "device_id": "485519ef1eb1",
  "name": "Entrance",
  "firmware_version": "1.9.11",
  "model_name": "SW100HV1",
  "sstr": "-67",
  "loc_id": "67b1b9e1c53b260012fe10f9",
  "next_firmware": [
    {
      "version_name": "1.9.11",
      "file_name": "sw100hv1_1.9.11.bin",
      "version_code": 92,
      "require_client_update": false,
      "app_version_code": 1
    }
  ],
  "buttons": [
    {
      "switch_state": false,
      "dpb_state": 0,
      "power_on_state": "Same",
      "mode": 0,
      "toggle_delay": 0,
      "name": "SW100HV1",
      "button_id": 0
    }
  ],
  "room_name": "default"
}
```

## Configuration Steps

### Step 1: Configure REST API Integration

Add this to your `configuration.yaml`:

```yaml
# REST API configuration for Autobayt
rest:
  - resource: "https://api.autobayt.com/v1/user/get-things"
    method: GET
    params:
      user_id: "YOUR_USER_ID_HERE"  # Replace with your actual user ID
    scan_interval: 30
    timeout: 10
    headers:
      Content-Type: "application/json"
    sensor:
      - name: "Autobayt Devices Raw"
        unique_id: "autobayt_devices_raw"
        value_template: "{{ value_json | length }}"
        json_attributes_path: "$"
        json_attributes:
          - devices
        unit_of_measurement: "devices"
```

### Step 2: Create Template Sensors

Create a file `autobayt_sensors.yaml` in your `packages` directory (or add to `configuration.yaml`):

```yaml
# Autobayt Template Sensors
template:
  - sensor:
      - name: "Autobayt Device Count"
        unique_id: "autobayt_device_count"
        state: "{{ state_attr('sensor.autobayt_devices_raw', 'devices') | length }}"
        unit_of_measurement: "devices"
        icon: "mdi:home-automation"

      # Connection Status for Entrance Device
      - name: "Entrance Switch Status"
        unique_id: "autobayt_entrance_status"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {{ "online" if device.connection_status else "offline" }}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        icon: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {{ "mdi:wifi" if device.connection_status else "mdi:wifi-off" }}
              {% endif %}
            {% endfor %}
          {% else %}
            mdi:help
          {% endif %}

      # Signal Strength for Entrance Device
      - name: "Entrance Signal Strength"
        unique_id: "autobayt_entrance_signal"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {{ device.sstr }}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        unit_of_measurement: "dBm"
        icon: "mdi:signal"

      # Firmware Version for Entrance Device
      - name: "Entrance Firmware"
        unique_id: "autobayt_entrance_firmware"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {{ device.firmware_version }}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        icon: "mdi:chip"
        attributes:
          current_version: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" %}
                  {{ device.firmware_version }}
                {% endif %}
              {% endfor %}
            {% endif %}
          available_version: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.next_firmware[0].version_name }}
                {% endif %}
              {% endfor %}
            {% endif %}
          update_file: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.next_firmware[0].file_name }}
                {% endif %}
              {% endfor %}
            {% endif %}
          update_available: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.firmware_version != device.next_firmware[0].version_name }}
                {% endif %}
              {% endfor %}
            {% else %}
              false
            {% endif %}

      # Firmware Update Available for Entrance Device
      - name: "Entrance Next Firmware"
        unique_id: "autobayt_entrance_next_firmware"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                {{ device.next_firmware[0].version_name }}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        icon: "mdi:update"
        attributes:
          file_name: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.next_firmware[0].file_name }}
                {% endif %}
              {% endfor %}
            {% endif %}
          version_code: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.next_firmware[0].version_code }}
                {% endif %}
              {% endfor %}
            {% endif %}
          require_client_update: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                  {{ device.next_firmware[0].require_client_update }}
                {% endif %}
              {% endfor %}
            {% endif %}

      # Update Status for Entrance Device
      - name: "Entrance Update Status"
        unique_id: "autobayt_entrance_update_status"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {% if device.is_updating %}
                  updating
                {% else %}
                  idle
                {% endif %}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        icon: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {{ "mdi:download" if device.is_updating else "mdi:check-circle" }}
              {% endif %}
            {% endfor %}
          {% else %}
            mdi:help
          {% endif %}
        attributes:
          update_percentage: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" %}
                  {{ device.perc }}
                {% endif %}
              {% endfor %}
            {% endif %}

  # Binary Sensors for Switch States
  - binary_sensor:
      - name: "Entrance Switch State"
        unique_id: "autobayt_entrance_switch_state"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" %}
                {% if device.buttons and device.buttons|length > 0 %}
                  {{ device.buttons[0].switch_state }}
                {% endif %}
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
        device_class: switch
        icon: "mdi:light-switch"

      # Firmware Update Available Binary Sensor
      - name: "Entrance Firmware Update Available"
        unique_id: "autobayt_entrance_update_available"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                {{ device.firmware_version != device.next_firmware[0].version_name }}
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
        device_class: update
        icon: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "485519ef1eb1" and device.next_firmware and device.next_firmware|length > 0 %}
                {{ "mdi:package-up" if device.firmware_version != device.next_firmware[0].version_name else "mdi:package-check" }}
              {% endif %}
            {% endfor %}
          {% else %}
            mdi:package
          {% endif %}
```

### Step 3: Create REST Command for Device Control

Add this to your `configuration.yaml`:

```yaml
# REST Commands for Autobayt device control
rest_command:
  autobayt_switch_on:
    url: "https://api.autobayt.com/v1/device/trigger"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: >
      {
        "btnStates": [true],
        "btnIds": [{{ button_id | default(0) }}],
        "device_id": "{{ device_id }}"
      }
    timeout: 10

  autobayt_switch_off:
    url: "https://api.autobayt.com/v1/device/trigger"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: >
      {
        "btnStates": [false],
        "btnIds": [{{ button_id | default(0) }}],
        "device_id": "{{ device_id }}"
      }
    timeout: 10

  autobayt_toggle_switch:
    url: "https://api.autobayt.com/v1/device/trigger"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: >
      {
        "btnStates": [{{ switch_state }}],
        "btnIds": [{{ button_id | default(0) }}],
        "device_id": "{{ device_id }}"
      }
    timeout: 10
```

### Step 4: Create Switch Entity

Create switches that can control your devices:

```yaml
# Autobayt Switches
switch:
  - platform: template
    switches:
      entrance_light:
        friendly_name: "Entrance Light"
        unique_id: "autobayt_entrance_light_switch"
        value_template: "{{ is_state('binary_sensor.entrance_switch_state', 'on') }}"
        turn_on:
          service: rest_command.autobayt_switch_on
          data:
            device_id: "485519ef1eb1"
            button_id: 0
        turn_off:
          service: rest_command.autobayt_switch_off
          data:
            device_id: "485519ef1eb1"
            button_id: 0
        icon_template: >
          {% if is_state('binary_sensor.entrance_switch_state', 'on') %}
            mdi:lightbulb-on
          {% else %}
            mdi:lightbulb-off
          {% endif %}

      stairs_gf_light:
        friendly_name: "Stairs Ground Floor"
        unique_id: "autobayt_stairs_gf_light_switch"
        value_template: "{{ is_state('binary_sensor.stairs_gf_switch_state', 'on') }}"
        turn_on:
          service: rest_command.autobayt_switch_on
          data:
            device_id: "485519ef2b44"
            button_id: 0
        turn_off:
          service: rest_command.autobayt_switch_off
          data:
            device_id: "485519ef2b44"
            button_id: 0
        icon_template: >
          {% if is_state('binary_sensor.stairs_gf_switch_state', 'on') %}
            mdi:lightbulb-on
          {% else %}
            mdi:lightbulb-off
          {% endif %}
```

### Step 5: Create Multiple Device Sensors (Template)

For multiple devices, you can create a template for each device. Here's an example for the IT Center Light:

```yaml
template:
  - sensor:
      # IT Center Light Status
      - name: "IT Center Light Status"
        unique_id: "autobayt_it_center_status"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "d8bc388791d2" %}
                {{ "online" if device.connection_status else "offline" }}
              {% endif %}
            {% endfor %}
          {% else %}
            unavailable
          {% endif %}
        icon: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "d8bc388791d2" %}
                {{ "mdi:wifi" if device.connection_status else "mdi:wifi-off" }}
              {% endif %}
            {% endfor %}
          {% else %}
            mdi:help
          {% endif %}

  - binary_sensor:
      # IT Center Light Switch State
      - name: "IT Center Light Switch State"
        unique_id: "autobayt_it_center_switch_state"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "d8bc388791d2" %}
                {% if device.buttons and device.buttons|length > 0 %}
                  {{ device.buttons[0].switch_state }}
                {% endif %}
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
        device_class: switch
        icon: "mdi:light-switch"
```

### Step 6: Multi-Button Device Support

For devices with multiple buttons (like the Pumps Room SW200LV1), create separate entities:

```yaml
template:
  - binary_sensor:
      # Pumps Room - Inside Button
      - name: "Pumps Room Inside State"
        unique_id: "autobayt_pumps_inside_state"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "341876rt9sm3" %}
                {% if device.buttons and device.buttons|length > 0 %}
                  {{ device.buttons[0].switch_state }}
                {% endif %}
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
        device_class: switch

      # Pumps Room - Outside Button
      - name: "Pumps Room Outside State"
        unique_id: "autobayt_pumps_outside_state"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {% for device in devices %}
              {% if device.device_id == "341876rt9sm3" %}
                {% if device.buttons and device.buttons|length > 1 %}
                  {{ device.buttons[1].switch_state }}
                {% endif %}
              {% endif %}
            {% endfor %}
          {% else %}
            false
          {% endif %}
        device_class: switch

# Corresponding switches
switch:
  - platform: template
    switches:
      pumps_room_inside:
        friendly_name: "Pumps Room Inside"
        unique_id: "autobayt_pumps_inside_switch"
        value_template: "{{ is_state('binary_sensor.pumps_room_inside_state', 'on') }}"
        turn_on:
          service: rest_command.autobayt_switch_on
          data:
            device_id: "341876rt9sm3"
            button_id: 0
        turn_off:
          service: rest_command.autobayt_switch_off
          data:
            device_id: "341876rt9sm3"
            button_id: 0

      pumps_room_outside:
        friendly_name: "Pumps Room Outside"
        unique_id: "autobayt_pumps_outside_switch"
        value_template: "{{ is_state('binary_sensor.pumps_room_outside_state', 'on') }}"
        turn_on:
          service: rest_command.autobayt_switch_on
          data:
            device_id: "341876rt9sm3"
            button_id: 1
        turn_off:
          service: rest_command.autobayt_switch_off
          data:
            device_id: "341876rt9sm3"
            button_id: 1
```

## Device Information Template

For comprehensive device information in a single sensor:

```yaml
template:
  - sensor:
      - name: "Autobayt Device Info"
        unique_id: "autobayt_device_info"
        state: "{{ state_attr('sensor.autobayt_devices_raw', 'devices') | length }}"
        attributes:
          devices: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% set ns = namespace(device_list=[]) %}
              {% for device in devices %}
                {% set device_info = {
                  'name': device.name,
                  'device_id': device.device_id,
                  'model': device.model_name,
                  'firmware': device.firmware_version,
                  'connection': device.connection_status,
                  'signal_strength': device.sstr,
                  'is_hub': device.is_hub,
                  'room': device.room_name,
                  'buttons_count': device.buttons | length if device.buttons else 0,
                  'update_available': device.firmware_version != device.next_firmware[0].version_name if device.next_firmware and device.next_firmware|length > 0 else false,
                  'next_firmware': device.next_firmware[0].version_name if device.next_firmware and device.next_firmware|length > 0 else 'N/A',
                  'is_updating': device.is_updating,
                  'update_progress': device.perc if device.is_updating else 0
                } %}
                {% set ns.device_list = ns.device_list + [device_info] %}
              {% endfor %}
              {{ ns.device_list }}
            {% else %}
              []
            {% endif %}
```

## Creating Device Entities

If you want to create actual Home Assistant devices (that group related entities), add this configuration:

```yaml
# Device tracking sensor
template:
  - sensor:
      - name: "Autobayt Hub Devices"
        unique_id: "autobayt_hub_devices"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {{ devices | selectattr('is_hub', 'equalto', true) | list | length }}
          {% else %}
            0
          {% endif %}
        attributes:
          hubs: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {{ devices | selectattr('is_hub', 'equalto', true) | list }}
            {% else %}
              []
            {% endif %}

      - name: "Autobayt Slave Devices"
        unique_id: "autobayt_slave_devices"
        state: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {{ devices | selectattr('is_hub', 'equalto', false) | list | length }}
          {% else %}
            0
          {% endif %}
        attributes:
          slaves: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {{ devices | selectattr('is_hub', 'equalto', false) | list }}
            {% else %}
              []
            {% endif %}
```

## Automation Examples

### Basic On/Off Automation
```yaml
automation:
  - alias: "Turn on Entrance Light at Sunset"
    trigger:
      platform: sun
      event: sunset
    action:
      service: switch.turn_on
      target:
        entity_id: switch.entrance_light

  - alias: "Turn off all Autobayt lights at midnight"
    trigger:
      platform: time
      at: "00:00:00"
    action:
      - service: switch.turn_off
        target:
          entity_id: 
            - switch.entrance_light
            - switch.stairs_gf_light
            - switch.it_center_light
```

### Device Status Notification
```yaml
automation:
  - alias: "Autobayt Device Offline Notification"
    trigger:
      platform: template
      value_template: >
        {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
        {% if devices %}
          {{ devices | selectattr('connection_status', 'equalto', false) | list | length > 0 }}
        {% else %}
          false
        {% endif %}
    action:
      service: notify.notify
      data:
        title: "Autobayt Device Alert"
        message: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% set offline_devices = devices | selectattr('connection_status', 'equalto', false) | list %}
          Device(s) offline: {{ offline_devices | map(attribute='name') | join(', ') }}
```

### Firmware Update Notification
```yaml
automation:
  - alias: "Autobayt Firmware Update Available"
    trigger:
      - platform: state
        entity_id: binary_sensor.entrance_firmware_update_available
        to: "on"
    action:
      service: notify.notify
      data:
        title: "Autobayt Firmware Update"
        message: >
          Firmware update available for {{ state_attr('sensor.entrance_firmware', 'device_name') | default('Entrance') }}.
          Current: {{ state_attr('sensor.entrance_firmware', 'current_version') }}
          Available: {{ state_attr('sensor.entrance_firmware', 'available_version') }}

  - alias: "Autobayt Update Progress Monitor"
    trigger:
      - platform: template
        value_template: >
          {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
          {% if devices %}
            {{ devices | selectattr('is_updating', 'equalto', true) | list | length > 0 }}
          {% else %}
            false
          {% endif %}
    action:
      - service: notify.notify
        data:
          title: "Autobayt Update in Progress"
          message: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% set updating_devices = devices | selectattr('is_updating', 'equalto', true) | list %}
            {% for device in updating_devices %}
              {{ device.name }}: {{ device.perc }}%
            {% endfor %}

  - alias: "Autobayt All Devices Firmware Status"
    description: "Check all devices for firmware updates daily"
    trigger:
      - platform: time
        at: "09:00:00"
    action:
      - service: notify.notify
        data:
          title: "Autobayt Firmware Status"
          message: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% set ns = namespace(updates=[]) %}
              {% for device in devices %}
                {% if device.next_firmware and device.next_firmware|length > 0 %}
                  {% if device.firmware_version != device.next_firmware[0].version_name %}
                    {% set ns.updates = ns.updates + [device.name ~ ': ' ~ device.firmware_version ~ ' → ' ~ device.next_firmware[0].version_name] %}
                  {% endif %}
                {% endif %}
              {% endfor %}
              {% if ns.updates|length > 0 %}
                Updates available for:
                {{ ns.updates | join('\n') }}
              {% else %}
                All devices are up to date.
              {% endif %}
            {% else %}
              Unable to check firmware status.
            {% endif %}
```

## Customization

### Change Update Interval
Modify the `scan_interval` in the REST configuration:
```yaml
rest:
  - resource: "https://api.autobayt.com/v1/user/get-things"
    scan_interval: 60  # Update every 60 seconds instead of 30
```

### Add Custom Icons
Modify the icon templates in the switch configurations:
```yaml
icon_template: >
  {% if is_state('binary_sensor.entrance_switch_state', 'on') %}
    mdi:ceiling-light
  {% else %}
    mdi:ceiling-light-outline
  {% endif %}
```

### Custom Device Names
Change the `friendly_name` values to match your preferences:
```yaml
friendly_name: "Main Entrance Lighting"  # Instead of "Entrance Light"
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your `user_id` is correct
2. **API Timeouts**: Increase the `timeout` value in REST configuration
3. **Template Errors**: Check Home Assistant logs for syntax issues
4. **Switch Not Working**: Verify `device_id` and `button_id` are correct

### Debug Templates

Add this sensor to debug template values:
```yaml
template:
  - sensor:
      - name: "Autobayt Debug"
        state: "debug"
        attributes:
          raw_data: "{{ state_attr('sensor.autobayt_devices_raw', 'devices') }}"
          entrance_device: >
            {% set devices = state_attr('sensor.autobayt_devices_raw', 'devices') %}
            {% if devices %}
              {% for device in devices %}
                {% if device.device_id == "485519ef1eb1" %}
                  {{ device }}
                {% endif %}
              {% endfor %}
            {% endif %}
```

### API Rate Limiting

If you experience rate limiting, increase the scan_interval:
```yaml
scan_interval: 120  # 2 minutes
```

## Security Considerations

- Store your user_id in `secrets.yaml` instead of plain text
- Consider using a reverse proxy if exposing to the internet
- Monitor API usage to avoid hitting rate limits

## Next Steps

Once you have the basic entities working:
1. Create a dashboard card for device overview
2. Set up automations for device control
3. Add device monitoring alerts
4. Consider creating a proper integration if you need more features

This approach gives you full control over your Autobayt devices in Home Assistant without needing the full integration, while maintaining the flexibility to customize entity behavior and naming.