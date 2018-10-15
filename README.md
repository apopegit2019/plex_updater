# plex_updater
Small script I wrote to update my plex media server. Uses plex api https://plex.tv/api/downloads/1.json?channel=plexpass to compare epoch date of latest release to the running version. Downloads, installs, removes the installation file. It also adds some logging so I can see what happened later. 

To use this:

1. Edit the file paths for everything as desired (logging/installation file save location/current version.txt)
2. Make sure that the JSON information is correct for your OS
