from	typing							import	Any, Dict
from	django							import	forms
from	Site.models.comment				import	Comment


class	CommentForm(forms.ModelForm):
		parent			= forms.CharField(widget=forms.HiddenInput, required=False)

		class	Meta:
				model	= Comment
				fields	= ['comment',]