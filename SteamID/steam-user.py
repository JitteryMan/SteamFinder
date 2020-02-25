from keys import STEAM_API_KEY
import requests
from datetime import datetime


class User:
    def __init__(self, steam_data: dict):
        # PUBLIC DATA
        # steam id
        self.steam_id = steam_data.get('steamid')
        # steam nickname
        self.nick = steam_data.get('personaname')
        # steam URL user
        self.url = steam_data.get('profileurl')
        # steam avatar
        self.avatar = steam_data.get('avatarfull')
        # steam user state
        self.state = steam_data.get('personastate')
        # steam user last logoff
        self.logoff = steam_data.get('lastlogoff')
        # can comment this user
        self.comment = steam_data.get('commentpermission')
        # PRIVATE DATA
        # steam user real name
        self.realname = steam_data.get('realname')
        # steam user clan id
        self.clanid = steam_data.get('primaryclanid')
        # steam user create time (unix)
        self.created = steam_data.get('timecreated')
        # get game_id if user in game
        self.in_game = steam_data.get('gameid')
        # server ip if user game online
        self.serverip = steam_data.get('gameserverip')
        # get data from game, if user in game
        self.in_game_info = steam_data.get('gameextrainfo')
        # get country (2 letters ISO code)
        self.country = steam_data.get('loccountrycode')

    def get_logoff(self):
        return datetime.utcfromtimestamp(self.logoff)

    def get_created(self):
        return datetime.utcfromtimestamp(self.created)

    def get_status(self):
        state = ('Offline', 'Online', 'Busy', 'Away', 'Snooze', 'looking to trade', 'looking to play')
        return state[self.state]





