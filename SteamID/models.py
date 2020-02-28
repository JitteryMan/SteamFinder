from django.db import models


class User(models.Model):
    steam_id = models.CharField('Steam ID', unique=True, editable=False, max_length=20)
    nick = models.CharField('Nickname', max_length=500, null=True)
    url = models.URLField('Page', null=True)
    avatar_logo = models.URLField('Icon', null=True)
    avatar = models.URLField('Avatar', null=True)
    comment = models.IntegerField('Can comment', null=True)
    realname = models.CharField('Real name', max_length=500, null=True)
    created = models.DateTimeField('Created', null=True)
    country = models.CharField('Country', max_length=2, null=True)
    # BANS
    ban_community = models.BooleanField('Ban community', null=True)
    ban_VAC = models.BooleanField('VAC ban', null=True)
    ban_VAC_count = models.PositiveIntegerField('VAC bans', null=True)
    ban_games = models.PositiveIntegerField('Games ban', null=True)
    ban_economy = models.CharField('Ban economy', max_length=500, null=True)

    def __str__(self):
        return self.nick

    class Meta:
        verbose_name = 'Steam user'
        verbose_name_plural = 'Steam users'


