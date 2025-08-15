# Jellyfin-for-Kodi-Searcher
Jellyfin Library Searcher for Kodi
A powerful search utility designed to work with the Jellyfin for Kodi addon, specifically for users operating in Add-on Mode. This addon creates a fast, local search index of your Jellyfin media, allowing for near-instant search results that can be seamlessly integrated into skins like Arctic Fuse 2.
The Problem It Solves
The official 'Jellyfin for Kodi' addon is excellent, but when used in its default "Add-on Mode," it does not integrate with Kodi's native library. This means that skin-level search functions and global search addons cannot find your Jellyfin media. The alternative, "Sync Mode," integrates with the library but can be slow or undesirable for some setups.
This addon provides the best of both worlds: the speed and simplicity of Add-on Mode with the powerful, integrated search of a native library.
Key Features
Creates a Local Search Index: Crawls your selected Jellyfin libraries to build a local cache of all media items.
Incremental, Scheduled Updates: After an initial full scan, the addon can run a small, fast scan automatically every day at a time you choose. It only scans for new content, making daily updates incredibly quick.
Automatic Data Pruning: To save space, the cache automatically removes items with an air date older than 14 days during each incremental scan.
Configurable Performance: Adjust the number of parallel crawling threads to match your hardware, from a high-performance PC to a low-power TV box.
Skin Integration: Designed to integrate perfectly with the global search functions of modern skins like Arctic Fuse 2.
Contextual Metadata: Search results display the location of the media file (e.g., TV / Channel / Fri 15-08-2025) in the plot summary, so you know exactly which version you're looking at.
How It Works
The addon operates in two stages:
Full Scan (Run Once): The first time you run it, you must perform a "Full Media Rebuild." This is a slow, one-time process where the addon recursively scans every single folder in your selected libraries to build the initial search cache. This will take time, especially on large libraries.
Incremental Scan (Fast & Automatic): Once the initial cache is built, the addon switches to a much faster incremental mode. It intelligently prunes old data and only scans for new content since the last update. This can be scheduled to run automatically in the background, ensuring your search index is always up-to-date with minimal performance impact.
Installation
Navigate to the Releases page of this repository.
Download the latest plugin.video.jellyfin.searcher-x.x.x.zip file.
In Kodi, go to Settings -> Add-ons -> Install from zip file.
Locate and select the .zip file you just downloaded.
Setup and Configuration (Very Important)
After installation, you must configure the addon before its first use.
Open Settings: Navigate to Add-ons -> Video add-ons, find the Jellyfin Library Searcher, and open its Settings.
Select Libraries:
In the "Search Scope" tab, click on the line that says Select Jellyfin Libraries to Search....
A multi-select dialog will appear, populated with the library views from your Jellyfin addon (e.g., "Films (dynamic)", "TV (dynamic)").
Select all the libraries you want to be included in your search index and click OK.
Configure Performance:
In the "Maintenance" tab, adjust the Crawler Threads slider.
Recommendation for a PC: Start with a higher value like 12.
Recommendation for a TV Box (e.g., s928x): Start with a lower value like 4 to avoid overwhelming the device.
Enable Automatic Scanning:
In the "Automatic Scanning" tab, toggle Enable Daily Automatic Scan.
Set the Time to Run Scan in 24-hour HH:MM format (e.g., 04:00 for 4 AM).
⚠️ Run the Initial Full Scan:
This is the most critical step. Go back to the "Maintenance" tab and click Full Media Rebuild (Slow, Run Once).
Let this process run to completion. You will receive a notification when it's finished.
Your addon is now fully configured. The daily incremental scans will run automatically if you enabled them.
Usage
Direct Search
You can run a search at any time by opening the addon from the Video Add-ons screen and selecting [B]Start Search[/B].
Arctic Fuse 2 Skin Integration
To integrate with the skin's global search feature:
Go to Settings -> Interface -> Skin -> - Configure skin....
Navigate to General -> Search.
Under the CUSTOM SEARCHES section, click an empty slot (e.g., Addon 1).
For Name, enter Jellyfin Search.
For Custom Path, carefully enter the following string:
code
Code
plugin://plugin.video.jellyfin.searcher/?action=search_external&query=
Exit the skin settings.
Now, when you use the skin's search function, "Jellyfin Search" will appear as an option, and selecting it will return results directly from your cache.
License
This project is licensed under the MIT License.
