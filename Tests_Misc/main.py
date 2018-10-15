import os
import requests
import subprocess
import fnmatch

plx_api = 'https://plex.tv/api/downloads/1.json'  # plex API returns JSON with downloads
data = requests.get(plx_api).json()  # pulls in the JSON response from plex


def vers_check():
    linux_64_v = data['computer']['Linux']['version']  # specifically nabs the Linux x64 version
    with open('/home/bukarubonzai/plxupdater/vers/vercheck.txt', 'r') as check:
        cur_vers = check.readline()
    newvers = linux_64_v
    if newvers != cur_vers:
        with open('/home/bukarubonzai/plxupdater/vers/vercheck.txt', 'w') as update:
            update.write(newvers)
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
            logent.write('Updating, new version' + newvers)
        bkup()
    else:
        print('current:' + cur_vers)
        print('new:' + newvers)
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
            logent.write('New version not found - no update today bud.')
        exit()


def bkup():
    if os.path.isdir("/home/bukarubonzai/plxbkup"):
        subprocess.check_call(['rm', '-r', '/home/bukarubonzai/plxbkup/'])
        subprocess.check_call(['mkdir', '/home/bukarubonzai/plxbkup'])
        subprocess.check_call(['service', 'plexmediaserver', 'stop'])
        subprocess.check_call(['cp', '-uRfv', '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/',
                               '/home/bukarubonzai/plxbkup'])
        subprocess.check_call(['service', 'plexmediaserver', 'start'])
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
            logent.write('Backup Successful')
        install()
    else:
        subprocess.check_call(['mkdir', '/home/bukarubonzai/plxbkup'])
        subprocess.check_call(['service', 'plexmediaserver', 'stop'])
        subprocess.check_call(['cp', '-Rvf', '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/',
                               '/home/bukarubonzai/plxbkup'])
        subprocess.check_call(['service', 'plexmediaserver', 'start'])
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
            logent.write('Backup Successful')
        install()


def install():
    linux_64 = data['computer']['Linux']['releases'][0]  # specifically nabs the Linux x64 response
    download_url = linux_64['url']  # against build to make sure it's the right one.
    if linux_64['build'] == 'linux-ubuntu-x86_64':  # Grabs DL link from the Linux x64 response, checks
        subprocess.check_call(['wget', download_url])  # downloads current version
        for file in os.listdir('/home/bukarubonzai/'):  # locates the file name of the downloaded file
            if fnmatch.fnmatch(file, '*.deb'):
                fname = file
        subprocess.check_call('dpkg', '-i', fname)  # installs new version
        subprocess.check_call(['rm', '-f', fname])  # removes file after installation
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
            logent.write('New Version Installed Successfully')
    else:
        with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as bdlog:
            bdlog.write('build mismatch - was not linux-ubuntu-x86_64, must make sure the download version is correct')
        exit()


vers_check()
