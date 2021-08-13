from 	django.db						import models
from 	django.db.models.deletion 		import CASCADE
from 	Site.models.myuser		 		import MyUser


class	Post(models.Model):
		id			= models.AutoField(primary_key=True)
		userID		= models.ForeignKey(MyUser, on_delete=CASCADE, related_name="post")
		title		= models.CharField(max_length=40)
		content		= models.TextField(null=False)
		created		= models.DateTimeField(auto_now_add=True, null=False)
		updated		= models.DateTimeField(auto_now=True, null=False)
		is_active	= models.BooleanField(default=True, null=False)
		upvotes		= models.ManyToManyField(MyUser, related_name="postUpvotes")
		downvotes	= models.ManyToManyField(MyUser, related_name="postDownvotes")

		class	Meta:
				ordering = ('created',)
		
		def	__str__(self):
			return	self.title
		
		def	get_comments(self):
			return	self.comment.filter(parent=None, is_active=True)

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
		
		def	is_upvoting(self, user):
			if user.nickName in [_usr.nickName for _usr in self.upvotes.all()]:
				return	True
			else:
				return	False

		def	is_downvoting(self, user):
			if user.nickName in [_usr.nickName for _usr in self.downvotes.all()]:
				return	True
			else:
				return	False