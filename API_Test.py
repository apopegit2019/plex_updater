import requests
import os
import re
import subprocess
import time


def version_check():  # decides whether a new version is available.
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    for item in data['computer']['Linux']['releases']:
        if item['distro'] == 'debian' and item['build'] == 'linux-x86_64':
            download = item['url']
            print(download)
        else:
            print('nope')


def version_check():  # decides whether a new version is available.
    with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'r') as curver:  # current version release epoch
        curvers = int(
            curver.readline())  # reads the epoch date from the file to compare to the API. Cast to int for compare
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    for item1 in data['computer']['Linux']['releases']:
        if item1['distro'] == 'debian' and item1['build'] == 'linux-x86_64':
            nversdate = int(item1['release_date'])  # pulls the API advertised epoch date for new version.
            # Cast to int for compare
            nvers = item1['version']  # pulls actual version number
        else:
            pass
    if nversdate > curvers:  # compares epoch from API to the one for the current version
        logging('New Version Found %s' % nvers)  # adds new version to the log
        with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'w') as new:
            new.write(str(nversdate))  # updating current version with new version epoch date
        get_download(data)  # move to download installation file
    else:
        logging('No Update Required.')
        exit()


def get_download(data):  # grab download installation file
    installDir = '/home/bukarubonzai/plexfiles2/updater/'  # directory where the file will be downloaded
    for item in data:
        if item['distro'] == 'debian' and item['build'] == 'linux-x86_64':
            download_url = item['url']  # just saving the URL to a variable for simplicity later
            os.chdir(installDir)  # move to the installation directory
            logging('Download Starting: %s' % download_url)
            try:
                subprocess.check_call(['wget', download_url])  # downloads current version
            except as dlexcept:
                logging(dlexcept + '\n')
                logging('Download Failed')
            install(download_url, installDir)  # moving to installation
        else:
            pass


version_check()
