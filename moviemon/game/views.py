import	os
import	random
from	django.shortcuts	import get_object_or_404, render, redirect
from	django.http			import HttpResponse, HttpResponseRedirect
from	django.conf			import settings
from	.models				import Movie
from	.api				import Data
from	.view_util			import *


_dts	= DataStorage()

def	index(request):
	settings.INDEX = 0
	if request.method == "GET":
		_btn = request.GET.get('button')
		if _btn:
			if (_btn == "A"):
				_dts = DataStorage()
				_dts.load_default_settings()
				_dts.dump()
				return HttpResponseRedirect("worldmap/")
			elif (_btn == "B"):
				return HttpResponseRedirect("/options/load_game/")
	return render(request, "title.html", {
		"buttons": {
			"a": {"text": "New Game"},
			"b": {"text": "Load"}
		}
	})

def	worldMap(request):
	_dts.load()
	_pos = _dts.getPositionPlayer()
	_po2 = {}
	_btn = request.GET.get('button', '')
	if _btn:
		if _btn == "up" and _pos[1] > -101:
			_pos[1] -= 10
		elif _btn == "down" and _pos[1] < 200:
			_pos[1] += 10
		elif _btn == "left" and _pos[0] < 470:
			_pos[0] += 12
		elif _btn == "right" and _pos[0] > -350:
			_pos[0] -= 12
		elif _btn == "select":
			return redirect("../moviedex")
		elif _btn == "start":
			return redirect("../options")
		elif _btn == "b":
			settings.TOKEN = ''
	settings.TOKEN = ''
	if _pos[0] and settings.DEFAULT_GAME_SIZE > 0:
		_po2["x"] = _pos[0]
	else:
		_po2["x"] = 0
	if _pos[1] and settings.DEFAULT_GAME_SIZE > 0:
		_po2["y"] = _pos[1]
	else:
		_po2["y"] = 0
	_obj = {"position": _po2}
	_mov = {}
	if random.randrange(100) < 30:
		_mov = _dts.get_random_movie()
	if _mov:
		_tok = "tokenid123"
		settings.TOKEN = _tok
		_obj["moviemon"] = _mov
		_btl = "../battle/" + _mov["imdbID"] + "?tokenid=" + _tok
		_obj["buttons"] = {"a": {"link": _btl}}
	_bal = False
	if not _mov and random.randrange(100) < 25:
		_bal = True
	if _mov: 
		_obj["movieball"] = True
		_dts.addAmountMovieBall()
	_scr = {}
	_scr["movieballs"] = settings.BALLS
	_scr["moviemons_left"] = len(settings.MOVIES)
	_scr["moviemons_totla"] = settings.SIZE_MOVIE
	_obj["screen_data"] = _scr
	return	render(request, "worldMap.html", _obj)

def	battle(request, moviemon_id):
	_obj = {}
	_obj["server_token"] = settings.TOKEN
	_obj["request_token"] = request.GET.get('tokenid')
	if settings.TOKEN == request.GET.get('tokenid'):
		_dts.load()
		_ini = Data()
		_dat = _ini.get_movie_by_id(moviemon_id)
		_obj["movie"] = _dat
		_btn = request.GET.get('button', '')
		if _btn == 'a':
			if settings.BALLS > 0:
				_tm1 = _dat["imdbRating"] or 5.2
				_tm2 = int(float(_tm1))
				_dts.removeAmountMovieBall()
				_dts.dump()
				_pst = _dts.get_strength()
				_chr = 50 -  _tm2 * 100 + _pst * 5
				if _chr <= 1:
					_chr = 1
				if _chr >= 90:
					_chr = 90
				if random.randrange(10) < _chr:
					_obj["win"] = True
					_dts.addListMovieId(_dat["imdbID"])
					settings.MOVIES.remove(_dat["Title"])
					_dts.dump()
		_scr = {}
		_scr["movieballs"] = settings.BALLS
		_scr["moviemons_left"]	= len(settings.MOVIES)
		_scr["moviemons_right"]	= settings.SIZE_MOVIE
		_obj["screen_data"] = _scr
		_tok = "tokenid" + str(random.randrange(9000, 100500))
		settings.TOKEN = _tok
		_url = "../battle/" + _dat["imdbID"] + "?tokenid=" + _tok + "&button=a"
		_obj["buttons"] = {"a": {"link": _url}, "b": {"link": "../worldmap"}}
		_obj["newtoken"] = _tok
		return	render(request, "battle.html", _obj)
	else:
		return	redirect("..")

