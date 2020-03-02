from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from keys import STEAM_API_KEY
from .models import User
from .steam_api import get_steamid_from_url, SteamAPI
from .steam_user import SteamUserAdv


def index(request):
    return render(request, 'SteamID/HomePage.html')


def search(request, find):
    if 'steam' in request.GET:
        find = request.GET.get('steam')
        if not find.isnumeric():
            user = User.objects.filter(url=find)
            find = user[0].steam_id if user else get_steamid_from_url(find.lower())
    if find and find.isnumeric():
        return HttpResponseRedirect(reverse('SteamID:user_detail', args=(find,)))
    else:
        return render(request, 'SteamID/Error-page.html')


def user_detail(request, steam_id):
    user = None
    if type(steam_id) == int:
        steam = SteamAPI(TOKEN=STEAM_API_KEY)
        bans = steam.get_users_with_bans(steam_id)
        if bans:
            user = SteamUserAdv(bans[0])
            if user.visibility == 3:
                user.set_badges(steam.get_badges(steam_id))
                user.friends_all(steam.get_friends_as_users(steam_id))
                user.set_games(steam.get_owned_games(steam_id))
        else:
            return render(request, 'SteamID/Error-page.html')
    return render(request, 'SteamID/user-details.html', {'user': user})
