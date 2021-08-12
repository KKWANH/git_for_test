import	psycopg2
from	django.conf				import	settings
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	redirect, render
from	..forms					import	RemoveForm


class	Remove(View):

	_tmp = "ex06/remove.html"
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
			with self._con.cursor() as _cur:
				_cur.execute(_sql)
				_mvs = _cur.fetchall()
			_ctx = {'form': RemoveForm(choices=((_mov[0], _mov[0]) for _mov in _mvs))}
			return	render(request, self._tmp, _ctx)
		except Exception as _exc:
			return	HttpResponse("No data available")
	
	def	post(self, request):
		_sql = f"""
			SELECT	*
			FROM	{self._def};
		"""
		try:
			with self._con.cursor() as _cur:
				_cur.execute(_sql)
				_mvs = _cur.fetchall()
			_chs = ((_mov[0], _mov[0]) for _mov in _mvs)
		except Exception as _exc:
			print(_exc)
		_dat = RemoveForm(_chs, request.POST)
		_sql = f"""
			DELETE	FROM {self._def}
			WHERE	title = %s
		"""
		if _dat.is_valid() == True:
			try:
				with self._con.cursor() as _cur:
					_cur.execute(_sql, [_dat.cleaned_data['title']])
				self._con.commit()
			except Exception as _exc:
				print(_exc)
		return	redirect(request.path)