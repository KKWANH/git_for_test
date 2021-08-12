import	psycopg2
from	django.conf				import	settings
from	django.views			import	View
from	django.http				import	HttpResponse

class	Init(View):
	
	_def = "ex06_movies"
	_con = psycopg2.connect(
		dbname=settings.DATABASES['default']['NAME'],
		user=settings.DATABASES['default']['USER'],
		password=settings.DATABASES['default']['PASSWORD'],
		host=settings.DATABASES['default']['HOST'],
		port=settings.DATABASES['default']['PORT'],)

	def	get(self, request):
		_sql = f"""
			SELECT	*
			FROM	{self._def};
		"""
		try:
			_sql = f"""
				CREATE	TABLE		{self._def}(
					title			VARCHAR(64)		UNIQUE NOT NULL,
					episode_nb		INT				PRIMARY KEY,
					opening_crawl	TEXT,
					director		VARCHAR(32)		NOT NULL,
					producer		VARCHAR(128)	NOT NULL,
					release_date	DATE			NOT NULL,
					created			TIMESTAMP		NOT NULL DEFAULT NOW(),
					updated			TIMESTAMP		NOT NULL DEFAULT NOW()
				);

				CREATE OR REPLACE FUNCTION update_changetimestamp_column()
				RETURNS TRIGGER AS $$
				BEGIN
				NEW.updated = now();
				NEW.created = OLD.created;
				RETURN NEW;
				END;
				$$ language 'plpgsql';
				CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
					ON {self._def} FOR EACH ROW EXECUTE PROCEDURE
				update_changetimestamp_column();
			"""
			with self._con.cursor() as _cur:
				_cur.execute(_sql)
			self._con.commit()
		except Exception as _exc:
			return	HttpResponse(_exc)
		return	HttpResponse("OK")
		