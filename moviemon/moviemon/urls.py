# from django.urls import path
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
	path('', include('game.urls')),
]
