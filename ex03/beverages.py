#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
class	HotBeverage:
	def	__init__(self):
		self.price = 0.30
		self.name = "hot baverage"
	def	description(self):
		return "Just some hot water in a cup."
	def __str__(self):
		rst = "name : " + self.name + "\nprice : " + str(self.price) + "\ndescription : " + self.description()
		return rst

class	Coffee(HotBeverage):
	def	__init__(self):
		self.price = 0.40
		self.name = "coffee"
	def	description(self):
		return "A coffee, to stay awake."

class	Tea(HotBeverage):
	def	__init__(self):
		self.price = 0.50
		self.name = "tea"

class	Chocolate(HotBeverage):
	def	__init__(self):
		self.price = 0.50
		self.name = "coffee"
	def	description(self):
		return "Chocolate, sweet chocolate..."

class	Cappuccino(HotBeverage):
	def	__init__(self):
		self.price = 0.45
		self.name = "cappuccino"
	def	description(self):
		return "Un po’ di Italia nella sua tazza!"
