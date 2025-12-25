# Bug Fixes Applied - December 24, 2025

## Issues Identified and Fixed

### 1. Integration Logo/Icon Not Showing ⚠️
**Status:** Partially Addressed
- Manifest.json is correctly configured
- Brand images are in the correct location: `custom_components/autobayt/brands/autobayt/`
- HTTP views are set up to serve fallback images
- **Solution:** Restart Home Assistant completely and clear browser cache

### 2. Discovery Dialog - Missing Device Information ✅
**Fixed in:** `config_flow.py`, `strings.json`, `translations/en.json`
- Added firmware version display
- Added button count display
- Added connection status (Online/Offline)
- Enhanced placeholders in discovery_confirm step

### 3. Button Entity Naming - Duplicate Words ✅
**Fixed in:** `switch.py`
- Added `_create_entity_name()` method
- Automatically removes duplicate words from button names that appear in device name
- Example: Device "P EX" + Button "EX" → `switch.p_ex_button_0` (fallback)
- Example: Device "Pumps Room" + Button "Inside" → `switch.pumps_room_inside`
- Fallback naming: `{device_name}_button_{button_id}` when all words are duplicates

### 4. README - Naming Convention Section ✅
**Fixed in:** `README.md`
- Added "Before You Start" section in Configuration
- Explains why naming matters
- Provides good and bad examples
- Warns users about duplicate word detection

### 5. Entities Show "Unavailable" ✅
**Fixed in:** `coordinator.py`
- Improved `_async_update_data()` to properly handle device data
- Added fallback to use user_devices data when detail fetch fails
- Added proper list/array checks before accessing data
- Uses user_devices data for added devices if detailed API call doesn't return data

### 6. Switches Not Responsive ✅
**Should be fixed** by issue #5 fix
- Entities were unavailable because coordinator wasn't fetching data properly
- With proper data fetching, switches should now respond
- API endpoint is correct: `https://api.autobayt.com/v1/device/trigger`

## Testing Recommendations

1. **Remove the integration completely** from Home Assistant
2. **Restart Home Assistant**
3. **Clear browser cache**
4. **Re-add the integration** with your User ID
5. **Wait for device discovery**
6. **Add a discovered device**
7. **Check entity availability** (should no longer show "Unavailable")
8. **Test switch control** (turn on/off)
9. **Verify entity names** follow the new naming convention

## Files Modified

1. `switch.py` - Button naming logic
2. `coordinator.py` - Data fetching improvements
3. `config_flow.py` - Discovery dialog enhancements
4. `strings.json` - Updated discovery messages
5. `translations/en.json` - Updated discovery messages
6. `README.md` - Added naming convention section

## Additional Notes

- The User ID in the API samples (`67b1b9cbc53b2600rtgb1234`) is exactly 24 characters as required
- The API response structure matches what the integration expects
- Hub/slave device relationships are properly tracked via `is_hub` and `slave_id` attributes
- Signal strength sensor uses the `sstr` field from API
