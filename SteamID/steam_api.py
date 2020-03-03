# STEAM WEB API. Created by JitteryMan
import re
import requests

URL = 'http://api.steampowered.com/'
APP_MEDIA = 'http://media.steampowered.com/steamcommunity/public/images/apps/'


class SteamAPI:
    TOKEN = ''

    def __init__(self, TOKEN):
        self.TOKEN = TOKEN

    def _get_json(self, query: str) -> dict:
        response = {}
        try:
            response = requests.get(URL + query)
        except requests.exceptions.RequestException as err:
            raise err
        return response.json()

    def get_users(self, steam_ids: str) -> list:
        query = f'ISteamUser/GetPlayerSummaries/v0002/?key={self.TOKEN}&steamids={steam_ids}'
        response = self._get_json(query)
        return _return_dict(response, 'response', 'players')

    def get_bans(self, steam_ids: str) -> list:
        query = f'ISteamUser/GetPlayerBans/v1/?key={self.TOKEN}&steamids={steam_ids}'
        response = self._get_json(query)
        bans = []
        if 'players' in response:
            bans = [ban for ban in response.get('players')]
        return bans

    def get_users_with_bans(self, steam_ids: str) -> list:
        users = self.get_users(steam_ids)
        bans = self.get_bans(steam_ids)
        if users and bans:
            for user in users:
                user['ban'] = next(ban for ban in bans if ban['SteamId'] == user['steamid'])
        return users

    def get_badges(self, steam_id: str) -> dict:
        query = f'IPlayerService/GetBadges/v1/?key={self.TOKEN}&steamid={steam_id}'
        response = self._get_json(query)
        return response

    def get_friends_id(self, steam_id: str) -> list:
        query = f'ISteamUser/GetFriendList/v0001/?key={self.TOKEN}&steamid={steam_id}&relationship=all'
        response = self._get_json(query)
        return _return_dict(response, 'friendslist', 'friends')

    def get_friends_as_users(self, steam_id: str) -> list:
        friends = self.get_friends_id(steam_id)
        if friends:
            steam_ids = [friend.get('steamid') for friend in friends]
            stacks = [steam_ids[i:i + 100] for i in range(0, len(steam_ids), 100)]
            users_stack = []
            for stack in stacks:
                users_stack.append(self.get_users_with_bans(','.join(stack)))
            if users_stack:
                users = [user for piece in users_stack for user in piece]
                for friend in friends:
                    friend['details'] = next(user for user in users if user.get('steamid') == friend['steamid'])
        return friends

    def get_owned_games(self, steam_id: str) -> dict:
        query = f'''IPlayerService/GetOwnedGames/v1/?key={self.TOKEN}&steamid={steam_id
                }&include_appinfo=true&include_played_free_games=true'''
        response = self._get_json(query)
        return response.get('response').get('games')


def get_steamid_from_url(url: str):
    """ FIND STEAMID FROM HTML PAGE AND RETURN IT """
    res = None
    try:
        is_steam = re.search(r'^https://steamcommunity.com/', url)
        if is_steam:
            response = requests.get(url)
            res = re.search(r'(?<="steamid":")[0-9]+', response.text)
    except requests.exceptions.RequestException as err:
        raise err
    return res.group(0) if res else None


def _return_dict(stacks: dict, key1: str, key2: str) -> list:
    result = []
    if key1 in stacks and key2 in stacks[key1]:
        result = [stack for stack in stacks.get(key1).get(key2)]
    return result
