from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import FormID
from .from_valve import get_user


def index(request):
    # user = requests.get(f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids=76561198217904428')
    # friends = requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&relationship=friend')
    # games = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&format=json')

    # game = requests.get(f'http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key={STEAM_API_KEY}&appid=550')
    #game = requests.get(f' http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={STEAM_API_KEY}&steamid=76561198217904428&format=json')
    # return HttpResponse(f'{timezone.now()}<br><br>{user.json()}<br><br>{friends.json()}<br><br>{games.json()}<br><br>{game.json()}')
    if request.GET.get('steam_id'):
        return HttpResponseRedirect(reverse('SteamID:user_detail', args=(request.GET.get('steam_id'), )))
    else:
        return render(request, 'SteamID/HomePage.html', {'forms': FormID})


def user_detail(request, steam_id):
    # todo request, next: create User class, write to DB
    user = get_user(steam_id)
    return render(request, 'SteamID/user-details.html', {'user': user})
