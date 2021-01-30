import copy
import pygame

pygame.init()
weight = 1200
height = 800
screen = pygame.display.set_mode([weight, height])
pygame.display.set_caption("CIRCUIT DESIGNER 👨🏼💻")

import Display
from Display import *

from graph import *


def update_nodes(node_group: Group, displayed_graph: Graph, wire: Group):
	node_group.empty()
	for node in displayed_graph.nodes:
		node_display = Display.Node_visualization(node, wire=wire, screen=screen)
		node_group.add(node_display)
	return node_group


def add_node(node: Node, node_group: Group, wire: Group):
	node_display = Display.Node_visualization(node, wire=wire, screen=screen)
	node_group.add(node_display)


def update_matrix(node_group: Group):
	graph.voltage_matrix = copy.deepcopy(graph.paths)
	graph.amperage_matrix = copy.deepcopy(graph.paths)
	for i in node_group.sprites():

		index = graph.nodes.index(i.node)
		for a in range(len(graph.voltage_matrix[index])):
			if graph.voltage_matrix[index][a] > 0:
				graph.voltage_matrix[index][a] = i.wire.voltage
		for a in range(len(graph.amperage_matrix[index])):
			if graph.amperage_matrix[index][a] > 0:
				graph.amperage_matrix[index][a] = i.wire.amps
		pass


