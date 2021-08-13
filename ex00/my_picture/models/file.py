from	django.db						import	models

class	FileModel(models.Model):
		name = models.CharField(max_length=40)
		file = models.FileField(upload_to='files')