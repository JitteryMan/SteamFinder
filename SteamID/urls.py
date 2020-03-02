from django.urls import path
from .views import index, user_detail, search

app_name = 'SteamID'
urlpatterns = [
    path('', index, name='index'),
    path('<str:find>', search, name='search'),
    path('<int:steam_id>/', user_detail, name='user_detail'),
]
