import requests
import time
import json

start_time = time.time()

APP_ID = 6775368
token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'
service_token = 'fc722e7afc722e7afc722e7acbfc154c32ffc72fc722e7aa07870048263346b0c441e79'

class User:
    def __init__(self, token):
        self.token = token


    def get_friends(self):
        params = {
            'access_token': token,
            'v': 5.92
        }

        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()


    def get_groups(self):
        params = {
            'access_token': token,
            'user_id': user_id,
            'v': 5.92
        }

        response = requests.get('https://api.vk.com/method/groups.get', params)
        return response.json()


    def is_member(self, group_id, user_ids):
        params = {
            'access_token': service_token,
            'group_id': group_id,
            'user_ids': user_ids,
            'v': 5.92
        }

        response = requests.get('https://api.vk.com/method/groups.isMember', params)
        return response.json()


    def get_group_info(self, group_id):
        params = {
            'access_token': token,
            'group_id': group_id,
            'fields': 'members_count',
            'v': 5.61
        }

        response = requests.get('https://api.vk.com/method/groups.getById', params)
        return response.json()


    def get_secret_groups(self):
        groups_list = self.get_groups()['response']['items']
        user_ids = self.get_friends()['response']['items']
        is_member_list = list()

        index = 0
        while index < len(groups_list):  # нахождение друзей, которые есть в группе
            index_k = 0
            while index_k < len(user_ids):
                member = self.is_member(groups_list[index], user_ids[index_k]) # находится ли в данной группе друг

                if member['response'][0]['member'] == 1: # получаем список групп, в которых есть друзья 
                    is_member_list.append(groups_list[index])

                print('Прошло времени: {} сек.'.format(time.time() - start_time))
                index_k += 1
            index += 1
        groups_set = set(groups_list)  # множество групп пользователя
        is_member_set = set(is_member_list)  # множество общих групп с друзьями

        result = groups_set.difference(is_member_set)  # вычитаем из множества групп пользователя множество общих групп
        result = list(result)
        index = 0

        result_list_with_info = list()
        while index < len(result):
            group_info = self.get_group_info(result[index])
            group_info_response = group_info["response"][0]

            group_dict = dict()
            group_dict = {"name": group_info_response["name"], "gid": group_info_response["id"], "members_count":  group_info_response["members_count"]}
            
            result_list_with_info.append(group_dict)
            index += 1

        return result_list_with_info


if __name__ == "__main__":
    user_id = 171691064

    user = User(token)

    with open("groups.json", "w") as outfile:
        outfile.write(json.dumps(user.get_secret_groups()))

    print('Готово! - прошло {} сек.'.format(time.time() - start_time))


    