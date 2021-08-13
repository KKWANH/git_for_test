from	django.shortcuts				import	render
from	..models						import	FileModel
from	..forms							import	FileForm

def		home(request):
		_fls = FileModel.objects.all()
		if request.method == "POST":
			print("this is if.. why?")
			_frm = FileForm(request.POST, request.FILES)
			if _frm.is_valid():
				_frm.save()
		else:
			print("this is else lol")
			_frm = FileForm()
		return	render(request, "ex00/home.html", {'form': _frm, 'files': _fls})