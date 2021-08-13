from	django.views.generic			import	FormView
from	django.urls						import	reverse_lazy
from	Site.forms						import	ProfileForm
from	Site.models.myuser				import	MyUser
from	Site.models.message				import	Message

class	ProfileView(FormView):
		form_class		= ProfileForm
		template_name	= 'Site/view/profile.html'

		def get_initial(self):
			_ini		= super().get_initial()
			_usr		= MyUser.objects.get(nickName=str(self.kwargs.get('pk')))
			if _usr is not None:
				_ini.update({'myEmail': _usr.email, 'description': _usr.description, \
					'firstName': _usr.firstName, 'lastName': _usr.lastName, 'profileImage': _usr.profileImage})
				if _usr.is_admin:
					_ini['myAdmin'] = "Y"
				else:
					_ini['myAdmin'] = "N"
			return	_ini

		def get_success_url(self):
			_url		= reverse_lazy('Site:profile', args=[str(self.kwargs.get('pk'))])
			return	_url

		def get_context_data(self, **kwargs):
			_ctx		= super().get_context_data(**kwargs)
			_usr		= MyUser.objects.get(nickName=str(self.kwargs.get('pk')))
			if (not _usr.is_superuser) and (self.request.user.is_superuser):
				_ctx['admin'] = True
			else:
				_ctx['admin'] = False
			if self.request.user and self.request.user.is_authenticated and self.request.user.nickName == str(self.kwargs.get('pk')):
				_ctx['owner'] = True
				_ctx['start'] = False
			else:
				_ctx['owner'] = False
				_msg = Message.objects.filter(sender=self.request.user, receiver=_usr)
				_msg |= Message.objects.filter(sender=_usr, receiver=self.request.user)
				if _msg:
					_ctx['start'] = False
				else:
					_ctx['start'] = True
			return	_ctx

		def form_valid(self, form):
			_usr		= MyUser.objects.get(nickName=str(self.kwargs.get('pk')))
			try:
				_old	= _usr.email
				_new	= form.cleaned_data['myEmail']
				if _old == _new:
					raise	MyUser.DoesNotExist
				if _old != _new and MyUser.objects.get(email=_new):
					raise	AttributeError
			except AttributeError:
				form._errors['myEmail'] = form.error_class([u'Existing Email'])
				return super().form_invalid(form)
			except MyUser.DoesNotExist:
				_usr.email			= form.cleaned_data['myEmail']
				_usr.firstName		= form.cleaned_data['firstName']
				_usr.lastName		= form.cleaned_data['lastName']
				_usr.profileImage	= form.cleaned_data['profileImage']
				_usr.description	= form.cleaned_data['description']
				if form.cleaned_data['myAdmin'] and form.cleaned_data['myAdmin'] == 'Y':
					_usr.is_admin	= True
				elif form.cleaned_data['myAdmin'] and form.cleaned_data['myAdmin'] == 'N':
					_usr.is_admin	= False
				_usr.save()
				return	super().form_valid(form)
			except Exception:
				return	super().form_invalid(form)
			return	super().form_invalid(form)

		def form_invalid(self, form):
			print(form._errors)
			return super().form_invalid(form)
