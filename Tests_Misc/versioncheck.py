import requests

plx_api = 'https://plex.tv/api/downloads/1.json'  # plex API returns JSON with downloads
data = requests.get(plx_api).json()  # pulls in the JSON response from plex


def vers_check():
    linux_64_v = data['computer']['Linux']['version']  # specifically nabs the Linux x64 version
    with open('/home/bukarubonzai/plxbkup/vers/vercheck.txt', 'r') as check:
        cur_vers = check.readline()
    newvers = linux_64_v
    if newvers > cur_vers:
        with open('/home/bukarubonzai/plxbkup/vers/vercheck.txt', 'w') as update:
            update.write(newvers)
            #bkup()
            #install()
    else:
        print('current:' + cur_vers)
        print('new:'+newvers)
        exit()

vers_check()
