from	django							import forms
from	django.contrib.auth				import login, authenticate, password_validation
from	django.contrib.auth.forms		import ReadOnlyPasswordHashField, UsernameField, UserCreationForm
from	django.core.exceptions			import ValidationError
from	django.forms.widgets			import PasswordInput
from 	django.http.request				import HttpRequest
from	django.utils.translation		import gettext, gettext_lazy as _
from	Site.models.myuser				import MyUser


class	UserLoginForm(forms.Form):
		nickName	= forms.CharField()
		password	= forms.CharField(widget=PasswordInput)

		class	AuthFail(Exception):		
				def	__str__(self) -> str:
					return	"authenticate fail"
		
		def	login(self, request: HttpRequest):
			_nck = self.cleaned_data['nickName']
			_pwd = self.cleaned_data['password']
			_usr = authenticate(
				request	=request,
				nickName=_nck,
				password=_pwd)
			if _usr is None:
				raise	self.AuthFail
			return	login(request, _usr)


class	UserCreationForm(forms.ModelForm):
		error_messages	= {
			'password_dismatch': _('The two password fields did not match!'),}
		password1		= forms.CharField(
			label		= _("Password"),
			strip		= False,
			widget		= forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
			help_text	= password_validation.password_validators_help_text_html(),)
		password2		= forms.CharField(
			label		= _("Password confirmation"),
			strip		= False,
			widget		= forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
			help_text	= _("Enter the same password as before! Just for verification."),)

		class	Meta:
				model			= MyUser
				fields			= ('nickName', 'email')
				field_classes	= {'nickName': UsernameField}
		
		def	__init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			if self._meta.model.nickName in self.fields:
				self.fields[self._meta.model.nickName].widget.attrs['autofocus'] = True
		
		def	clean_password2(self):
			_pw1 = self.cleaned_data.get("password1")
			_pw2 = self.cleaned_data.get("password2")
			if _pw1 and _pw2 and _pw1 != _pw2:
				raise	ValidationError(
					self.error_messages['password_dismatch'],
					code='password_dismatch',)
			return	_pw2
		
		def	_post_clean(self):
			super()._post_clean()
			_pwd = self.cleaned_data.get('password2')
			if _pwd:
				try:
					password_validation.validate_password(_pwd, self.instance)
				except	ValidationError as _exc:
					self.add_error('password2', _exc)
		
		def	save(self, commit=True):
			_usr = super().save(commit=False)
			print("debug1")
			print(_usr)
			_usr.set_password(self.cleaned_data['password1'])
			print("debug2")
			if commit:
				_usr.save()
			print("debug3")
			return	_usr