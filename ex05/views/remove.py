from	django					import	db
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	render, redirect
from	..models				import	Movies
from	..forms					import	RemoveForm


class	Remove(View):

	_tmp = 'ex05/remove.html'

	def	get(self, request):
		try:
			_mvs = Movies.objects.all()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
		except Movies.DoesNotExist as e:
			return HttpResponse("No data available")
		_chs = ((_mov.title, _mov.title) for _mov in _mvs)
		_ctx = {"form": RemoveForm(_chs)}
		return render(request, self._tmp, _ctx)
	
	def	post(self, request):
		try:
			_mvs = Movies.objects.all()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
		except Movies.DoesNotExist as _exc:
			return	redirect(request.path)
		_chs = ((_mov.title, _mov.title) for _mov in _mvs)
		_dat = RemoveForm(_chs, request.POST)
		if _dat.is_valid():
			try:
				Movies.objects.get(title=_dat.cleaned_data['title']).delete()
			except db.Error as _exc:
				print(_exc)
		return redirect(request.path)