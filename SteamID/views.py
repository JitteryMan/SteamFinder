from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from keys import STEAM_API_KEY
from .forms import FormID
from .models import User
from .steam_api import get_steamid_from_url, SteamAPI
from .steam_user import SteamUserAdv


def index(request):
    sid = request.GET.get('steam_id')
    if sid:
        if not sid.isnumeric():
            user = User.objects.get(url=sid)
            if user:
                sid = user.steam_id
            else:
                sid = get_steamid_from_url(sid)
        return HttpResponseRedirect(reverse('SteamID:user_detail', args=(sid, )))
    else:
        return render(request, 'SteamID/HomePage.html', {'forms': FormID})


def user_detail(request, steam_id):
    user = None
    if steam_id.isnumeric():
        steam = SteamAPI(TOKEN=STEAM_API_KEY)
        user = SteamUserAdv(steam.get_users_with_bans(steam_id)[0])
        if user.visibility == 3:
            user.set_badges(steam.get_badges(steam_id))
            user.friends_all(steam.get_friends_as_users(steam_id))
            user.set_games(steam.get_owned_games(steam_id))
    return render(request, 'SteamID/user-details.html', {'user': user})
