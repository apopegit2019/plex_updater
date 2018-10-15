import requests
import os
import re
import json
import ast
import subprocess
import time


def logging(message):
    with open('/home/bukarubonzai/plexfiles2/updater/logs/plex_update.log', 'a+') as log:
        log.write('%s %s \n' % (time.ctime(), message))


def version_check():
    with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'r') as curver:
        curvers = curver.readline()
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    data = ast.literal_eval(json.dumps(data))
    nvers = data['computer']['Linux']['version']
    print('current version: %s new version %s' % (curvers, nvers))
    if nvers > curvers:
        logging('New Version Found %s' % nvers)
        with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'w') as new:
            new.write(nvers)
        get_download(data)
    else:
        logging('No Update Required')
        exit()


def get_download(data):
    installDir = '/home/bukarubonzai/plexfiles2/updater/'
    linux_64 = data['computer']['Linux']['releases'][0]  # specifically nabs the Linux x64 response
    download_url = linux_64['url']  # against build to make sure it's the right one.
    if linux_64['build'] == 'linux-ubuntu-x86_64':  # Grabs DL link from the Linux x64 response, checks
        os.chdir(installDir)
        logging('Download Starting: %s' % download_url)
        subprocess.check_call(['wget', download_url])  # downloads current version
    install(download_url, installDir)


def install(download_url, installDir):
    pattern = re.compile(r'(plexmediaserver.*)')
    fileName = pattern.findall(download_url)
    filepath = os.path.join(installDir, fileName[0])
    if os.path.isfile(filepath):
        logging('Installation commencing: %s' % filepath)
        try:
            subprocess.check_call(['dpkg', '-i', filepath])  # installs new version
            logging('Installation Complete')
        except Exception as ex:
            logging('Error:\n' + ex)
        try:
            os.remove(filepath)  # removes file after installation
            logging('Removing %s' % filepath)
        except Exception as rmex:
            logging('Error:\n' + rmex)
    else:
        logging('Something failed with the file path')
        exit()
    exit()


version_check()
