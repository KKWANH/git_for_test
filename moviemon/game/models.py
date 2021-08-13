from django.db import models

class	Movie(models.Model):
	name		= models.CharField(max_length=128)
	director	= models.CharField(max_length=128)
	year		= models.IntegerField(default=1895)
	rating		= models.IntegerField(default=0)
	synopsys	= models.CharField(max_length=2000)
	actors		= models.CharField(max_length=2000)
