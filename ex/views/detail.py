from	typing							import	Any
from	django							import	http
from	django.http.response			import	HttpResponse
from	django.views.generic			import	DetailView
from	..forms							import	FavouriteForm
from	..models.article				import	Article

class	Detail(DetailView):

		template_name	= "detail.html"
		model			= Article

		def	get_context_data(self, **kwargs):
			_ctx = super().get_context_data(**kwargs)
			_art = _ctx['object']
			_ctx["favouriteForm"] = FavouriteForm(_art.id)
			return	_ctx