def run(displayed_graph: Graph):
	done = False
	clock = pygame.time.Clock()
	nodes: Group = pygame.sprite.Group()
	node_edit_mode = Edit_node_screen(graph, nodes)
	node_edit_mode.start()

	cable = pygame.sprite.Group()
	nodes = update_nodes(nodes, graph, cable)
	buttons: Group = pygame.sprite.Group()
	selected = pygame.sprite.Group()

	simulation_button = Display.Button(Display.simulation, Display.simulation_selec, 1065, 725, buttons)
	resistance_button_edit = Display.Button(Display.resistance_edit, Display.resistance_select_edit, 1065, 350, buttons)
	battery_button_edit = Display.Button(Display.battery_edit, Display.battery_select_edit, 1065, 470, buttons)
	import_button_edit = Display.Button(Display.import_edit, Display.import_edit, 1010, 100, buttons)
	export_button_edit = Display.Button(Display.export_edit, Display.export_edit, 1125, 105, buttons)
	delete_button_edit = Display.Button(Display.delete, Display.delete, 1065, 570, buttons)

	old_mouse_x, old_mouse_y = (0, 0)
	new_element: Node or None = None
	init_simulation: bool = False
	nodes_search = []

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
		cable.draw(screen)
		for a in nodes:
			a.wire.draw()

		if init_simulation:
			for a in nodes:
				a.name_tag(screen)
				if a.rect.collidepoint(mouse_x, mouse_y):
					try:
						screen.blit(
							pygame.font.Font('freesansbold.ttf', 16).render(
								("mA:" + str(a.wire.amps) + "\n" + "V" + str(a.wire.voltage)), True,
								(211, 210, 200)), a.wire.wires[0].rect.center)
					except Exception:
						print("No wire")

			if len(selected.sprites()) == 2 and len(nodes_search) == 0:
				sprites = []
				for a in selected.sprites():
					if a.__class__ == Node_visualization:
						sprites.append(a)
				if len(sprites) == 2:
					try:
						nodes_search = graph.dijkstra([sprites[0].node, sprites[1].node], graph.voltage_matrix)
						nodes_search.append(sprites[1].node)
					except Exception as e:
						print(e)
				print(nodes_search)
			if len(selected.sprites()) != 2:
				nodes_search = []
			for a in range(len(nodes_search) - 1):
				for b in nodes:
					if b.node == nodes_search[a]:
						try:
							b.wire.draw_underline((0, 100, 100), graph_node=nodes_search[a + 1])
						except Exception as e:
							print("error while underlining the wire:")
							print(e)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				done = True
			# Checking if user clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				# check for left click
				if event.button == 1:
					# check for new element
					if new_element is not None and mouse_x < 920 and not init_simulation:
						for element in selected:
							element.update()
						selected.empty()
						if new_element.type == 1:
							resistance_button_edit.update()
						else:
							battery_button_edit.update()
						new_element.position = (mouse_x, mouse_y)
						graph.insert_node(new_element)
						add_node(new_element, nodes, cable)
						new_element = None
						node_edit_mode.refresh()
						update_matrix(nodes)

					# check for button selection
					if simulation_button.rect.collidepoint(mouse_x, mouse_y):
						graph.update_graph_arcs()
						graph.update_node_arcs()
						update_matrix(nodes)
						simulation_button.update()
						for element in selected:
							element.update()
						selected.empty()
						new_element = None
						if init_simulation:
							init_simulation = False
						else:
							init_simulation = True
						continue

					if resistance_button_edit.rect.collidepoint(mouse_x, mouse_y) and not init_simulation:
						resistance_button_edit.update()
						new_element = Node()
						new_element.type = 1
						new_element.set_name("resistance" + str(random.randint(0, 500)))
						continue

					if battery_button_edit.rect.collidepoint(mouse_x, mouse_y) and not init_simulation:
						battery_button_edit.update()
						new_element = Node()
						new_element.type = 0
						new_element.set_name("battery" + str(random.randint(0, 500)))
						continue

					if delete_button_edit.rect.collidepoint(mouse_x, mouse_y) and not init_simulation:
						delete_button_edit.update()
						for node in selected:
							cable.remove(node.wire.wires)
							graph.del_node(node.node)
							nodes.remove(node)
							selected.remove(node)
							graph.update_node_arcs()
							node_edit_mode.refresh()
						for node in nodes:
							node.wire.update_position()
						continue

					if import_button_edit.rect.collidepoint(mouse_x, mouse_y):
						file = node_edit_mode.load()
						graph.graph_load(file)

						nodes.empty()
						selected.empty()
						cable.empty()

						nodes = update_nodes(nodes, graph, cable)
					if export_button_edit.rect.collidepoint(mouse_x, mouse_y):
						graph.graph_dump(node_edit_mode.text.get())

					# check for Node selection
					for node in nodes:
						if node.rect.collidepoint(mouse_x, mouse_y):
							if pygame.key.get_mods() == 256:
								node.rotate()
								continue
							if selected.has(node):
								node.update()
								selected.remove(node)
							else:
								node.update()
								selected.add(node)
							continue

					# check for cable selection
					for wire in cable:
						if wire.rect.collidepoint(mouse_x, mouse_y):
							if selected.has(wire):
								selected.remove(wire)
								wire.update()
							else:
								selected.add(wire)
								wire.update()
						pass

				# check for right click
				elif event.button == 3:
					for node in nodes:
						if node.rect.collidepoint(mouse_x, mouse_y):
							node_edit_mode.node(node)
							break
					for wire_node in cable:
						if wire_node.rect.collidepoint(mouse_x, mouse_y):
							wire = wire_node.wire
							if wire.wires[-1] == wire_node:
								wire.wires.append(
									Wire_node(wire_node.position[0] + 15, wire_node.position[1] + 15, wire_node.node,
									          wire, wire_node.color, cable))
							else:
								index = wire.wires.index(wire_node)
								wire.wires = wire.wires[:index+1] + [
									Wire_node(wire_node.position[0] + 15, wire_node.position[1] + 15, wire_node.node,
									          wire, wire_node.color, cable)] + wire.wires[index+1:]
					continue

			# move selected Nodes
			if event.type == pygame.MOUSEMOTION:
				if pygame.mouse.get_pressed()[0] and pygame.key.get_mods() == 64:
					for a in selected:
						a.rect.center = (
							a.rect.center[0] - (old_mouse_x - mouse_x), a.rect.center[1] - (old_mouse_y - mouse_y))
						if a.__class__ == Display.Wire_node:
							try:
								a.wire.wires[a.wire.wires.index(a)].position = a.rect.center
								a.wire.wires[a.wire.wires.index(a)].rect.center = a.rect.center
							except ValueError:
								cable.remove(a)

						else:
							a.node.position = a.rect.center

		pygame.display.flip()
		old_mouse_x, old_mouse_y = (mouse_x, mouse_y)
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

node3 = Node()
node3.set_name("Three")
node3.type = 1
node3.position = (320, 452)
node3.rotation = 0
graph.insert_node(node3)

graph.new_arc(node2, node1)
graph.new_arc(node3, node1)
graph.new_arc(node1, node3)
graph.new_arc(node3, node2)

# modify the graph to adapt
graph.voltage_matrix = []
graph.amperage_matrix = []

run(graph)
exit()
