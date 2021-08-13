from	django.conf.urls	import url
from	.					import views

urlpatterns = [
	url(r'^worldmap/$', views.worldMap),
	url(r'^battle/(?P<moviemon_id>tt[0-9]+)?$', views.battle),
	url(r'^moviedex/$', views.moviedex),
	url(r'^moviedex/(?P<moviemon_id>tt[0-9]+)/?$', views.detail),
	url(r'^random/$', views.randomMovie),
	url(r'^options/$', views.options),
	url(r'^options/save_game/$', views.saveGame),
	url(r'^options/load_game/$', views.loadGame),
	url(r'^$', views.index, name="index"),
]