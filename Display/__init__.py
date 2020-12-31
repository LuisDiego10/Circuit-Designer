import pygame


class Node_visualization(pygame.sprite.Sprite):
	def __init__(self, node, *groups):
		super().__init__(*groups)
		if node.type == 0:
			self.rect = battery.get_rect()
			self.image = battery
			self.image_normal = battery
			self.image_select = battery_select
		else:
			self.rect = resistance.get_rect()
			self.image = resistance
			self.image_normal = resistance
			self.image_select = resistance_select
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

	def update(self, screen, cursor):
		if self.image == self.imgselec:
			self.image = self.imgnor
		else:
			self.image = self.imgselec
		screen.blit(self.image, self.rect)


# Create button
simulation = pygame.image.load("resources/simulation.png")
simulation_selec = pygame.image.load("resources/simulation_Selection.png")

# Images
background = pygame.image.load("resources/background.png").convert()

resistance = pygame.image.load("resources/resistance.png").convert()
resistance_select = pygame.image.load("resources/resistance_Selection.png").convert()

battery = pygame.image.load("resources/battery.png").convert()
battery_select = pygame.image.load("resources/battery_Selection.png").convert()
