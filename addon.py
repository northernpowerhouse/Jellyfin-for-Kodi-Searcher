import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import json
import os
import urllib.parse

# --- Globals - Best practice to define these at the top ---
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
# Use getLocalizedString for all user-facing text
L = ADDON.getLocalizedString
ADDON_PROFILE = xbmc.translatePath(ADDON.getAddonInfo('profile'))
CACHE_FILE = os.path.join(ADDON_PROFILE, 'media_cache.json')
HANDLE = int(sys.argv[1])

def run():
    """Main router function."""
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
    action = params.get('action')

    if action == 'get_categories':
        populate_settings_categories()
    elif action == 'rebuild_cache':
        crawl_and_cache_media()
    elif action == 'search':
        perform_search()
    else:
        main_menu()

def main_menu():
    """Builds the addon's root directory."""
    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=False, listitem=xbmcgui.ListItem())
    
    li_search = xbmcgui.ListItem(label='[B]Start Search[/B]')
    search_url = f'plugin://{ADDON_ID}?action=search'
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=search_url, listitem=li_search, isFolder=True)
    
    li_settings = xbmcgui.ListItem(label='Open Settings')
    # This is a special Kodi command to open the settings dialog for our addon
    settings_url = f'RunPlugin(plugin://{ADDON_ID}/_settings)' # A more robust way to open settings
    xbmc.executebuiltin(f'Addon.OpenSettings({ADDON_ID})')
    # We will just make a button that opens settings
    li = xbmcgui.ListItem(label='Open Settings')
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=f'plugin://{ADDON_ID}/', listitem=li_settings, isFolder=False)
    ADDON.openSettings()

    xbmcplugin.endOfDirectory(HANDLE)

def populate_settings_categories():
    """Gets libraries from Jellyfin to populate the settings dialog."""
    try:
        # JSON-RPC is the correct way to get directory listings programmatically
        rpc_call = {
            "jsonrpc": "2.0",
            "method": "Files.GetDirectory",
            "params": {"directory": "plugin://plugin.video.jellyfin/", "media": "files"},
            "id": 1
        }
        response = json.loads(xbmc.executeJSONRPC(json.dumps(rpc_call)))

        if 'result' in response and 'files' in response['result']:
            for item in response['result']['files']:
                # Filter for directories that represent user libraries
                if item.get('filetype') == 'directory' and '/library/' in item.get('file', ''):
                    li = xbmcgui.ListItem(label=item['label'])
                    # For a multistring, the URL becomes the value
                    xbmcplugin.addDirectoryItem(handle=HANDLE, url=item['file'], listitem=li, isFolder=False)
        
        xbmcplugin.endOfDirectory(HANDLE)
    except Exception as e:
        xbmc.log(f'[{ADDON_ID}] ERROR: Failed to get Jellyfin categories: {e}', level=xbmc.LOGERROR)

def crawl_and_cache_media():
    """Crawls selected libraries and builds the search cache."""
    selected_libraries_str = ADDON.getSetting('search.libraries')
    if not selected_libraries_str:
        xbmcgui.Dialog().ok(ADDON_NAME, L(32100), L(32101))
        return

    # Semicolon is the separator for multistring settings
    selected_paths = [path for path in selected_libraries_str.split(';') if path]
    
    pDialog = xbmcgui.DialogProgressBG()
    pDialog.create(ADDON_NAME, 'Building media cache...')
    
    all_media = []
    
    for i, path in enumerate(selected_paths):
        progress = int((i / len(selected_paths)) * 100)
        pDialog.update(progress, message=f'Crawling library: {urllib.parse.unquote(path)}')
        
        try:
            rpc_call = {
                "jsonrpc": "2.0",
                "method": "Files.GetDirectory",
                "params": {"directory": path, "media": "video", "properties": ["art", "title"]},
                "id": 1
            }
            response = json.loads(xbmc.executeJSONRPC(json.dumps(rpc_call)))

            if 'result' in response and 'files' in response['result']:
                for item in response['result']['files']:
                    if item.get('filetype') == 'file': # Only add playable files
                        all_media.append({
                            'label': item['label'],
                            'path': item['file'],
                            'icon': item.get('art', {}).get('thumb', 'DefaultVideo.png')
                        })
            if pDialog.isFinished():
                break
        except Exception as e:
            xbmc.log(f'[{ADDON_ID}] ERROR: Could not crawl path {path}: {e}', level=xbmc.LOGERROR)
            
    pDialog.close()
    
    if not os.path.exists(ADDON_PROFILE):
        os.makedirs(ADDON_PROFILE)

    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_media, f, indent=2)

    # Use the localized string and format it with the count
    xbmcgui.Dialog().notification(ADDON_NAME, L(32102) + " " + L(32103).format(len(all_media)), xbmcgui.NOTIFICATION_INFO, 5000)


def perform_search():
    """Gets user input and displays search results."""
    if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) < 5:
        xbmcgui.Dialog().ok(ADDON_NAME, L(32104), L(32105))
        return

    keyboard = xbmc.Keyboard('', 'Search Your Jellyfin Library')
    keyboard.doModal()
    if not keyboard.isConfirmed() or not keyboard.getText():
        return
        
    query = keyboard.getText().lower()

    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        media_items = json.load(f)

    results = [item for item in media_items if query in item['label'].lower()]

    xbmcplugin.setResolvedUrl(handle=HANDLE, succeeded=False, listitem=xbmcgui.ListItem())
    for item in results:
        li = xbmcgui.ListItem(label=item['label'])
        li.setArt({'thumb': item.get('icon', 'DefaultVideo.png'), 'icon': item.get('icon', 'DefaultVideo.png')})
        li.setInfo('video', {'title': item['label']})
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=item['path'], listitem=li, isFolder=False)
    
    xbmcplugin.endOfDirectory(HANDLE)


if __name__ == '__main__':
    run()
