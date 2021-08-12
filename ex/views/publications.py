from	typing							import	Any
from	django.views.generic			import	ListView
from	..models.article				import	Article

class	Publications(ListView):

		template_name	= "publications.html"
		model			= Article

		def	get_queryset(self):
			return	self.model.objects.filter(author=self.request.user)