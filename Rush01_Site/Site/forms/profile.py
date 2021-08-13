from	django							import forms
from	Site.models						import MyUser

class	ProfileForm(forms.ModelForm):
		myAdmin = forms.ChoiceField(label='Is_Admin', choices=[('Y', 'Yes'), ('N', 'No')], widget=forms.RadioSelect, required=False)
		myEmail = forms.EmailField(label="Email")

		class Meta:
			model = MyUser
			fields = ('myEmail', 'firstName', 'lastName', 'description', 'profileImage', 'myAdmin')

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)