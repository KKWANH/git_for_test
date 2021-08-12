from	typing							import	Any
from	django.contrib					import	messages
from	django.contrib.auth				import	authenticate, login
from	django.http						import	HttpResponse, HttpRequest
from	django.shortcuts				import	redirect
from	django.views.generic			import	FormView
from	django.urls						import	reverse_lazy
from	ex.forms.login					import	LoginForm


class	Login(FormView):

		template_name	= "login.html"
		form_class		= LoginForm
		success_url		= reverse_lazy("index")

		def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
			if self.request.user.is_authenticated:
				messages.error(self.request, *args, **kwargs)
				return	redirect('index')
			return	super().get(request, *args, **kwargs)
		
		def form_valid(self, form: LoginForm):
			_nam	= form.cleaned_data.get('username')
			_pas	= form.cleaned_data.get('password')
			_usr	= authenticate(self.request, username=_nam, password=_pas)
			if _usr is None:
				messages.error(self.request, "Invalid username or password.")
				return
			login(self.request, _usr)
			messages.info(self.request, f"You are now logged in as {_nam}.")
			return	super().form_valid(form)
		
		def form_invalid(self, form):
			return	super().form_invalid(form)