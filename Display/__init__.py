import pygame


class Node_visualization(pygame.sprite.Sprite):
	def __init__(self, node, *groups):
		super().__init__(*groups)
		if node.type == 0:
			self.image = battery
			self.image_normal = battery
			self.image_select = battery_select
		else:
			self.image = resistance
			self.image_normal = resistance
			self.image_select = resistance_select
		if node.rotation == 1:
			self.image = pygame.transform.rotate(self.image, 90)
			self.image_select = pygame.transform.rotate(self.image_select, 90)
			self.image_normal = pygame.transform.rotate(self.image_normal, 90)
		elif node.rotation == 2:
			self.image = pygame.transform.rotate(self.image, 180)
			self.image_select = pygame.transform.rotate(self.image_select, 180)
			self.image_normal = pygame.transform.rotate(self.image_normal, 180)
		elif node.rotation == 3:
			self.image = pygame.transform.rotate(self.image, 270)
			self.image_select = pygame.transform.rotate(self.image_select, 270)
			self.image_normal = pygame.transform.rotate(self.image_normal, 270)
		self.rect = self.image.get_rect()
		self.rect.center = node.position

	def update(self, *args):
		if self.image == self.image_select:
			self.image = self.image_normal
		else:
			self.image = self.image_select
		pass


class Button(pygame.sprite.Sprite):
	def __init__(self, img1, img2, x, y, *groups):
		super().__init__(*groups)
		self.imgnor = img1
		self.imgselec = img2
		self.image = self.imgnor
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		if self.image == self.imgselec:
			self.image = self.imgnor
		else:
			self.image = self.imgselec


# Create button
simulation = pygame.image.load("resources/simulation.png")

simulation_selec = pygame.image.load("resources/simulation_Selection.png")

# Images
background = pygame.image.load("resources/background.png").convert()

resistance = pygame.image.load("resources/resistance.png").convert()
resistance = pygame.transform.scale(resistance, (100,60))
resistance_select = pygame.image.load("resources/resistance_Selection.png").convert()
resistance_select = pygame.transform.scale(resistance_select, (100,60))

battery = pygame.image.load("resources/battery.png").convert()
battery = pygame.transform.scale(battery, (80,80))
battery_select = pygame.image.load("resources/battery_Selection.png").convert()
battery_select = pygame.transform.scale(battery_select, (80,80))
