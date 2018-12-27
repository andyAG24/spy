from urllib.parse import urlencode, urljoin
import requests
import sys
import time

start_time = time.time()

APP_ID = 6775368
AUTH_URL = 'https://oauth.vk.com/authorize?'

token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

service_token = 'fc722e7afc722e7afc722e7acbfc154c32ffc72fc722e7aa07870048263346b0c441e79'

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

    def getGroupInfo(self, group_id):
        params = {
            'access_token': token,
            'group_id': group_id,
            'fields': 'members_count',
            'v': 5.61
        }
        response = requests.get('https://api.vk.com/method/groups.getById', params)
        return response.json()

    def getSecretGroups(self):
        groups_list = self.getGroups()['response']['items']
        user_ids = self.getFriends()['response']['items']
        isMember_list = list()
        i = 0

        while i < len(groups_list):  # нахождение друзей, которые есть в группе
            k = 0
            while k < len(user_ids):
                member = self.isMember(groups_list[i], user_ids[k]) # находится ли в данной группе друг

                if member['response'][0]['member'] == 1: # получаем список групп, в которых есть друзья 
                    isMember_list.append(groups_list[i])

                print('Прошло времени: {} сек.'.format(time.time() - start_time))
                k += 1
            i += 1
        groups_set = set(groups_list)  # множество групп пользователя
        isMember_set = set(isMember_list)  # множество общих групп с друзьями

        result = groups_set.difference(isMember_set)  # вычитаем из множества групп пользователя множество общих групп
        result = list(result)
        i = 0

        result_list_with_info = list()
        while i < len(result):
            group_info = self.getGroupInfo(result[i])

            group_dict = dict()
            group_dict = {'name': group_info['response'][0]['name'], 'gid': group_info['response'][0]['id'], 'members_count':  group_info['response'][0]['members_count'],}

            result_list_with_info.append(group_dict)
            i += 1
        return result_list_with_info


if __name__ == "__main__":
    user_id = 171691064

    user = User(token)
    user.getGroups()

    f = open('groups.json', 'w')
    f.write(str(user.getSecretGroups()))
    print('Готово! - прошло {} сек.'.format(time.time() - start_time))
    f.close()