from	typing							import	Any
from	django.http						import	request
from	django.contrib					import	messages
from	django.contrib.auth				import	login
from	django.contrib.auth.mixins		import	LoginRequiredMixin
from	django.db						import	DatabaseError
from	django.shortcuts				import	redirect
from	django.views.generic			import	FormView
from	django.urls						import	reverse_lazy
from	..models.article				import	Article
from	..forms							import	PublishForm


class	Publish(LoginRequiredMixin, FormView):

		template_name	= "publish.html"
		form_class		= PublishForm
		success_url		= reverse_lazy('index')
		login_url		= reverse_lazy('index')

		def	form_valid(self, form: PublishForm):
			_ttl = form.cleaned_data['title']
			_syn = form.cleaned_data['synopsis']
			_con = form.cleaned_data['content']
			try:
				Article.objects.create(
					title		= _ttl,
					author		= self.request.user,
					synopsis	= _syn,
					content		= _con)
			except DatabaseError as _exc:
				messages.success(self.request, "Unsuccessful publish. DatabaseError")
				return	redirect('index')
			messages.success(self.request, "Successful publish.")
			return	super().form_valid(form)

		def	form_invalid(self, form):
			messages.error(self.request, "Unsuccessful publish. Invalid information.")
			return	super().form_invalid(form)
