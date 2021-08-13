import	pickle
import	random
import	sys
import	os
from	django.conf	import settings
from	game.api import Data

class	DataStorage:

	def	__init__(	self,
					positionPlayer=list(),
					amountMovieBall=150,
					listMovieId=list(),
					dataMovieIMDB=None,
					menuItem=0				):
		self.positionPlayer = positionPlayer
		if len(self.positionPlayer) == 0:
			self.positionPlayer = settings.DEFAULT_START_PLAYER_POSITION
		self.amountMovieBall = amountMovieBall
		self.listMovieId = listMovieId
		self.dataMovieIMDB = dataMovieIMDB
		self.menuItem = menuItem
		settings.BALLS = amountMovieBall

	def	setPositionPlayer(self, positionPlayer):
		self.positionPlayer = positionPlayer
	def	getPositionPlayer(self):
		return	(self.positionPlayer)

	def	setAmountMovieBall(self, amountMovieBall):
		self.amountMovieBall = amountMovieBall
		settings.BALLS = amountMovieBall
	def	getAmountMovieBall(self):
		return	self.amountMovieBall

	def	setListMovieName(self, listMovieId):
		self.listMovieId = listMovieId
	
	def	getListMovieName(self):
		return	self.listMovieId

	def	getMoviesById(self):
		_dat = Data()
		_arr = self.getListMovieName()
		_rst = _dat.getMoviesById(_arr)
		return	_rst

	def	setDataMovieIMDB(self, dataMovieIMDB):
		self.dataMovieIMDB = dataMovieIMDB
	def	getDataMovieIMDB(self):
		return	self.dataMovieIMDB

	def	setMenuItem(self, index):
		self.menuItem = index
	def	getMenuItem(self):
		return	self.menuItem
	def get_movie(self):
		return (self.getDataMovieIMDB())
	def	addAmountMovieBall(self):
		self.amountMovieBall = self.amountMovieBall + 1
		settings.BALLS = settings.BALLS + 1
	def	removeAmountMovieBall(self):
		self.amountMovieBall = self.amountMovieBall - 1
		settings.BALLS = settings.BALLS - 1

	def	dump(self, filename="data.pickle"):
		_dic = {
			"positionPlayer"	:	self.getPositionPlayer(),
			"amountMovieBall"	:	self.getAmountMovieBall(),
			"listMovieId"		:	self.getListMovieName(),
			"dataMovieIMDB"		:	self.getDataMovieIMDB(),
			"menuItem"			:	self.getMenuItem()
		}
		_fil = open(filename, "wb")
		pickle.dump(_dic, _fil)
		_fil.close()

	def	load(self, filename="data.pickle"):
		_fil = open(filename, "rb")
		_dic = pickle.load(_fil)
		return	_dic

	def	load_default_settings(self):
		self.positionPlayer = settings.DEFAULT_START_PLAYER_POSITION
		self.amountMovieBall = settings.DEFAULT_AMOUNT_BALL
		self.listMovieId	= list()
		self.dataMovieIMDB	= self.load_IMDB()
		self.menuItem		= 0
	
	def	get_random_movie(self):
		_dat = Data()
		return	_dat.get_random_movie()

	def	get_movie(self, name):
		_dat = Data()
		_dat.get_movie(name)
		return	_dat

	def 	printO(self):
		print(self.positionPlayer)
		print(self.amountMovieBall)
		print(self.listMovieId)
		# print(self.dataMovieIMDB)
		
	def	get_strength(self):
		return	len(self.listMovieId) + 1
	
	def	load_IMDB(self):
		_dat = Data()
		return	_dat.get()

	def	coefBattle(self, strengthEnemy):
		_pst = self.get_strength()
		_chr = 50 - (strengthEnemy * 10) + (_pst * 5)
		if (_chr <= 1):
			return	1
		elif _chr >= 90:
			return	90
		return	_chr

	def	addListMovieId(self, listMovieId):
		self.listMovieId.append(listMovieId)
