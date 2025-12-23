<div align="center">
  <img src="custom_components/autobayt/brands/autobayt/autobayt-banner-3.png" alt="Autobayt Banner" width="250"/>
  
  # Autobayt Home Assistant Integration

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1+-blue.svg)](https://www.home-assistant.io/)

  **A comprehensive Home Assistant custom integration for Autobayt smart switches with automatic device discovery and seamless control.**

  <img src="custom_components/autobayt/brands/autobayt/icon.png" alt="Autobayt Icon" width="120"/>
</div>

---

## ✨ Features

- 💡 **Smart Switch Control** - Control single, double, and triple switch devices
- 🔍 **Automatic Device Discovery** - Devices appear automatically for easy addition
- 📊 **Real-time Monitoring** - Connection status, signal strength, and firmware tracking
- 🔄 **Update Status** - Monitor firmware update progress
- 🏠 **Modern Home Assistant Integration** - Config flow setup, device registry, proper unique IDs
- 🖼️ **Custom Icons & Logos** - Local fallback icons included for offline operation
- 🔗 **Device Consolidation** - Automatically combines devices by MAC address across integrations
- 🌐 **Hub & Slave Support** - Full support for hub and slave device configurations

## 📱 Supported Devices

### SW100HV1 - Smart Switch Single
Single button smart switch with WiFi connectivity.

### SW100PMV1 - Smart Switch Single with Power Monitoring
Single button smart switch with power monitoring capabilities.

### SW200LV1 - Smart Switch Double
Dual button smart switch for controlling two separate circuits.

### SW300LV1 - Smart Switch Triple
Triple button smart switch for controlling three separate circuits.

## 📊 Entity Details

For each device, the integration creates:

### Switches
- **Button Switches** - One switch entity per button
  - Example: `switch.entrance_sw100hv1` (single button)
  - Example: `switch.pumps_room_inside`, `switch.pumps_room_outside` (double button)
  - Control each button independently
  - Displays power on state, mode, and toggle delay

### Sensors
- **Connection Status** (`sensor.{name}_connection`) - Shows connected/disconnected state
  - Additional attributes: is_hub, slave_id, room_name
- **Signal Strength** (`sensor.{name}_signal_strength`) - WiFi signal strength in dBm
- **Firmware Version** (`sensor.{name}_firmware`) - Current firmware version
  - Additional attributes: next_version, next_file, version_code
- **Update Status** (`sensor.{name}_update_status`) - Shows idle/updating state
  - Additional attributes: update_percentage

## 🚀 Installation

### Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/autobayt` folder to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant
4. The integration is now ready to configure!

### Directory Structure
After installation, you should have:
```
config/
  custom_components/
    autobayt/
      __init__.py
      manifest.json
      config_flow.py
      coordinator.py
      sensor.py
      switch.py
      const.py
      device.py
      http.py
      icons.json
      strings.json
      icon.png
      logo.png
      brands/
        autobayt/
          icon.png
          logo.png
      translations/
        en.json
```

## ⚙️ Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **"+ ADD INTEGRATION"**
3. Search for **"Autobayt"** and select it
4. Enter your **24-character User ID**
   - Example: `67b1b9cbc53b2600rtgb1234`
5. Click **"SUBMIT"**

### Device Discovery & Addition

After successful setup:

1. **Automatic Discovery**: Your devices will automatically appear in the "Discovered" section
2. **Device Information**: Each discovered device shows:
   - Autobayt logo
   - Device name and model (e.g., SW100HV1)
   - Device type (Smart Switch Single, Double, or Triple)
3. **Adding Devices**: Click "CONFIGURE" then "SUBMIT" on devices you want to add
4. **Configuration**: Customize device name, area, and other settings
5. **Completion**: Your device and its entities are now available

## 🎮 Usage Examples

### Control Switches

Turn on a switch:
```yaml
service: switch.turn_on
target:
  entity_id: switch.entrance_sw100hv1
```

Turn off a specific button:
```yaml
service: switch.turn_off
target:
  entity_id: switch.pumps_room_inside
```

### Automation Examples

#### Turn on light when connection is restored
```yaml
automation:
  - alias: "Light on when online"
    trigger:
      platform: state
      entity_id: sensor.entrance_connection
      to: "connected"
    action:
      service: switch.turn_on
      target:
        entity_id: switch.entrance_sw100hv1
```

#### Alert on weak signal
```yaml
automation:
  - alias: "Weak WiFi Signal Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.entrance_signal_strength
      below: -80
    action:
      service: notify.notify
      data:
        message: "Entrance switch has weak WiFi signal ({{ states('sensor.entrance_signal_strength') }} dBm)"
```

#### Firmware update notification
```yaml
automation:
  - alias: "Firmware Update Available"
    trigger:
      platform: state
      entity_id: sensor.entrance_firmware
    condition:
      condition: template
      value_template: "{{ state_attr('sensor.entrance_firmware', 'next_version') is not none }}"
    action:
      service: notify.notify
      data:
        message: "Firmware update available for Entrance: {{ state_attr('sensor.entrance_firmware', 'next_version') }}"
```

## 🔧 Advanced Features

### Hub and Slave Devices
Autobayt devices can work in hub-slave configurations:
- **Hub devices** connect directly to WiFi
- **Slave devices** communicate through a hub
- The integration tracks these relationships via the `slave_id` attribute

### Device Consolidation
The integration automatically combines devices with the same MAC address from other integrations in the Home Assistant device registry.

### Custom Icons
Local fallback icons are included and automatically served by Home Assistant for offline operation.

### API Integration
- **Update Interval**: 290 seconds (optimized for device performance)
- **Endpoints**: Automatic API endpoint management
- **Error Handling**: Comprehensive error handling with user-friendly messages

## 🔍 Troubleshooting

### Common Issues

**"No devices found" Error:**
- Verify your User ID is exactly 24 characters
- Check internet connectivity
- Confirm Autobayt servers are online
- Ensure you have devices registered to your account

**Device Not Updating:**
- Check the connection status sensor
- Verify device internet connectivity (for hubs) or hub connection (for slaves)
- Review Home Assistant logs for API errors
- Try reloading the integration

**Switches Not Responding:**
- Check device connection status
- Verify hub is online (for slave devices)
- Check Home Assistant logs for API communication errors
- Ensure device firmware is up to date

**Icons Not Displaying:**
- Restart Home Assistant after installation
- Clear browser cache
- Check Home Assistant logs for HTTP view errors

**Discovery Not Working:**
- Wait a few minutes for initial API calls
- Check User ID format (24 characters)
- Reload integration from Settings → Devices & Services

### Logging

Enable debug logging by adding to `configuration.yaml`:
```yaml
logger:
  logs:
    custom_components.autobayt: debug
```

## 🛠️ Development

### API Endpoints
- **Device List**: `https://api.autobayt.com/v1/user/get-things?user_id={user_id}`
- **Device Detail**: `https://api.autobayt.com/v1/user/get-things?device_id={device_id}`
- **Device Control**: `https://api.autobayt.com/v1/device/trigger`

### API Request Format
```json
{
  "btnStates": [true],
  "btnIds": [0],
  "device_id": "923748bc5xy1"
}
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📋 Requirements

- Home Assistant 2024.1+
- Internet connection for device communication
- Autobayt account with registered devices
- Valid 24-character User ID

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues, questions, or feature requests:
- **GitHub Issues**: [Create an Issue](https://github.com/RASBR/home-assistant-autobayt/issues)
- **Repository**: [home-assistant-autobayt](https://github.com/RASBR/home-assistant-autobayt)

## 🗺️ Roadmap

### Phase 1 (Current - Complete) ✅
- Device discovery and management
- Switch control for all button types
- Connection and status monitoring
- Firmware tracking

### Phase 3 (Future)
- Account-level sensors
- HACS distribution
- Advanced features

---

**Made with ❤️ for the Home Assistant Community**
