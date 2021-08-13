import	json
import	pickle
import	random
import	requests
from	django.conf			import settings

class	Data:

	def	get(self):
		self.api_key = settings.API_KEY
		self.moviedex = []
		self.movielist = []
		for name in settings.MOVIES:
			response = requests.get(
				"https://www.omdbapi.com/?apikey=" +
				self.api_key +
				"&t=" +
				name +
				"&plot=short&r=json")
			self.movielist.append(json.loads(response.text))
		self._dic = {
			"Moviedex": self.moviedex,
			"Movies": self.movielist}
		return	self._dic

	def	getMoviesById(self, _arr):
		self.api_key = settings.API_KEY
		self.moviedex = []
		self.movielist = []
		for idnx in _arr:
			response = requests.get(
				"https://www.omdbapi.com/?apikey=" +
				self.api_key +
				"&i=" +
				idnx +
				"&plot=short&r=json")
			self.movielist.append(json.loads(response.text))
		self._dic = {
			"Moviedex": self.moviedex,
			"Movies": self.movielist}
		return	self._dic

	def	get_random_movie(self):
		_obj = self.get()
		_mov = _obj['Movies']
		_dex = _obj['Moviedex']
		while len(_dex) < len(_mov):
			_var = random.choice(_mov)
			_cnt = 0
			for _idx in _dex:
				if _dex[_idx]['Title'] == _var['Title']:
					_cnt += 1
			if _cnt == 0:
				return	_var
		
	def	get_movie(self, name):
		_obj = self.get()['Movies']
		for _itm in _obj:
			if _itm['Title'] == name:
				return	_itm
		
	def	get_movie_by_id(self, mvid):
		_obj = self.get()['Movies']
		for _itm in _obj:
			if _itm['imdbID'] == mvid:
				return	_itm