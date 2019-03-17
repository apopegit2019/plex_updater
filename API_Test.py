import requests
import os
import re
import subprocess
import time


def version_check():  # decides whether a new version is available.
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    item = {}
    for item in data['computer']['Linux']['releases']:
        if item['distro'] == 'debian' and item['build'] == 'linux-x86_64':
            download = item['url']
            print(download)
        else:
            print('nope')




version_check()
