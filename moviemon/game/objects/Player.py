from	django.conf			import settings

class	Player:

	def	__init__(self, position):
		self.x = position[0]
		self.y = position[1]
		self.max_x = settings.DEFAULT_GAME_SIZE
		self.max_y = settings.DEFAULT_GAME_SIZE
		self.min_x = 0
		self.min_y = 0
	
	def	ft_move_up(self):
		if (self.y > self.min_y)
			self.y -= 1
	
	def	ft_move_down(self):
		if (self.y < self.max_y):
			self.y += 1
	
	def	ft_move_left(self):
		if (self.x > self.min_x):
			self.x -= 1

	def	ft_move_right(self):
		if (self.x < self.max_x):
			self.x += 1
	
	def	ft_get_position(self):
		return ([self.x, self.y])