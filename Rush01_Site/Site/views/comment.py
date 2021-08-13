from	typing							import	Any, Dict, Optional
from	django							import	http
from	django.http						import	request
from	django.http.response			import	Http404, HttpResponse, HttpResponseBase
from	django.urls						import	reverse_lazy, reverse
from	django.contrib					import	messages
from	django.contrib.auth.mixins		import	LoginRequiredMixin
from	django.shortcuts				import	redirect, render
from	django.views.generic			import	FormView, RedirectView
from	Site.models.post				import	Post
from	Site.models.comment				import	Comment
from	Site.forms						import	CommentForm


class	PostCheckMixin:
		def	dispatch(self, request: http.HttpRequest, post_id,  *args: Any, **kwargs: Any) -> HttpResponse:
			try:
				post: Post		= Post.objects.get(id=post_id)
			except Post.DoesNotExist:
				raise	Http404()
			self.instance		= post
			return	super().dispatch(request, post_id, *args, **kwargs)


class	CommentView(LoginRequiredMixin, PostCheckMixin, FormView):
		form_class			= CommentForm

		def	get_success_url(self) -> str:
			return	reverse('Site:post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

		def	get(self, *args, **kwargs):
			raise	Http404

		def	get_initial(self) -> Dict[str, Any]:
			_ini			= super().get_initial()
			return	_ini

		def	form_valid(self, form: CommentForm) -> HttpResponse:
			_cmt:Comment	= form.save(commit=False)
			_cmt.userID 	= self.request.user
			_cmt.postID 	= self.instance
			if form.cleaned_data['parent']:
				try:
					_par = Comment.objects.get(id=form.cleaned_data['parent'])
					_cmt.parent = _par
				except Comment.DoesNotExist:
					print("ERROR!!!!")
			_cmt.save()
			messages.success(self.request, "✅ Reply succeess ✅")
			return	super().form_valid(form)

		def	form_invalid(self, form: CommentForm) -> HttpResponse:
			messages.error(self.request, "⚠️ Delete Failed ⚠️")
			return	super().form_invalid(form)

		def post(self, request, *args, **kwargs):
			_cid = self.request.POST.get('id')
			if _cid:
				try:
					if request.POST.get("comment-up"):
						_cmt = Comment.objects.get(id=_cid)
						_cmt.upvote(request.user)
						return redirect("Site:post-detail", _cmt.postID.id)
					elif request.POST.get("comment-down"):
						_cmt =  Comment.objects.get(id=_cid)
						_cmt.downvote(request.user)
						return redirect("Site:post-detail", _cmt.postID.id)
				except Exception as _exc:
					print(_exc)
			return super().post(request, *args, **kwargs)

class	CommentDeleteView(LoginRequiredMixin, PostCheckMixin, RedirectView):
		def	get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
			return	reverse('Site:post-detail', kwargs={'post_id': self.kwargs.get('post_id')})

		def get(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
			_cid = self.kwargs.get('comment_id')
			try:
				_cmt:Comment = Comment.objects.get(id=_cid)
				_cmt.is_active = False
				_cmt.save()
			except Comment.DoesNotExist:
				messages.error(self.request, "⚠️ Delete Failed ⚠️")
				raise	Http404
			self.instance.save()
			messages.success(self.request, "✅ Delete succeess ✅")
			return	super().get(request, *args, **kwargs)
