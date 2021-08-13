from	django							import	forms
from 	django.db						import	models
from 	django.db.models.deletion 		import	CASCADE
from 	django.contrib.auth.models 		import	BaseUserManager, AbstractBaseUser

class	UserManager(BaseUserManager):
		def	create_user(self, nickName, email, password=None):
			if not nickName:
				raise ValueError('Users must have an nickName')
			if not email:
				raise ValueError('Users must have an email')
			_usr = self.model(
				nickName		= nickName,
				email			= self.normalize_email(email),
				firstName		= "",
				lastName		= "",
				description		= "")
			_usr.set_password(password)
			_usr.save(using=self._db)
			return	_usr

		def	create_superuser(self, nickName, email, password):
			_usr = self.create_user(
				nickName		= nickName,
				email			= email,
				password		= password,)
			_usr.is_admin		= True
			_usr.is_superuser	= True
			_usr.save(using=self._db)
			return	_usr

class	MyUser(AbstractBaseUser):
		nickName				= models.CharField(max_length=25, primary_key=True, unique=True, null=False)
		email					= models.EmailField(unique=True)
		firstName				= models.CharField(max_length=25, null=False)
		lastName				= models.CharField(max_length=25, null=False)
		description				= models.TextField(max_length=420, null=False)
		profileImage			= models.ImageField()

		is_active				= models.BooleanField(default=True)
		is_admin				= models.BooleanField(default=False)
		is_superuser			= models.BooleanField(default=False)

		objects					= UserManager()
		USERNAME_FIELD			= 'nickName'
		REQUIRED_FIELDS			= ['email', ]

		PASSWORD_FIELD			= 'password'

		def __str__(self):
			return	self.nickName

		def has_perm(self, perm, obj=None):
			return	True

		def has_module_perms(self, app_label):
			return	True

		@property
		def is_staff(self):
			return	self.is_admin
