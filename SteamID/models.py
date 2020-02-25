from django.db import models


class User(models.Model):
    steam_id = models.CharField(max_length=17, unique=True)
    steam_url = models.SlugField()
    steam_nick = models.TextField()

    def __str__(self):
        return self.steam_nick

    class Meta:
        verbose_name = 'Steam user'
        verbose_name_plural = 'Steam users'
