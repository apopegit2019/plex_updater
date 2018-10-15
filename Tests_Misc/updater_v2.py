import requests
import re
import ast
import json
# import fnmatch
# import os
# import subprocess


def get_download():
    plx_api = 'https://plex.tv/api/downloads/1.json'  # plex API returns JSON with downloads
    data = requests.get(plx_api).json()  # pulls in the JSON response from plex
    data = ast.literal_eval(json.dumps(data))
    linux_64 = data['computer']['Linux']['releases'][0]  # specifically nabs the Linux x64 response
    download_url = linux_64['url']  # against build to make sure it's the right one.
    print(download_url)
    if download_url.endswith('.deb'):
        print('this works')
        pattern = re.compile(r'(plexmediaserver.*)')
        fileName = pattern.findall(download_url)
    else:
        print('either you suck or the files wrong')


def install():
    get_download()
    #
    # if linux_64['build'] == 'linux-ubuntu-x86_64':  # Grabs DL link from the Linux x64 response, checks
    #     subprocess.check_call(['wget', download_url])  # downloads current version
    #     for file in os.listdir('/home/bukarubonzai/'):  # locates the file name of the downloaded file
    #         if fnmatch.fnmatch(file, '*.deb'):
    #             fname = file
    #     subprocess.check_call(['dpkg', '-i', fname])  # installs new version
    #     subprocess.check_call(['rm', '-f', fname])  # removes file after installation
    #     with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as logent:
    #         logent.write('New Version Installed Successfully')
    # else:
    #     with open('/home/bukarubonzai/plxupdater/logs/log.txt', 'a') as bdlog:
    #         bdlog.write('build mismatch - was not linux-ubuntu-x86_64, must make sure the download version is correct')
    exit()


install()
