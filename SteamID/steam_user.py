from datetime import datetime
from .steam_api import APP_MEDIA, APP_URL
from .models import User
from django.utils.translation import gettext_lazy as _


def unix_to_default(unix_date):
    return datetime.utcfromtimestamp(unix_date) if unix_date else None


class SteamUser:
    def __init__(self, steam_data: dict):
        # PUBLIC DATA
        # steam id
        self.steam_id = steam_data.get('steamid')
        # steam nickname
        self.nick = steam_data.get('personaname')
        # steam URL user
        self.url = steam_data.get('profileurl')
        # steam avatar BIG
        self.avatar_big = steam_data.get('avatarfull')
        # steam avatar MINI
        self.avatar_mini = steam_data.get('avatar')
        # steam user state
        self.state = steam_data.get('personastate')
        # steam user last logoff
        self.logoff = unix_to_default(steam_data.get('lastlogoff'))
        # can comment this user
        self.comment = steam_data.get('commentpermission')
        # public or private
        self.visibility = steam_data.get('communityvisibilitystate')
        # PRIVATE DATA
        # steam user real name
        self.realname = steam_data.get('realname')
        # steam user clan id
        self.clanid = steam_data.get('primaryclanid')
        # steam user create time (unix)
        self.created = unix_to_default(steam_data.get('timecreated'))
        # get game_id if user in game
        self.in_game = steam_data.get('gameid')
        # server ip if user game online
        self.serverip = steam_data.get('gameserverip')
        # get data from game, if user in game
        self.in_game_info = steam_data.get('gameextrainfo')
        # get country (2 letters ISO code)
        self.country = steam_data.get('loccountrycode')
        # BANS
        self.ban_community = steam_data.get('ban').get('CommunityBanned')
        self.ban_VAC = steam_data.get('ban').get('VACBanned')
        self.ban_VAC_count = steam_data.get('ban').get('NumberOfVACBans')
        self.ban_last = steam_data.get('ban').get('DaysSinceLastBan')
        self.ban_game = steam_data.get('ban').get('NumberOfGameBans')
        self.ban_economy = steam_data.get('ban').get('EconomyBan')
        self._to_db()

    def __str__(self):
        return self.nick

    def _to_db(self):
        User.objects.update_or_create(steam_id=self.steam_id, defaults={'steam_id': self.steam_id, 'nick': self.nick,
            'url': self.url, 'avatar_logo': self.avatar_mini, 'avatar': self.avatar_big, 'comment': self.comment,
            'realname': self.realname, 'created': self.created, 'country': self.country,
            'ban_community': self.ban_community, 'ban_VAC': self.ban_VAC, 'ban_VAC_count': self.ban_VAC_count,
            'ban_games': self.ban_game, 'ban_economy': self.ban_economy})

    def get_status(self):
        state = (_('Offline'), _('Online'), _('Busy'), _('Away'), _('Snooze'), _('looking to trade'), _('looking to play'))
        return state[self.state]

    def get_visibility(self):
        state = (None, _('Private'), _('Friends only'), _('Public'))
        return state[self.visibility]

    def days_to_ymd(self):
        years = self.ban_last // 365
        month = round(self.ban_last % 365 // 30.42)
        days = round(self.ban_last % 365 % 30.42)
        s = f'{years}{_("y")} ' if years else ''
        s += f'{month}{_("m")} ' if month else ''
        s += f'{days}{_("d")}'
        return s


class FriendUser(SteamUser):
    def set_relationship(self, relationship: str):
        self.relationship = relationship

    def set_friend_date(self, date_friend):
        self.friend_date = unix_to_default(date_friend)


class SteamUserAdv(SteamUser):
    def friends_all(self, friends: list):
        self.friends = []
        if friends:
            for friend in friends:
                friend_user = FriendUser(friend.get('details'))
                friend_user.set_relationship(friend.get('relationship'))
                friend_user.set_friend_date(friend.get('friend_since'))
                self.friends.append(friend_user)
            self.friends_count = len(self.friends)
            self.friends = [self.friends[i:i + 20] for i in range(0, len(self.friends), 20)]

    def set_badges(self, badges: dict):
        self.badges = badges.get('response').get('badges')
        self.level = badges.get('response').get('player_level')
        self.need_xp = badges.get('response').get('player_xp_needed_to_level_up')
        self.xp = badges.get('response').get('player_xp')
        self.xp_curr_lvl = badges.get('response').get('player_xp_needed_current_level')
        if self.xp:
            self.progress_max = self.xp + self.need_xp


    def set_games(self, games: dict):
        self.games = []
        if games:
            games = sorted(games, key=lambda game: game['playtime_forever'], reverse=True)
            for game in games:
                self.games.append(Games(game))
            self.games_count = len(self.games)
            self.games = [self.games[i:i + 50] for i in range(0, len(self.games), 50)]


class Games:
    def __init__(self, game_info: dict):
        self.app_id = game_info.get('appid')
        self.app_name = game_info.get('name')
        self.app_play_time = self.in_game(game_info.get('playtime_forever'))
        self.app_icon = f'{APP_MEDIA}{self.app_id}/{game_info.get("img_icon_url")}.jpg'
        self.app_logo = f'{APP_MEDIA}{self.app_id}/{game_info.get("img_logo_url")}.jpg'
        self.app_url = f'{APP_URL}{self.app_id}'
        self.app_visible = game_info.get('has_community_visible_stats')
        self.app_windows = self.in_game(game_info.get('playtime_windows_forever'))
        self.app_mac = self.in_game(game_info.get('playtime_mac_forever'))
        self.app_linux = self.in_game(game_info.get('playtime_linux_forever'))

    @staticmethod
    def in_game(minutes: int) -> str:
        s = f'{(minutes // 60)}{_("h")} ' if minutes // 60 > 0 else ''
        s += f'{(minutes % 60)}{_("m")}'
        return s


