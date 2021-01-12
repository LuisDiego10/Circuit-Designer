import tkinter
from functools import partial
from tkinter import *

import pygame
import threading

from Display.Wire import *


class Node_visualization(pygame.sprite.Sprite):
	def __init__(self, node, *groups, wire, screen):
		super().__init__(*groups)
		self.node = node
		self.wire = Wire(screen, node, wire)
		if node.type == 0:
			self.image = battery
			self.image_normal = battery
			self.image_select = battery_select
		else:
			self.image = resistance
			self.image_normal = resistance
			self.image_select = resistance_select

		if node.rotation > 0:
			self.image = pygame.transform.rotate(self.image, 90 * node.rotation)
			self.image_select = pygame.transform.rotate(self.image_select, 90 * node.rotation)
			self.image_normal = pygame.transform.rotate(self.image_normal, 90 * node.rotation)

		self.rect = self.image.get_rect()
		self.rect.center = node.position

	def update(self, *args):
		if self.image == self.image_select:
			self.image = self.image_normal
		else:
			self.image = self.image_select
		pass

	def rotate(self):
		rect_postion = self.rect.center
		self.node.rotation = (self.node.rotation + 1) % 4
		self.image = pygame.transform.rotate(self.image, 90)
		self.image_select = pygame.transform.rotate(self.image_select, 90)
		self.image_normal = pygame.transform.rotate(self.image_normal, 90)
		self.rect = self.image.get_rect()
		self.rect.center = rect_postion


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

	def move(self, x, y):
		self.rect.x = x
		self.rect.y = y


class Edit_node_screen(threading.Thread):
	def __init__(self, graph, nodes):
		super().__init__()
		self.graph = graph
		self.nodes = nodes

	def edit_node(self, node, name, value, arcs: str, graph, screen=0, node_vis=None):
		node.set_name(name)
		node.set_value(value)
		node.arcs = []
		arc = arcs.split(",")
		for a in arc:
			graph.new_arc(node, a)
		graph.update_graph_arcs()
		if screen != 0:
			screen.destroy()
		self.refresh()
		if node_vis is not None:
			node_vis.wire.update_position()
		pass

	def run(self) -> None:
		self.main_window = Tk()
		self.main_window.protocol("WM_DELETE_WINDOW", (lambda: self.main_window))
		# self.main_window.overrideredirect(True)
		self.main_window.bind("<Unmap>", self.main_window.focus_force())
		self.main_window.bind("<Map>", self.main_window.focus_force())
		self.main_window.geometry("400x300")
		self.main_window.title("Nodes")
		self.refresh()

		self.main_window.mainloop()

	def close_top(self, top):
		self.main_window.focus_force()
		top.destroy()

	def node(self, node):
		if node.__class__ == Node_visualization:
			visualizator = node
			node = node.node
		else:
			node = node
			for a in self.nodes:
				if a.node == node:
					visualizator = a
					break
		tabs_color = "DarkGrey"
		window = Toplevel(self.main_window)
		window.protocol("WM_DELETE_WINDOW", (lambda: self.close_top(window)))
		window.geometry("300x350")
		window.title("Node:" + node.name)
		Label(window, text="Node properties:" + node.name, bg="LightGreen", width="300", height="2",
		      font=("Calibri", 13)).pack()
		name = StringVar()
		name_entry = Entry(window, textvariable=name)
		name.set(node.name)
		Label(window, text="name:", font=("Calibri", 13)).pack()
		name_entry.pack()
		value = StringVar()
		value_entry = Entry(window, textvariable=value)
		value.set(node.value)
		Label(window, text="value:", font=("Calibri", 13)).pack()
		value_entry.pack()
		arcs = StringVar()
		arcs_entry = Entry(window, textvariable=arcs)
		text = ""
		if len(node.arcs) != 0:
			for arc in node.arcs:
				text = text + arc.name + ","
		arcs.set(text)
		Label(window, text="arcs:", font=("Calibri", 13)).pack()
		arcs_entry.pack()
		tkinter.Button(window, text="Apply", height="2", width="30", bg=tabs_color,
		               command=lambda: self.edit_node(node, name_entry.get(), value_entry.get(), arcs_entry.get(),
		                                              self.graph, window, visualizator)).pack()
		tkinter.Button(window, text="Close", height="2", width="30", bg=tabs_color,
		               command=lambda: window.destroy()).pack()
		window.focus_force()

	def stop(self):
		self.main_window.destroy()

	def refresh(self):
		for child in self.main_window.winfo_children():
			child.destroy()
		self.graph.sort()
		row = 1
		tkinter.Label(text="UP").grid(column=1, row=0)
		for node in self.graph.sorted_up:
			tkinter.Button(text=node.name, height="2", width="30",
			               command=partial(self.node, node)).grid(column=1, row=row)
			row += 1
		row = 1
		tkinter.Label(text="DOWN").grid(column=3, row=0)
		for node in self.graph.nodes:
			tkinter.Button(text=node.name, height="2", width="30",
			               command=partial(self.node, node)).grid(column=3, row=row)
			row += 1


# Create button
simulation = pygame.image.load("resources/simulation.png")
simulation = pygame.transform.scale(simulation, (150, 70))
simulation_selec = pygame.image.load("resources/simulation_Selection.png")
simulation_selec = pygame.transform.scale(simulation_selec, (150, 70))
# Images
background = pygame.image.load("resources/background.png").convert()

resistance = pygame.image.load("resources/resistance.png").convert()
resistance = pygame.transform.scale(resistance, (100, 60))
resistance_select = pygame.image.load("resources/resistance_Selection.png").convert()
resistance_select = pygame.transform.scale(resistance_select, (100, 60))

battery = pygame.image.load("resources/battery.png").convert()
battery = pygame.transform.scale(battery, (80, 80))
battery_select = pygame.image.load("resources/battery_Selection.png").convert()
battery_select = pygame.transform.scale(battery_select, (80, 80))

resistance_edit = pygame.image.load("resources/resistance.png").convert()
resistance_edit = pygame.transform.scale(resistance_edit, (100, 60))
resistance_select_edit = pygame.image.load("resources/resistance_Selection_edit.png").convert()
resistance_select_edit = pygame.transform.scale(resistance_select_edit, (100, 60))

battery_edit = pygame.image.load("resources/battery.png").convert()
battery_edit = pygame.transform.scale(battery_edit, (100, 60))
battery_select_edit = pygame.image.load("resources/battery_Selection_edit.png").convert()
battery_select_edit = pygame.transform.scale(battery_select_edit, (100, 60))
battery_select_edit.set_colorkey((0, 0, 0))

import_edit = pygame.image.load("resources/Import.png").convert()
import_edit = pygame.transform.scale(import_edit, (100, 60))
import_edit.set_colorkey((0, 0, 0))

export_edit = pygame.image.load("resources/Export.png").convert()
export_edit = pygame.transform.scale(export_edit, (100, 60))
export_edit.set_colorkey((0, 0, 0))
