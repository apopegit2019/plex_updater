import requests

plurl = 'https://plex.tv/users/sign_in.json'

plhead = {'X-Plex-Client-Identifier': 'test',
          'X-Plex-Product': 'test 888999666444',
          'X-Plex-Version': '1.0'}

userid = 'user'
passwd = 'password'

result = requests.post(plurl, data='user%5Blogin%5D=' + userid + '&user%5Bpassword%5D=' + passwd, headers=plhead).json()

print(result)
