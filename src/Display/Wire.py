from typing import List, Any

import pygame
from pygame.sprite import Group

from graph import Node

wire_image = pygame.image.load("resources/Red.png").convert()
wire_image = pygame.transform.scale(wire_image, (10, 10))


class Wire_node(pygame.sprite.Sprite):
	def __init__(self, x, y, node, *groups):
		super().__init__(*groups)
		self.position = (x, y)
		self.image = wire_image
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.node = node


class Wire:
	wires: List[Wire_node]

	def __init__(self, screen, node: Node, group: Group):
		self.screen = screen
		self.group = group
		self.start = node
		self.end = []
		self.wires = []
		self.update_position()
		print("asd")

	def standar_deviation(self):
		if len(self.end) == 0:
			return 0
		x = self.start.position[0]
		y = self.start.position[1]
		for i in self.end:
			x += i.position[0]
			y += i.position[1]
		y = y / (len(self.end) + 1)
		x = x / (len(self.end) + 1)

		self.wires.append(Wire_node(x, y, self.start))

	def draw(self):
		if len(self.end) == 0:
			return
		pygame.draw.line(self.screen, (220, 15, 15), self.start.position, self.wires[0].position, 2)
		actual = self.wires[0]
		for i in self.wires[1:]:
			pygame.draw.line(self.screen, (200, 20, 20), actual.position, i.position)
			actual = i
		for a in self.end:
			distance = 10000
			node = ""
			for b in self.wires:
				d = ((a.position[0] + b.position[0]) ** 2 + (a.position[1] + b.position[1]) ** 2) ** 0.5
				if d < distance:
					node = b
			pygame.draw.line(self.screen, (200, 20, 20), a.position, node.position, 1)

	def update_position(self):
		for a in self.wires:
			self.group.remove(a)
		self.end = []
		for node in self.start.arcs:
			self.end.append(Wire_node(node.position[0], node.position[1], self.start))
		self.wires = []
		self.standar_deviation()
		for wire in self.wires:
			self.group.add(wire)

	def update(self):
		for wire in self.wires:
			if wire in self.group:
				continue
			else:
				self.group.add(wire)
