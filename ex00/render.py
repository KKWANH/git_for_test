#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
import sys
import os

class	FileReader:
	def	__init__(self, filename):
		self.filename = filename
	def read_file(self):
		pass

class	Render(FileReader):
	def	__init__(self, filename, setting_flname):
		super().__init__(filename)
		self.settings = Settings(setting_flname)
	def	process_line(self, line):
		html_line = line
		for indx in self.settings.params:
			html_line = html_line.replace("{" + indx + "}", self.settings.params[indx])
		return html_line
	def write_html(self, html_filename):
		file_html = open(html_filename, "w")
		try:
			with open(self.filename) as fild:
				for line in fild:
					html_line = self.process_line(line)
					file_html.write(html_line)
		except FileNotFoundError as excp:
			print("[{0}] FILE NOT EXIST :(".format(excp.filename))
			exit(1)
		file_html.close()

class	Settings(FileReader):
	def	__init__(self, filename):
		super().__init__(filename)
		self.read_file()
	def	read_file(self):
		self.params = dict()
		try:
			with open(self.filename) as fild:
				for line in fild:
					data = line.split("=")
					self.params[data[0].strip(" ")] = data[1].strip("\" \n")
		except FileNotFoundError as excp:
			print("[{0}] FILE NOT EXIST :(".format(excp.filename))
			exit(1)

def		ft_render(filename):
		file, flex = os.path.splitext(filename)
		if flex == ".template":
			tmp = Render(filename, "settings.py")
			tmp.write_html(file+".html")
		else:
			print("[{0}] FILE IS NOT EXTENDED WITH .template".format(filename))

if		__name__ == '__main__' :
		if len(sys.argv) == 2:
			ft_render(sys.argv[1])