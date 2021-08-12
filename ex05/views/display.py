from	django					import	db
from	django.views			import	View
from	django.http				import	HttpResponse
from	django.shortcuts		import	render
from	..models				import	Movies

class	Display(View):

	_tmp = 'ex05/display.html'

	def	get(self, request):
		try:
			_mvs = Movies.objects.all()
			if len(_mvs) == 0:
				raise Movies.DoesNotExist
			return	render(request, self._tmp, {"movies": _mvs})
		except Movies.DoesNotExist as _exc:
			return	HttpResponse("No data available")
