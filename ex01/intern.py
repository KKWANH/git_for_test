#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
class	Intern:
	def __init__(self, name = "My name? I’m nobody, an intern, I have no name."):
		self.Name = name
	
	def	__str__(self):
		return self.Name
	
	def work(self):
		raise Exception("I’m just an intern, I can’t do that...")
	
	class	Coffee:
		def	__str__(self):
			return "This is the worst coffee you ever tasted."
	
	def make_coffee(self):
		return self.Coffee()
	
if __name__ == '__main__':
	tst1 = Intern("Mark")
	tst2 = Intern()

	print(tst1)
	print(tst2)

	caff = tst1.make_coffee()
	print(caff)

	try:
		tst2.work()
	except:
		print("tst2 - Exception occurred")