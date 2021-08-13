from	typing							import	Any, Dict, Optional
from	django							import	http
from	django.http						import	request, HttpRequest
from	django.http.response			import	Http404, HttpResponse, HttpResponseBase
from	django.urls						import	reverse_lazy, reverse
from	django.http.response			import	HttpResponseBase
from	django.contrib					import	messages
from	django.contrib.auth.mixins		import	LoginRequiredMixin
from	django.shortcuts				import	redirect, render
from	django.views.generic			import	FormView, DetailView, RedirectView
from	Site.models.post				import	Post
from	Site.models.comment				import	Comment
from	Site.forms						import	PostForm, CommentForm


class	PostUserCheckMixin:
	def	dispatch(self, request: http.HttpRequest, post_id,  *args: Any, **kwargs: Any) -> HttpResponse:
		print(post_id)
		try:
			post: Post		= Post.objects.get(id=post_id)
		except Post.DoesNotExist:
			raise	Http404()
		if post.userID		!= request.user and not request.user.is_staff:
			messages.error(request, "⚠️ Permission denied ⚠️")
			return	redirect("Site:main")
		self.instance		= post
		return	super().dispatch(request, post_id, *args, **kwargs)


class	PostView(LoginRequiredMixin, FormView):
		template_name		= 'Site/view/post_new.html'
		form_class			= PostForm
		login_url			= reverse_lazy('Site:login')

		def	get_success_url(self) -> str:
			return	reverse('Site:post-detail', args=[self.instance.id])

		def	form_valid(self, form: PostForm) -> HttpResponse:
			post:Post		= form.save(commit=False)
			post.userID 	= self.request.user
			post.save()
			self.instance = post
			messages.success(self.request, "✅ Posting succeess ✅")
			return	super().form_valid(form)

		def	form_invalid(self, form: PostForm) -> HttpResponse:
			return	super().form_invalid(form)

class	PostDetailView(LoginRequiredMixin, DetailView):
		template_name		= 'Site/view/post_detail.html'
		login_url			= reverse_lazy('Site:login')
		model				= Post
		pk_url_kwarg		= 'post_id'

		def	get_context_data(self, **kwargs):
			_ctx		= super().get_context_data(**kwargs)
			_pst: Post	= _ctx['object']
			if _pst.is_active == False:
				raise	Http404()
			_ctx['post_up'] = False
			_ctx['post_down'] = False
			if _pst.is_upvoting(self.request.user):
				_ctx['post_up'] = True
			if _pst.is_downvoting(self.request.user):
				_ctx['post_down'] = True
			_ctx["comment_form"] = CommentForm()
			return	_ctx
		
		def post(self, request, post_id):
			_pid = self.request.POST.get('id')
			if _pid:
				try:
					if request.POST.get("post-up"):
						_pst = Post.objects.get(id=_pid)
						_pst.upvote(request.user)
					elif request.POST.get("post-down"):
						_pst = Post.objects.get(id=_pid)
						_pst.downvote(request.user)
					return redirect("Site:post-detail", post_id)
				except Exception as _exc:
					print(_exc)
			return	redirect("Site:main")

class	PostEditView(LoginRequiredMixin, PostUserCheckMixin, FormView):
		template_name		= 'Site/view/post_edit.html'
		login_url			= reverse_lazy('Site:login')
		form_class			= PostForm

		def	get_success_url(self) -> str:
			return	reverse('Site:post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

		def	get_initial(self) -> Dict[str, Any]:
			_pst: Post		= self.instance
			_ini			= super().get_initial()
			_ini['title']	= _pst.title
			_ini['content']	= _pst.content
			return	_ini

		def	form_valid(self, form: PostForm) -> HttpResponse:
			self.instance.title		= form.cleaned_data['title']
			self.instance.content	= form.cleaned_data['content']
			self.instance.save()
			return	super().form_valid(form)

		def	form_invalid(self, form: PostForm) -> HttpResponse:
			return	super().form_invalid(form)

class	PostDeleteView(LoginRequiredMixin, PostUserCheckMixin, RedirectView):
		url = reverse_lazy('Site:main')

		def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
			self.instance.is_active = False
			for _cmt in self.instance.get_comments():
				_cmt.is_active = False
				_cmt.save()
			self.instance.save()
			messages.info(request, "✅ Delete post success ✅")
			return	super().get(request, *args, **kwargs)
