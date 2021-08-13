from 	django.db						import	models
from 	django.db.models.deletion 		import	CASCADE
from 	Site.models.myuser				import	MyUser
from	Site.models.post				import	Post


class	Comment(models.Model):
		id			= models.AutoField(primary_key=True)
		postID		= models.ForeignKey(Post, on_delete=CASCADE, related_name="comment")
		userID		= models.ForeignKey(MyUser, on_delete=CASCADE, related_name="comment")
		parent		= models.ForeignKey('self', on_delete=CASCADE, related_name="recomment", null=True)
		comment		= models.TextField(max_length=500, null=False)
		created		= models.DateTimeField(auto_now_add=True, null=False)
		updated		= models.DateTimeField(auto_now=True, null=False)
		is_active	= models.BooleanField(default=True)
		upvotes		= models.ManyToManyField(MyUser, related_name="commentUpvotes")
		downvotes	= models.ManyToManyField(MyUser, related_name="commentDownvotes")

		class	Meta:
				ordering = ('created',)

		def	__str__(self):
			return	self.comment

		def	get_comments(self):
			return	Comment.objects.filter(parent=self, is_active=True)

		def	get_replyform(self):
			from	Site.forms.comment	import	CommentForm
			_frm = CommentForm()
			_frm.fields['parent'].initial = self.id
			return	_frm

		def	upvote(self, user):
			if user.nickName in [_usr.nickName for _usr in self.upvotes.all()]:
				self.upvotes.remove(user)
			else:
				if user.nickName in [_usr.nickName for _usr in self.downvotes.all()]:
					self.downvotes.remove(user)
				self.upvotes.add(user)
			self.save()

		def	downvote(self, user):
			if user.nickName in [_usr.nickName for _usr in self.downvotes.all()]:
				self.downvotes.remove(user)
			else:
				if user.nickName in [_usr.nickName for _usr in self.upvotes.all()]:
					self.upvotes.remove(user)
				self.downvotes.add(user)
			self.save()

		def	get_upvotes(self):
			return	self.upvotes.count()

		def	get_downvotes(self):
			return	self.downvotes.count()
