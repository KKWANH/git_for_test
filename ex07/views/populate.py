import	psycopg2
from	django					import	db
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	render
from	..models				import	Movies

class	Populate(View):

	_mvs = [
			{	"episode_nb"	: 1,
				"title"			: "The Phantom Menace",
				"director"		: "George Lucas",
				"producer"		: "Rick McCallum",
				"release_date"	: "1999-05-19"	},
			{	"episode_nb"	: 2,
				"title"			: "Attack of the Clones",
				"director"		: "George Lucas",
				"producer"		: "Rick McCallum",
				"release_date"	: "2002-05-16"	},
			{	"episode_nb"	: 3,
				"title"			: "Revenge of the Sith",
				"director"		: "George Lucas",
				"producer"		: "Rick McCallum",
				"release_date"	: "2005-05-19"	},
			{	"episode_nb"	: 4,
				"title"			: "A New Hope",
				"director"		: "George Lucas",
				"producer"		: "Gary Kurtz, Rick McCallum",
				"release_date"	: "1977-05-25"	},
			{	"episode_nb"	: 5,
				"title"			: "The Empire Strikes Back",
				"director"		: "Irvin Kershner",
				"producer"		: "Gary Kurtz, Rick McCallum",
				"release_date"	: "1980-05-17"	},
			{	"episode_nb"	: 6,
				"title"			: "Return of the Jedi",
				"director"		: "Richard Marquand",
				"producer"		: "Howard G. Kazanjian, George Lucas, Rick McCallum",
				"release_date"	: "1983-05-25"	},
			{	"episode_nb"	: 7,
				"title"			: "The Force Awakens",
				"director"		: "J. J. Abrams",
				"producer"		: "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
				"release_date"	: "2015-12-11"	},
		]
	
	def	get(self, request):
		_rst = []
		for _mov in self._mvs:
			try:
				Movies.objects.create(
					episode_nb=_mov['episode_nb'],
					title=_mov['title'],
					director=_mov['director'],
					producer=_mov['producer'],
					release_date=_mov['release_date'],
				)
				_rst.append("OK")
			except db.Error as _exc:
				_rst.append(_exc)
		return	HttpResponse("<br/>".join(str(_idx) for _idx in _rst))