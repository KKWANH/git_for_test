from	django.contrib					import	messages
from	django.views.generic			import	FormView
from	django.http						import	HttpResponse
from	django.urls.base				import	reverse_lazy
from	Site.forms.user					import	UserLoginForm
from	django.shortcuts				import	redirect

class	Login(FormView):
		success_url		= reverse_lazy('Site:main')
		template_name	= 'Site/view/login.html'
		form_class		= UserLoginForm

		def get(self, request, *args, **kwargs):
			if self.request.user and self.request.user.is_authenticated:
				return	redirect("Site:main")
			else:
				return super().get(request, *args, **kwargs)

		def	get_success_url(self) -> str:
			_nxt = self.request.GET.get('next', None)
			if _nxt is not None:
				return	_nxt
			return	self.success_url

		def	form_valid(self, form: UserLoginForm) -> HttpResponse:
			try:
				form.login(self.request)
				messages.success(self.request, "✅ Login Success ✅")
			except UserLoginForm.AuthFail:
				messages.error(self.request, "⚠️ Login Fail ⚠️")
				return	super().form_invalid(form)
			return	super().form_valid(form)

		def	form_invalid(self, form: UserLoginForm) -> HttpResponse:
			messages.error(self.request, "⚠️ Login Fail ⚠️")
			return	super().form_invalid(form)
