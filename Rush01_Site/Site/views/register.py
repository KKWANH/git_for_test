from	django.urls						import	reverse_lazy
from	django.http.response			import	HttpResponse
from	django.contrib					import	messages
from	django.contrib.auth				import	login
from	django.views.generic			import	FormView
from	Site.forms						import	UserCreationForm
from	django.shortcuts				import	redirect

class	Register(FormView):
		template_name	= 'Site/view/register.html'
		success_url		= reverse_lazy('Site:main')
		form_class		= UserCreationForm

		def get(self, request, *args, **kwargs):
			if self.request.user and self.request.user.is_authenticated:
				return	redirect("Site:main")
			else:
				return super().get(request, *args, **kwargs)

		def	form_valid(self, form: UserCreationForm) -> HttpResponse:
			_usr = form.save()
			login(self.request, _usr)
			messages.success(self.request, "✅ Registration success ✅")
			return	super().form_valid(form)

		def	form_invalid(self, form: UserCreationForm) -> HttpResponse:
			messages.success(self.request, "⚠️ Registration failed ⚠️")
			return	super().form_invalid(form)
