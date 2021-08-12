import	psycopg2
from	django.http				import	HttpResponse, HttpRequest
from	django.shortcuts		import	render, redirect
from	django.conf				import	settings

DEF_TABLE = "ex02_movies"

def		init(request):
		try:
			_con = psycopg2.connect(
				dbname=settings.DATABASES['default']['NAME'],
				user=settings.DATABASES['default']['USER'],
				password=settings.DATABASES['default']['PASSWORD'],
				host=settings.DATABASES['default']['HOST'],
				port=settings.DATABASES['default']['PORT'],
			)
			_sql = """
				CREATE	TABLE		{TABLE}(
					title			VARCHAR(64)		UNIQUE NOT NULL,
					episode_nb		INT				PRIMARY KEY,
					opening_crawl	TEXT,
					director		VARCHAR(32)		NOT NULL,
					producer		VARCHAR(128)	NOT NULL,
					release_date	DATE			NOT NULL
				);
				""".format(TABLE=DEF_TABLE)
			with _con.cursor() as _cur:
				_cur.execute(_sql)
				_cur.execute("commit")
			return	HttpResponse("OK")
		except Exception as _exc:
			return	HttpResponse(_exc)

def		populate(request):
		try:
			_con = psycopg2.connect(
				dbname=settings.DATABASES['default']['NAME'],
				user=settings.DATABASES['default']['USER'],
				password=settings.DATABASES['default']['PASSWORD'],
				host=settings.DATABASES['default']['HOST'],
				port=settings.DATABASES['default']['PORT'],
			)
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
			_sql = """
				INSERT	INTO {TABLE}
				(
					episode_nb,
					title,
					director,
					producer,
					release_date
				)
				VALUES
				(
					%s, %s, %s, %s, %s
				)
				""".format(TABLE=DEF_TABLE)
			_rst = []
			with _con.cursor() as _cur:
				for _mov in _mvs:
					try:
						_cur.execute(_sql, [
							_mov['episode_nb'],
							_mov['title'],
							_mov['director'],
							_mov['producer'],
							_mov['release_date'],
						])
						_rst.append("OK")
						_con.commit()
					except psycopg2.DatabaseError as _exc:
						_con.rollback()
						_rst.append(_exc)
			return	HttpResponse("<br/>".join(str(_idx) for _idx in _rst))
		except Exception as _exc:
			return	HttpResponse(_exc)

def		display(request):
		try:
			_con = psycopg2.connect(
				dbname=settings.DATABASES['default']['NAME'],
				user=settings.DATABASES['default']['USER'],
				password=settings.DATABASES['default']['PASSWORD'],
				host=settings.DATABASES['default']['HOST'],
				port=settings.DATABASES['default']['PORT'],
			)
			_sql = """
				SELECT * FROM {TABLE};
				""".format(TABLE=DEF_TABLE)
			with _con.cursor() as _cur:
				_cur.execute(_sql)
				_mvs = _cur.fetchall()
			return	render(request, 'ex02/display.html', {"movies": _mvs})
		except Exception as _exc:
			return	HttpResponse("No data available")