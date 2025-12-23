# 020 — Setup/Deployment

## Method 1: Manual Installation
1. Download or clone this repository [home-assistant-autobayt](https://github.com/RASBR/home-assistant-autobayt.git) from Github
2. Copy the `custom_components/autobayt` folder to your Home Assistant `custom_components` directory:
   ```
   <config>/custom_components/autobayt/
   ```
3. Restart Home Assistant
4. Go to **Settings** → **Devices & Services** → **Add Integration**
5. Search for "AUTOBAYT" and follow the setup wizard

## Configuration

### Initial Setup
1. During setup, you'll need your **AUTOBAYT User ID** (24-character hexadecimal string)
2. Example: `507f1f77bcf86cd799439011`
3. The integration will automatically discover all devices associated with your account

### Device Discovery
- New devices are automatically discovered
- Each device appears with comprehensive monitoring entities
- Devices can be added individually as needed

## Method 2: Automatic via **HACS**
Planned for *Phase 3* and beyond.


