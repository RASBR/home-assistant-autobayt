# Icon and Logo Setup for Home Assistant Integrations

## Working Solution (Based on Kaco)

### Directory Structure
```
custom_components/
  autobayt/
    static/
      icon.png        # Integration icon (square, recommended 256x256px)
      logo.png        # Integration logo (rectangular, recommended 512x128px)
    manifest.json
```

### manifest.json Configuration
```json
{
  "domain": "autobayt",
  "name": "Autobayt",
  "icon": "static/icon.png",
  "logo": "static/logo.png"
}
```

### File Requirements
- **icon.png**: Square format, transparent background, PNG format
- **logo.png**: Rectangular format, can include text, PNG format
- Place files in `static/` subdirectory within integration folder
- Reference with relative path: `"static/icon.png"`

## What Didn't Work

### Attempt 1: Root Level Files
- Files: `icon.png`, `logo.png` in integration root
- Result: ❌ Not displayed in integration list

### Attempt 2: Brands Folder
- Files in `brands/autobayt/icon.png`
- Result: ❌ Not displayed in integration list

### Attempt 3: MDI Icon Fallback
- Using `"icon": "mdi:light-switch"` in manifest
- Result: ❌ Still didn't show custom icons

### Attempt 4: HTTP Views
- Created http.py to serve brand images
- Result: ❌ Doesn't affect integration list display

## Working Examples in Workspace

### Kaco (WORKING ✅)
```
kaco/
  static/
    icon.png
    logo.png
    dark_icon.png
    dark_logo.png
  manifest.json → "icon": "static/icon.png"
```

### Gobzigh (Icons in root, no manifest reference)
```
gobzigh/
  icon.png
  logo.png
  brands/
    gobzigh/
      icon.png
      logo.png
  manifest.json → No icon/logo keys
```

## Implementation Steps

1. **Create static folder**
   ```bash
   mkdir custom_components/autobayt/static
   ```

2. **Copy icon and logo files**
   ```bash
   cp icon.png static/icon.png
   cp logo.png static/logo.png
   ```

3. **Update manifest.json**
   ```json
   {
     "icon": "static/icon.png",
     "logo": "static/logo.png"
   }
   ```

4. **Restart Home Assistant**
   - Full restart required for manifest changes
   - Clear browser cache (Ctrl+F5)

## Testing Locations

Icons should appear in:
1. **Settings → Devices & Services → Add Integration** (search list)
2. **Integration card** after installation
3. **Device pages** (uses device manufacturer info)

## Notes

- Home Assistant caches integration metadata
- Changes require full restart, not just reload
- Browser cache must be cleared
- PNG format recommended over SVG
- Transparent backgrounds work best
- Square icons look best in integration list

## Future Reference

For new integrations:
1. Always use `static/` folder for icon/logo files
2. Always add `"icon"` and `"logo"` keys to manifest.json
3. Use relative paths: `"static/filename.png"`
4. Test after full HA restart and browser cache clear
