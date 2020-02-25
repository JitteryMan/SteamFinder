from keys import STEAM_API_KEY
import requests
from requests.exceptions import HTTPError
from .steam_user import SteamUser

API_URL = 'http://api.steampowered.com/'


def _get_json(query: str):
    response = {}
    try:
        response = requests.get(API_URL+query)
    except HTTPError as err:
        print(f'Error {err}')
    return response.json()


def get_user(steamid: str):
    query = f'ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamid}'
    response = _get_json(query)
    print(response)
    return SteamUser(response.get('response').get('players')[0])


def get_friends(steamid: str):
    pass


def get_bans(steamid: str):
    pass