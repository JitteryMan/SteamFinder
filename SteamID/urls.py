from django.urls import path
from .views import index

app_name = 'SteamID'
urlpatterns = [
    path('', index, name='index'),
]
