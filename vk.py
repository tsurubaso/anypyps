import requests

ACCESS_TOKEN = ''
OWNER_ID ='2'''  # Sans le signe "-"

MESSAGE = '📝 Nouveau post automatique sur mon mur perso !'
API_VERSION = '5.199'

url = 'https://api.vk.com/method/wall.post'

params = {
    'owner_id': OWNER_ID,
    'message': MESSAGE,
    'access_token': ACCESS_TOKEN,
    'v': API_VERSION
}

response = requests.post(url, params=params)
print(response.json())