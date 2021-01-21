import random
from typing import List, Any

import pygame
import math
from pygame.sprite import Group

from graph import Node


class Wire_node(pygame.sprite.Sprite):
	def __init__(self, x, y, node, wire, color, *groups):
		super().__init__(*groups)
		self.position = (x, y)
		self.selected = False
		self.color = color
		self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0))
		pygame.draw.circle(self.image, color, (5, 5), 5)
		pygame.draw.circle(self.image, tuple(int(i * 0.8) for i in self.color), (5, 5), 3)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.node = node
		self.wire = wire

	def update(self, *args):
		if self.selected:
			self.selected = False
			self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
			self.image.fill((0, 0, 0, 0))
			pygame.draw.circle(self.image, self.color, (5, 5), 5)
			pygame.draw.circle(self.image, tuple(int(i * 0.8) for i in self.color), (5, 5), 2)
		else:
			self.selected = True
			self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
			self.image.fill((0, 0, 0, 0))
			pygame.draw.circle(self.image, self.color, (5, 5), 5)
			pygame.draw.circle(self.image, (250, 250, 250), (5, 5), 2)


class Wire:
	wires: List[Wire_node]

	def __init__(self, screen, node: Node, group: Group):
		self.screen = screen
		self.group = group
		self.start = node
		self.end = []
		self.wires = []
		self.color = tuple(random.randint(0, 220) for _ in range(3))
		self.update_position()
		self.voltage = random.randint(0, 10)
		self.amps = random.randint(0, 1000)
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

		self.wires.append(Wire_node(x, y, self.start, self, self.color))

	def draw(self, color=None):
		if len(self.end) == 0:
			return
		start = self.start
		wire_connect = start.position
		if start.type == 0:
			wire_connect = (wire_connect[0] - 25 * math.sin(start.rotation * (math.pi / 2)),
			                wire_connect[1] - 25 * math.cos(start.rotation * (math.pi / 2)))
		else:
			if start.rotation % 2 == 1:
				wire_connect = (wire_connect[0] - 1 * math.cos(start.rotation * (math.pi / 2)),
				                wire_connect[1] - 50 * math.sin(start.rotation * (math.pi / 2)))
			else:
				wire_connect = (wire_connect[0] - 50 * math.cos(start.rotation * (math.pi / 2)),
				                wire_connect[1] - 1 * math.sin(start.rotation * (math.pi / 2)))
		pygame.draw.line(self.screen, self.color, wire_connect, self.wires[0].rect.center, 2)
		actual = self.wires[0]
		for i in self.wires[1:]:
			pygame.draw.line(self.screen, self.color, actual.rect.center, i.rect.center, 1)
			actual = i
		for a in self.end:
			distance = 10000
			node = ""
			for b in self.wires:
				d = ((a.position[0] + b.rect.center[0]) ** 2 + (a.position[1] + b.rect.center[1]) ** 2) ** 0.5
				if d < distance:
					node = b
			wire_connect = a.position
			if a.type == 0:
				wire_connect = (wire_connect[0] + 30 * math.sin(a.rotation * (math.pi / 2)),
				                wire_connect[1] + 30 * math.cos(a.rotation * (math.pi / 2)))
			else:
				if a.rotation % 2 == 1:
					wire_connect = (wire_connect[0] + 1 * math.cos(a.rotation * (math.pi / 2)),
					                wire_connect[1] + 50 * math.sin(a.rotation * (math.pi / 2)))
				else:
					wire_connect = (wire_connect[0] + 50 * math.cos(a.rotation * (math.pi / 2)),
					                wire_connect[1] + 1 * math.sin(a.rotation * (math.pi / 2)))
			pygame.draw.line(self.screen, self.color, wire_connect, node.rect.center, 1)

	def update_position(self):
		for a in self.wires:
			self.group.remove(a)
		self.end = []
		for node in self.start.arcs:
			self.end.append(node)
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

	def draw_underline(self, color=(0, 100, 100), size=4, graph_node=None):

		start = self.start
		wire_connect = start.position
		if start.type == 0:
			wire_connect = (wire_connect[0] - 25 * math.sin(start.rotation * (math.pi / 2)),
			                wire_connect[1] - 25 * math.cos(start.rotation * (math.pi / 2)))
		else:
			if start.rotation % 2 == 1:
				wire_connect = (wire_connect[0] - 1 * math.cos(start.rotation * (math.pi / 2)),
				                wire_connect[1] - 50 * math.sin(start.rotation * (math.pi / 2)))
			else:
				wire_connect = (wire_connect[0] - 50 * math.cos(start.rotation * (math.pi / 2)),
				                wire_connect[1] - 1 * math.sin(start.rotation * (math.pi / 2)))
		pygame.draw.line(self.screen, color, wire_connect, self.wires[0].rect.center, size + 1)
		actual = self.wires[0]
		for i in self.wires[1:]:
			pygame.draw.line(self.screen, color, actual.rect.center, i.rect.center, size)
			actual = i
		a = graph_node
		distance = 10000
		node = ""
		for b in self.wires:
			d = ((a.position[0] + b.rect.center[0]) ** 2 + (a.position[1] + b.rect.center[1]) ** 2) ** 0.5
			if d < distance:
				node = b
		wire_connect = a.position
		if a.type == 0:
			wire_connect = (wire_connect[0] + 30 * math.sin(a.rotation * (math.pi / 2)),
			                wire_connect[1] + 30 * math.cos(a.rotation * (math.pi / 2)))
		else:
			if a.rotation % 2 == 1:
				wire_connect = (wire_connect[0] + 1 * math.cos(a.rotation * (math.pi / 2)),
				                wire_connect[1] + 50 * math.sin(a.rotation * (math.pi / 2)))
			else:
				wire_connect = (wire_connect[0] + 50 * math.cos(a.rotation * (math.pi / 2)),
				                wire_connect[1] + 1 * math.sin(a.rotation * (math.pi / 2)))
		pygame.draw.line(self.screen, color, wire_connect, node.rect.center, size)
