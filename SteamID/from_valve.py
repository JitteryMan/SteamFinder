from keys import STEAM_API_KEY
import requests
import re
from requests.exceptions import HTTPError
from .steam_user import SteamUserAdv

API_URL = 'http://api.steampowered.com/'


def _get_json(query: str):
    response = {}
    try:
        response = requests.get(API_URL+query)
    except HTTPError as err:
        print(f'Error {err}')
    return response.json()


def get_steamid_from_url(url: str):
    """ FIND STEAMID FROM HTML PAGE AND RETURN IT """
    try:
        response = requests.get(url)
        res = re.search(r'(?<="steamid":")[0-9]+', response.text)
    except HTTPError as err:
        print(f'Error {err}')
    return res.group(0) if res else 'Not-found'


def get_users(steamids: str):
    query = f'ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamids}'
    response = _get_json(query)
    users = []
    if response['response']['players']:
        users = [player for player in response.get('response').get('players')]
    return users


def get_friends(steamid: str):
    query = f'ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid={steamid}&relationship=all'
    # get friends steam ids
    friends = _get_json(query)
    if friends['friendslist']['friends']:
        steamids = [f.get('steamid') for f in friends['friendslist']['friends']]
        # divide friends into parts of hundred in stack
        stacks = [steamids[i:i + 100] for i in range(0, len(steamids), 100)]
        # get friends detail and write it in user_stack
        users_stack = []
        for stack in stacks:
            users_stack.append(get_users(','.join(stack)))
        # convert back to friends
        b = [y for x in users_stack for y in x]
        for friend in friends.get('friendslist').get('friends'):
            friend['details'] = next(t for t in b if t.get('steamid') == friend['steamid'])
        return friends['friendslist']['friends']
    else:
        return None


def get_bans(steamid: str):
    pass


def get_adv_user(steamid: str):
    user = get_users(steamid)
    if user:
        c_user = SteamUserAdv(user[0])
        query = f'IPlayerService/GetBadges/v1/?key={STEAM_API_KEY}&steamid={steamid}'
        c_user.set_badges(_get_json(query))
        c_user.friends_all(get_friends(steamid))
        return c_user
    else:
        return None
