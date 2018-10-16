import requests
import os
import re
import subprocess
import time


def logging(message):  # Simple log file with time/date stamps
    with open('/home/bukarubonzai/plexfiles2/updater/logs/plex_update.log', 'a+') as log:
        log.write('%s %s \n' % (time.ctime(), message))


def version_check(): # decides whether a new version is available.
    with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'r') as curver: # current version release epoch
        curvers = curver.readline() # reads the epoch date from the file to compare to the API
    plx_api = 'https://plex.tv/api/downloads/1.json?channel=plexpass'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    nversdate = data['computer']['Linux']['release_date'] # pulls the API advertised epoch date for new version
    nvers = data['computer']['Linux']['version'] # pulls actual version number
    if nversdate > curvers: # compares epoch from API to the one for the current version
        logging('New Version Found %s' % nvers) # adds new version to the log
        with open('/home/bukarubonzai/plexfiles2/updater/vercur.txt', 'w') as new:
            new.write(nversdate) # updating current version with new version epoch date
        get_download(data) # move to download installation file
    else:
        logging('No Update Required.')
        exit()


def get_download(data): # grab download installation file
    installDir = '/home/bukarubonzai/plexfiles2/updater/' # directory where the file will be downloaded
    linux_64 = data['computer']['Linux']['releases'][0]  # specifically nabs the Ubuntu 64 bit part of json response
    download_url = linux_64['url']  # just saving the URL to a variable for simplicity later
    if linux_64['build'] == 'linux-ubuntu-x86_64':  # Checks to make sure I did, in fact, get Ubuntu 64 bit
        os.chdir(installDir) # move to the installation directory
        logging('Download Starting: %s' % download_url)
        subprocess.check_call(['wget', download_url])  # downloads current version
    install(download_url, installDir) # moving to installation


def install(download_url, installDir):
    pattern = re.compile(r'(plexmediaserver.*)') # pattern to find file name from download URL
    fileName = pattern.findall(download_url) # pulls the file name out of the URL
    filepath = os.path.join(installDir, fileName[0]) # creates the file path to the installation file
    if os.path.isfile(filepath): # make sure there's a file there
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
