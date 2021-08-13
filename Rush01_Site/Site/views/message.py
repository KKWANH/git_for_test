from	django.views.generic			import	ListView
from	django.contrib					import	messages
from	django.shortcuts				import	redirect, render
from	django.urls						import	reverse_lazy
from	Site.models.myuser				import	MyUser
from	Site.models.message				import	Message

class	DiscussionListView(ListView):
		paginate_by		= 10
		model			= Message
		template_name	= 'Site/view/discussion_list.html'

		def get_queryset(self):
			_usr	 =  MyUser.objects.get(nickName=self.request.user.nickName)
			_msg =  Message.objects.filter(sender=_usr, last=True)
			_msg |= Message.objects.filter(receiver=_usr, last=True)
			if _msg:
				_msg = _msg.order_by('-created')
			return	_msg

class	DiscussionDetailView(ListView):
		model			= Message
		fields			= ['content']
		template_name	= 'Site/view/discussion_detail.html'

		def get_queryset(self):
			_us1 =  MyUser.objects.get(nickName=str(self.kwargs.get('user1')))
			_us2 =  MyUser.objects.get(nickName=str(self.kwargs.get('user2')))
			_msg =  Message.objects.filter(sender=_us1, receiver=_us2)
			_msg |= Message.objects.filter(sender=_us2, receiver=_us1)
			return	_msg.order_by('created')

		def	get(self, request, *args, **kwargs):
			if self.kwargs.get('user1') == self.kwargs.get('user2'):
				return	redirect("Site:main")
			elif self.request.user.nickName == self.kwargs.get('user1'):
				return	super().get(request, *args, **kwargs)
			elif self.request.user.nickName == self.kwargs.get('user2'):
				return redirect("Site:discussionDetail", self.kwargs.get('user2'),  self.kwargs.get('user1'))
			else:
				messages.error(request, "⚠️ Permission denied ⚠️")
				return	redirect("Site:main")


		def post(self, request, user1, user2):
			if request.POST.get('content'):
				_snd = MyUser.objects.get(nickName=user1)
				_rcv = MyUser.objects.get(nickName=user2)
				try:
					_old = Message.objects.get(sender=_snd, receiver=_rcv, last=True)
					_old.last = False
					_old.save()
				except Message.DoesNotExist:
					try:
						_old = Message.objects.get(sender=_rcv, receiver=_snd, last=True)
						_old.last = False
						_old.save()
					except Message.DoesNotExist:
						pass
				finally:
					new = Message(
						sender	=_snd,
						receiver=_rcv,
						content	=request.POST.get('content')
					)
					new.save()
				return	redirect(reverse_lazy('Site:discussionDetail', kwargs={'user1': user1, 'user2': user2}))
			else:
				return	redirect(reverse_lazy('Site:discussionDetail', kwargs={'user1': user1, 'user2': user2}))
