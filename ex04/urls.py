from	django.urls				import	path
from	.						import	views

urlpatterns = [
	path('init/',		views.init,				name='ex04-init'),
	path('populate/',	views.populate,			name='ex04-populate'),
	path('display/',	views.display,			name='ex04-display'),
	path('remove/',		views.Remove.as_view(),	name='ex04-remove'),
]
