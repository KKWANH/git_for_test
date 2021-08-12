from	django.views.generic			import	ListView
from	typing							import	Any, Dict
from	..models						import	Article


class	ArticlesView(ListView):

		template_name	= "articles.html"
		module			= Article
		queryset		= Article.objects.filter().order_by('-created')

		def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
			_ctx = super().get_context_data(**kwargs)
			return	_ctx
