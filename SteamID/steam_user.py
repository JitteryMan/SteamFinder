from datetime import datetime


def unix_to_default(unix_date):
    return datetime.utcfromtimestamp(unix_date) if unix_date else '-'


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
        # todo поскольку это базовый класс, то может и его записывать в БД, хз

    def __str__(self):
        return self.nick

    def get_status(self):
        state = ('Offline', 'Online', 'Busy', 'Away', 'Snooze', 'looking to trade', 'looking to play')
        return state[self.state]

    def get_visibility(self):
        state = ('-', 'Private', 'Friends only', 'Public')
        return state[self.visibility]


class FriendUser(SteamUser):
    def set_relationship(self, relationship: str):
        self.relationship = relationship

    def set_friend_date(self, date_friend):
        self.friend_date = unix_to_default(date_friend)


class SteamUserAdv(SteamUser):
    def friends_all(self, friends: dict):
        self.friends = []
        for friend in friends:
            friend_user = FriendUser(friend.get('details'))
            friend_user.set_relationship(friend.get('relationship'))
            friend_user.set_friend_date(friend.get('friend_since'))
            self.friends.append(friend_user)

    def set_badges(self, badges):
        self.badges = badges.get('response').get('badges')
        self.level = badges.get('response').get('player_level')
        self.need_xp = badges.get('response').get('player_xp_needed_to_level_up')
        self.xp = badges.get('response').get('player_xp')
        self.xp_curr_lvl = badges.get('response').get('player_xp_needed_current_level')
        self.progress_max = self.xp + self.need_xp - self.xp_curr_lvl
        self.progress_curr = self.xp - self.xp_curr_lvl





