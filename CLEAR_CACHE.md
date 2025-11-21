# Browser Cache Clearing Instructions

The CORS error you're seeing is due to browser cache holding the old version of the page.

## How to Fix:

### Option 1: Hard Refresh (Recommended)
- **Chrome/Edge**: Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
- **Firefox**: Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
- **Safari**: Press `Cmd + Option + R`

### Option 2: Clear Browser Cache
1. Open Chrome DevTools (F12)
2. Right-click on the refresh button
3. Select "Empty Cache and Hard Reload"

### Option 3: Open in Incognito/Private Mode
- **Chrome**: `Ctrl + Shift + N`
- **Firefox**: `Ctrl + Shift + P`
- **Edge**: `Ctrl + Shift + N`

### Option 4: Clear Site Data
1. Open Chrome DevTools (F12)
2. Go to Application tab
3. Click "Clear storage" on the left
4. Click "Clear site data"

## Verification

After clearing cache, the DataTables should load without any CORS errors. The language configuration is now inline and doesn't rely on external CDN URLs.

## What Changed

We replaced:
```javascript
language: {
    url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/en-GB.json'
}
```

With inline configuration:
```javascript
language: {
    "emptyTable": "No data available in table",
    "info": "Showing _START_ to _END_ of _TOTAL_ entries",
    // ... etc
}
```

This eliminates the need for external language file requests and avoids CORS issues.