def	options(request):
	settings.INDEX = 0
	_prm = {
		"buttons": {
			"a": {"text": "Save"},
			"b": {"text": "Quite"},
			"start": {"text": "Cancel"}
		},
	}
	if request.method == "GET":
		_btn = request.GET.get('button')
		if _btn:
			if _btn == "A":
				return	HttpResponseRedirect("/options/save_game/")
			elif _btn == "B":
				return	HttpResponseRedirect("/")
			elif _btn == "start":
				return	HttpResponseRedirect("/worldmap/")
	return	render(request, "options.html", _prm)

def	saveGame(request):
	_prm = {
		"slots": [
			{"name": "slotA",  "status": "Free"},
			{"name": "slotB",  "status": "Free"},
			{"name": "slotC",  "status": "Free"},
		],
		"buttons": {
			"a": {"text": "Save"},
			"b": {"text": "Cancel"},
		},
		"menuItem": 0
	}
	_pth = init_slot(_prm)
	menuItem = 0
	if request.method == "GET":
		_btn = request.GET.get('button')
		if _btn:
			if _btn == "A":
				save_game_file(_pth)
				init_slot(_prm)
				menuItem = 0
				settings.INDEX = 0
				_prm["menuItem"] = menuItem
				return	render(request, "saveGame.html", _prm)
			elif _btn == "B":
				settings.INDEX = 0
				return	HttpResponseRedirect("/options/")
			elif _btn == "up":
				menuItem = (settings.INDEX - 1) % 3
			elif _btn == "down":
				menuItem = (settings.INDEX + 1) % 3
	settings.INDEX = menuItem
	_prm["menuItem"] = menuItem
	return	render(request, "saveGame.html", _prm)

def	loadGame(request):
	_prm = {
		"slots": [
			{"name": "slotA",  "status": "Free"},
			{"name": "slotB",  "status": "Free"},
			{"name": "slotC",  "status": "Free"},
		],
		"buttons": {
			"a": {"text": "Load"},
			"b": {"text": "Cancel"},
		},
		"menuItem": 0
	}
	_pth = init_slot(_prm)
	menuItem = 0
	if request.method == "GET":
		_btn = request.GET.get('button')
		if _btn:
			if _btn == "A":
				if settings.LOAD_FLAG == 1:
					settings.LOAD_FLAG = 0
					_dts = DataStorage()
					_dic = _dts.load()
					_tmp = _dic["listMovieId"]
					_idx = 0
					for _mov in _tmp:
						if settings.MOVIES == _mov:
							settings.MOVIES.pop(_idx)
						_idx += 1
					return	HttpResponseRedirect("/worldmap/")
				else:
					_bol = load_progress(_prm, _pth)
					if _bol == True:
						settings.LOAD_FLAG = 1
					else:
						settings.LOAD_FLAG = 0
						_prm["menuItem"] = 0
						settings.INDEX = 0
					return	render(request, "loadGame.html", _prm)
			elif _btn == "B":
				settings.LOAD_FLAG = 0
				return	HttpResponseRedirect("/")
			elif _btn == "up":
				menuItem = (settings.INDEX - 1) % 3
			elif (_btn == "down"):
				menuItem = (settings.INDEX + 1) % 3
	settings.INDEX = menuItem
	_prm["menuItem"] = menuItem
	return	render(request, "saveGame.html", _prm)

def	detail(request, moviemon_id):
	_mov = _dts.getMoviesById()['Movies']
	_dat = _mov[0]
	if request.method == "GET":
		_btn = request.GET.get('button')
		if _btn:
			if _btn == "B":
				return	redirect("../moviedex/")
		_viw = {"movie": _dat}
		return	render(request, "detail.html", _viw)

def	moviedex(request):
	_dtt = _dts
	_mov = _dtt.getMoviesById()['Movies']
	menuItem = 0
	_btn = request.GET.get('button', '')
	if _btn:
		if _btn == "select":
			return	redirect("../worldmap/")
		elif len(_mov):
			if _btn == "A":
				menuItem = _dts.getMenuItem()
				return	redirect("../moviedex/" + _mov[menuItem]['imdbID'])
			elif _btn == "up":
				menuItem = settings.INDEX - 1 % len(_mov)
			elif _btn == "down":
				menuItem = settings.INDEX + 1 % len(_mov)
	settings.INDEX = menuItem
	_viw = {"movies": _mov, "menuItem": menuItem}
	return	render(request, "moviedex.html", _viw)

def	randomMovie(request):
	_ini = Data()
	_dat = _ini.get_random_movie()
	_viw = {"movie": _dat}
	return	render(request, "detail.html", _viw)