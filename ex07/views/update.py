import	psycopg2
from	django					import	db
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	redirect, render
from	..forms					import	UpdateForm
from	..models				import	Movies

class	Update(View):
	
	_tmp = "ex07/update.html"
	
	def	get(self, request):
		try:
			_mvs = Movies.objects.all()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
		except Movies.DoesNotExist as _exc:
			return	HttpResponse("No data available")
		_chs = ((_mov.title, _mov.title) for _mov in _mvs)
		_ctx = {"form": UpdateForm(_chs)}
		return	render(request, self._tmp, _ctx)
	
	def	post(self, request):
		try:
			_mvs = Movies.objects.all()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
		except Movies.DoesNotExist as _exc:
			return	redirect(request.path)
		_chs = ((_mov.title, _mov.title) for _mov in _mvs)
		_dat = UpdateForm(_chs, request.POST)
		if _dat.is_valid():
			try:
				_mov = Movies.objects.get(title=_dat.cleaned_data['title'])
				_mov.opening_crawl = _dat.cleaned_data['opening_crawl']
				_mov.save()
			except db.Error as _exc:
				print(_exc)
		return	redirect(request.path)