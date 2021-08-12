from	django.utils.deprecation		import	MiddlewareMixin
from	django.http						import	HttpRequest, HttpResponse
from	..forms.login					import	LoginForm
from	..models.article				import	Article

class	LastArticleMiddleware(MiddlewareMixin):
		def	process_template_response(self, request: HttpRequest, response: HttpResponse):
			_art = Article.objects.all().order_by("-id")
			if len(_art):
				response.context_data["last_article"] = _art[0]
			response.context_data["login_form"] = LoginForm
			return	response