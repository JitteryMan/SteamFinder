from django.urls import path
from .views import index, user_detail

app_name = 'SteamID'
urlpatterns = [
    path('', index, name='index'),
    path('<str:steam_id>/', user_detail, name='user_detail')
]
