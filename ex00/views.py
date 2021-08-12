import	psycopg2
from	django.http				import	HttpResponse, HttpRequest
from	django.shortcuts		import	render, redirect
from	django.conf				import	settings

def		init(request):
		try:
			_con = psycopg2.connect(
				dbname=settings.DATABASES['default']['NAME'],
				user=settings.DATABASES['default']['USER'],
				password=settings.DATABASES['default']['PASSWORD'],
				host=settings.DATABASES['default']['HOST'],
				port=settings.DATABASES['default']['PORT'],
			)
			with _con.cursor() as _cur:
				_cur.execute("""
					CREATE	TABLE		ex00_movies(
						title			VARCHAR(64)		UNIQUE NOT NULL,
						episode_nb		INT				PRIMARY KEY,
						opening_crawl	TEXT,
						director		VARCHAR(32)		NOT NULL,
						producer		VARCHAR(128)	NOT NULL,
						release_date	DATE			NOT NULL
					);
				""")
				_cur.execute('commit')
			return	HttpResponse("OK")
		except Exception as _exc:
			return	HttpResponse(_exc)