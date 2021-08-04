#   42 KKIM - DJANGO & PYThON PISCINE - HEADER
#		finish date: 7/30
#		passed date:
import	random

from	beverages import HotBeverage, Coffee, Tea, Cappuccino, Chocolate

class		CoffeeMachine:

	class	EmptyCup(HotBeverage):
		def __init__(self):
			self.name = "empty cup"
			self.price = 0.90
		def description(self):
			return "An empty cup?! Gimme my money back!"

	class	BrokenMachineException(Exception):
		def	__init__(self):
			super().__init__("This coffee machine has to be repaired.")

	def		__init__(self):
		self.cnt_break = 10

	def		repair(self):
		self.cnt_break = 10
	def		serve(self, drink: HotBeverage):
		if (self.cnt_break <= 0):
			raise CoffeeMachine.BrokenMachineException
		self.cnt_break -= 1
		if random.randint(0, 9) == 0:
			return CoffeeMachine.EmptyCup()
		return drink()

if __name__ == '__main__':
	cfMc = CoffeeMachine()
	for indx in range(25):
		try:
			print(cfMc.serve(random.choice([Coffee, Tea, Cappuccino, Chocolate])))
			print()
		except CoffeeMachine.BrokenMachineException as excp:
			print(excp)
			print()
			cfMc.repair()
