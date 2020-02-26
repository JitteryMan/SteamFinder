from idlelib.searchengine import get

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import FormID
from .from_valve import get_steamid_from_url, get_adv_user



def index(request):
    # user = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids=76561198217904428')
    # friends = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&relationship=friend')
    # games = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&format=json')

    # game = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={STEAM_API_KEY}&appid=550')
    #game = requests.get(f' http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&format=json')
    # return HttpResponse(f'{timezone.now()}<br><br>{user.json()}<br><br>{friends.json()}<br><br>{games.json()}<br><br>{game.json()}')
    #https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=CD3C5D9B5084B5DD80FF0731E1C863AE&steamid=76561198217904428&include_appinfo=true&include_played_free_games=true
    sid = request.GET.get('steam_id')
    if sid:
        if not sid.isnumeric():
            sid = get_steamid_from_url(sid)
        return HttpResponseRedirect(reverse('SteamID:user_detail', args=(sid, )))
    else:
        return render(request, 'SteamID/HomePage.html', {'forms': FormID})


def user_detail(request, steam_id):
    # todo request, next: create User class, write to DB
    user = get_adv_user(steam_id) if steam_id != 'Not-found' else None
    print(user)
    return render(request, 'SteamID/user-details.html', {'user': user})
