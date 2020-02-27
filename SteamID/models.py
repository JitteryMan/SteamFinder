from datetime import datetime
from django.db import models
from .steam_api import SteamAPI
from keys import STEAM_API_KEY


class User(models.Model):
    steam_id = models.CharField('Steam ID', unique=True, editable=False, max_length=20)
    nick = models.CharField('Nickname', max_length=500, null=True)
    url = models.URLField('Page', null=True)
    avatar_logo = models.URLField('Icon', null=True)
    avatar = models.URLField('Avatar', null=True)
    state = models.PositiveSmallIntegerField('Status', null=True)
    logoff = models.DateTimeField('Last seen', null=True)
    comment = models.IntegerField('Can comment', null=True)
    realname = models.CharField('Real name', max_length=500, null=True)
    created = models.DateTimeField('Created', null=True)
    in_game = models.CharField('Game', max_length=500, null=True)
    country = models.CharField('Country', max_length=2, null=True)
    # BANS
    ban_community = models.BooleanField('Ban community')
    ban_VAC = models.BooleanField('VAC ban')
    ban_VAC_count = models.PositiveIntegerField('VAC bans')
    ban_last_day = models.PositiveIntegerField('Days last ban')
    ban_games = models.PositiveIntegerField('Games ban')
    ban_economy = models.CharField('Ban economy', max_length=500)

    def __str__(self):
        return self.nick

    def get_status(self):
        state = ('Offline', 'Online', 'Busy', 'Away', 'Snooze', 'looking to trade', 'looking to play')
        return state[self.state]

    class Meta:
        verbose_name = 'Steam user'
        verbose_name_plural = 'Steam users'


class Friend(models.Model):
    users = models.ManyToManyField(User)
    relationship = models.CharField('Relationship', max_length=50)
    friend_date = models.DateTimeField('Friend from')


class Advance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    player_xp = models.BigIntegerField('XP')
    player_level = models.PositiveIntegerField('Level')
    player_xp_needed_to_level_up = models.PositiveIntegerField('XP need to level up')
    player_xp_needed_current_level = models.BigIntegerField('XP current level')


class Games(models.Model):
    app_id = models.ManyToManyField(User)
    steam_app_id = models.BigIntegerField('App ID', unique=True)
    name = models.CharField('Name', max_length=500)
    play_time = models.PositiveIntegerField('Minutes in game')
    icon = models.URLField('Icon')
    logo = models.URLField('Logo')
    windows = models.PositiveIntegerField('Minutes on Windows')
    mac = models.PositiveIntegerField('Minutes on Mac')
    linux = models.PositiveIntegerField('Minutes on Linux')

    def __str__(self):
        return self.name

    def in_game(self) -> str:
        return f'{self.play_time // 60}:{self.play_time % 60}'


def unix_to_default(unix_date):
    return datetime.utcfromtimestamp(unix_date) if unix_date else None


def create_or_update_user(s_user: dict):
    user = User.objects.update_or_create(steam_id=s_user.get('steamid'), defaults={'steam_id': s_user.get('steamid'),
    'nick': s_user.get('personaname'), 'url': s_user.get('profileurl'), 'avatar_logo': s_user.get('avatar'),
    'avatar': s_user.get('avatarfull'), 'state': s_user.get('personastate'),
    'logoff': unix_to_default(s_user.get('lastlogoff')), 'comment': s_user.get('commentpermission'),
    'realname': s_user.get('realname'), 'created': unix_to_default(s_user.get('timecreated')),
    'in_game': s_user.get('gameextrainfo'), 'country': s_user.get('loccountrycode'),
    'ban_community': s_user.get('ban').get('CommunityBanned'), 'ban_VAC': s_user.get('ban').get('VACBanned'),
    'ban_VAC_count': s_user.get('ban').get('NumberOfVACBans'), 'ban_last_day': s_user.get('ban').get('DaysSinceLastBan'),
    'ban_games': s_user.get('ban').get('NumberOfGameBans'), 'ban_economy': s_user.get('ban').get('EconomyBan')})


def create_or_update_adv(badges: dict):
    adv = Advance.objects.update_or_create(user__steam_id=badges.get('response').get('steamid'), defaults={
                'player_xp': badges.get('response').get('player_xp'),
                'player_level': badges.get('response').get('player_level'),
                'player_xp_needed_to_level_up': badges.get('response').get('player_xp_needed_to_level_up'),
                'player_xp_needed_current_level': badges.get('response').get('player_xp_needed_current_level')})




def create_or_update_friends(steam_id: str):
    steam = SteamAPI(TOKEN=STEAM_API_KEY)
    users = steam.get_friends_as_users(steam_id)
    for user in users:
        create_or_update_user(user.get('details'))
        friend = Friend.objects.get_or_create(users__steam_id=steam_id, id=user.get('steamid'))
        friend.relationship = user.get('relationship')
        friend.friend_date = user.get('friend_since')
        friend.save()


def upd_user(steam_id: str):
    steam = SteamAPI(TOKEN=STEAM_API_KEY)
    user = steam.get_users_with_bans(steam_id)
    if user:
        create_or_update_user(user[0])
    badges = steam.get_badges(steam_id)
    if badges:
        badges['response']['steamid'] = steam_id
        create_or_update_adv(badges)


