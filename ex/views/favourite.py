from	django.db						import	DatabaseError
from	django.db.models.query			import	QuerySet
from	django.contrib					import	messages
from	django.contrib.auth.forms		import	AuthenticationForm
from	django.contrib.auth.mixins		import	LoginRequiredMixin
from	django.urls						import	reverse_lazy
from	django.shortcuts				import	redirect
from	django.forms.forms				import	BaseForm
from	django.views.generic			import	FormView
from	django.views.generic.list		import	ListView
from	..forms							import	FavouriteForm
from	..models.article				import	Article, UserFavouriteArticle

class	Favourite(LoginRequiredMixin, ListView, FormView):

		template_name				= "favourite.html"
		form_class					= FavouriteForm
		success_url					= reverse_lazy('index')
		login_url					= reverse_lazy('index')
		model: UserFavouriteArticle	= UserFavouriteArticle

		def get_queryset(self):
			return	self.model.objects.filter(user=self.request.user)
		
		def	form_valid(self, form):
			_aid = form.cleaned_data['article']
			try:
				UserFavouriteArticle.objects.get(article=_aid, user=self.request.user).delete()
				messages.success(self.request, "successful Remove to favourite.")
			except UserFavouriteArticle.DoesNotExist as _exc:
				try:
					UserFavouriteArticle.objects.create(user=self.request.user, article=Article.objects.get(id=_aid),)
					messages.success(self.request, "successful Add to favourite.")
				except DatabaseError as _exc:
					messages.error(self.request, "Unsuccessful Add to favourite. Database error.")
			return	super().form_valid(form)
		
		def	form_invalid(self, form):
			messages.error(self.request, "Unsuccessful Add to favourite. Invalid information.")
			return	redirect("favourite")
		
		def	get_form(self, form_class=None) -> BaseForm:
			if form_class is None:
				form_class = self.get_form_class()
			return	form_class(None, **self.get_form_kwargs())