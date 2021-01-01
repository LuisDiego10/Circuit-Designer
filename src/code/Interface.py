import threading
import tkinter
from tkinter import *

import pygame
from pygame.sprite import Group

pygame.init()
weight = 1200
height = 800
screen = pygame.display.set_mode([weight, height])
pygame.display.set_caption("CIRCUIT DESIGNER 👨🏼💻")

import Display
from Display import *

from graph import *


def update_nodes(node_group: Group, displayed_graph: Graph):
	node_group.empty()
	for node in displayed_graph.nodes:
		node_display = Display.Node_visualization(node)
		node_group.add(node_display)
	return node_group


def run(displayed_graph: Graph):
	done = False
	clock = pygame.time.Clock()
	node_edit_mode = Edit_node_screen(graph)
	node_edit_mode.start()

	nodes: Group = pygame.sprite.Group()
	nodes = update_nodes(nodes, graph)
	buttons: Group = pygame.sprite.Group()
	cable = pygame.sprite.Group()
	selected = pygame.sprite.Group()

	simulation_button = Button(Display.simulation, Display.simulation_selec, 1055, 725, buttons)

	while not done:

		screen.blit(background, [0, 0])

		# update mouse position
		(mouse_x, mouse_y) = pygame.mouse.get_pos()
		screen.blit(
			pygame.font.Font('freesansbold.ttf', 16).render(("x" + str(mouse_x) + "y" + str(mouse_y)), True,
			                                                (255, 200, 200)), (700, 200))

		# show nodes and buttons
		nodes.draw(screen)
		buttons.draw(screen)
		selected.draw(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			# Checking if user clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				# check for left click
				if event.button == 1:
					# check for button selection
					if simulation_button.rect.collidepoint(mouse_x, mouse_y):
						simulation_button.update()
						continue
					# check for Node selection
					for node in nodes:
						if node.rect.collidepoint(mouse_x, mouse_y):
							if selected.has(node):
								node.update()
								selected.remove(node)
							else:
								node.update()
								selected.add(node)
				# check for right click
				elif event.button == 3:
					for node in nodes:
						if node.rect.collidepoint(mouse_x, mouse_y):
							node_edit_mode.node(node)
					continue

		pygame.display.flip()
		clock.tick(60)
	pygame.quit()
	node_edit_mode.main_window.quit()
	node_edit_mode.stop()


graph = Graph()

node1 = Node()
node1.set_name("one")
node1.type = 0
node1.position = (250, 41)
graph.insert_node(node1)

node2 = Node()
node2.set_name("two")
node2.type = 1
node2.position = (120, 452)
node2.rotation = 1
graph.insert_node(node2)

graph.new_arc(node2, node1)

run(graph)
exit()