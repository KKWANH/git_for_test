from 	django.conf 					import settings
from	django.urls						import	path
from	.								import	views
from 	django.views.static 			import	serve
from 	django.urls 					import	re_path

app_name = "Site"

urlpatterns = [
	path('',							views.Main.as_view(),					name='main'),
	path('login/',						views.Login.as_view(),					name='login'),
	path('logout/',						views.Logout.as_view(),					name='logout'),
	path('register/',					views.Register.as_view(),				name='register'),
	path('profile/<str:pk>/',			views.ProfileView.as_view(),			name='profile'),
	path('post/',						views.PostView.as_view(),				name='post'),
	path('post/<int:post_id>/',			views.PostDetailView.as_view(),			name='post-detail'),
	path('post/<int:post_id>/edit/',		views.PostEditView.as_view(),			name='post-edit'),
	path('post/<int:post_id>/delete/',	views.PostDeleteView.as_view(),			name='post-delete'),
	path('post/<int:post_id>/comment/',	views.CommentView.as_view(),			name='comment'),
	path('post/<int:post_id>/comment<int:comment_id>/delete/',
										views.CommentDeleteView.as_view(),		name='comment-delete'),
	path('discussions/',				views.DiscussionListView.as_view(), 	name='discussionList'),
	path('discussions/<str:user1>&<str:user2>/',
										views.DiscussionDetailView.as_view(),	name='discussionDetail'),
	re_path(r'^media/(?P<path>.*)$',	serve,									{'document_root':settings.MEDIA_ROOT}),
	re_path(r'^static/(?P<path>.*)$',	serve,									{'document_root': settings.STATIC_ROOT}),
]
