import requests
import os
import re
import json
import ast
import subprocess
import time


def logging(message):  # logs activity with date/time stamp to specified directory
    with open('/home/bukarubonzai/plexfiles2/updater/logs/plex_update.log', 'a+') as log:
        log.write('%s %s \n' % (time.ctime(), message))


def version_check():
    with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'r') as curver: # file with current version epoch
        curvers = curver.readline() # grabs current version epoch date from file for comparison
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    data = ast.literal_eval(json.dumps(data)) # this to get rid of indices must be int not str error
    nvers = data['computer']['Linux']['version'] # new version
    if nvers > curvers: # if there's a new version
        logging('New Version Found %s' % nvers) # found new version
        with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'w') as new: # current version file
            new.write(nvers) # update with current version file with the new version epoch
        get_download(data) # gets' the download for the new version
    else:  # no new version
        logging('No Update Required')
        exit()


def get_download(data): # takes the json data from plex api to download the newest version
    installDir = '/home/bukarubonzai/plexfiles2/updater/' # directory where installation file is downloaded
    linux_64 = data['computer']['Linux']['releases'][0]  # specifically nabs the Linux x64 response
    download_url = linux_64['url']  # download_url
    if linux_64['build'] == 'linux-ubuntu-x86_64':  # paranoid so sanity check
        os.chdir(installDir) # moving to install directory
        logging('Download Starting: %s' % download_url)
        subprocess.check_call(['wget', download_url])  # downloads current version
    install(download_url, installDir) # moving to installation


def install(download_url, installDir):
    pattern = re.compile(r'(plexmediaserver.*)') # gets the name of the file from the download URL
    fileName = pattern.findall(download_url)
    filepath = os.path.join(installDir, fileName[0]) # create path to install file
    if os.path.isfile(filepath): # check to see that file exists
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
