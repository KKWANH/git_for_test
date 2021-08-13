from	typing							import	Any
from	django							import	http
from	django.urls						import	reverse_lazy
from	django.http.response			import	HttpResponseBase
from	django.contrib					import	messages
from	django.contrib.auth				import	logout
from	django.contrib.auth.mixins		import	LoginRequiredMixin
from	django.views.generic			import	RedirectView

class	Logout(LoginRequiredMixin, RedirectView):
		url				= reverse_lazy('Site:main')
		login_url		= reverse_lazy('Site:login')
		
		def	get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
			logout(request)
			messages.success(request, "✅ Logout Success ✅")
			return	super().get(request, *args, **kwargs)