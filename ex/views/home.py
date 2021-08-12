from	django.views.generic			import	RedirectView
from	django.urls						import	reverse_lazy
from	django.utils.translation		import	activate


class	Home(RedirectView):
		url = reverse_lazy('articles')
