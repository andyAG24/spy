from urllib.parse import urlencode, urljoin
import requests
from tqdm import tqdm
import sys
import time

start_time = time.time()
# progress_bar = ['\\', '|', '/', '—']
progress_bar = ['.', '..', '...', '..']

APP_ID = 6775368
AUTH_URL = 'https://oauth.vk.com/authorize?'

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

service_token = 'fc722e7afc722e7afc722e7acbfc154c32ffc72fc722e7aa07870048263346b0c441e79'

auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'response_type': 'token',
    'scope': 'status, friends',
    'v': '5.92' 
}

params = {
    'access_token': token,
    'v': '5.92' 
}

class User:
    def __init__(self, token):
        self.token = token

    def getFriends(self):
        params = {
            'access_token': token,
            'v': 5.92
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()

    def getGroups(self):
        params = {
            'access_token': token,
            'user_id': user_id,
            'v': 5.92
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        return response.json()

    def isMember(self, group_id, user_ids):
        params = {
            'access_token': service_token,
            'group_id': group_id,
            'user_ids': user_ids,
            'v': 5.92
        }
        response = requests.get('https://api.vk.com/method/groups.isMember', params)
        return response.json()

    def getSecretGroups(self):
        groups_list = self.getGroups()['response']['items']
        user_ids = self.getFriends()['response']['items']
        # group_id = 8564
        isMember_list = list()
        i = 0
        while i < len(groups_list):
            # group_id = groups_list[i]
            k = 0
            while k < len(user_ids):
                member = self.isMember(groups_list[i], user_ids[k])
                isMember_list.append(str(self.isMember(groups_list[i], user_ids[k])))
                isMember_list.append('________________________________________________________________')
                print('Прошло времени: {} сек.'.format(time.time() - start_time))
                k += 1
            i += 1
        return isMember_list
        # return self.isMember(group_id, user_ids)


if __name__ == "__main__":
    user_id = 171691064

    user = User(token)
    user.getGroups()
    # print(user.getGroups()['response']['items'] )
    # print(user.getSecretGroups())
    # print(user.getFriends())

    f = open('groups.txt', 'w')
    f.write(str(user.getSecretGroups()))
    print('Готово! - прошло {} сек.'.format(time.time() - start_time))
    f.close()