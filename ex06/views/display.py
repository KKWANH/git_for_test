import	psycopg2
from	django.conf				import	settings
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	render

class	Display(View):

	_tmp = 'ex06/display.html'
	_def = "ex06_movies"
	_con = psycopg2.connect(
		dbname=settings.DATABASES['default']['NAME'],
		user=settings.DATABASES['default']['USER'],
		password=settings.DATABASES['default']['PASSWORD'],
		host=settings.DATABASES['default']['HOST'],
		port=settings.DATABASES['default']['PORT'],)

	def	get(self, request):
		_sql = f"""
			SELECT * FROM {self._def};
		"""
		try:
			with self._con.cursor() as _cur:
				_cur.execute(_sql)
				_mvs = _cur.fetchall()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
			return	render(request, self._tmp, {"movies": _mvs})
		except Exception as _exc:
			return	HttpResponse("No data available")
