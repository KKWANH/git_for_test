from	typing							import	Any, Dict
from	django							import	forms
from	django.forms.widgets			import	Textarea
from	Site.models.post				import	Post


class	PostForm(forms.ModelForm):
		title	= forms.CharField()
		content	= forms.CharField(widget=Textarea)

		class	Meta:
				model	= Post
				fields	= ['title', 'content']