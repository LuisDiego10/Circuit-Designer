class Node:
	def __init__(self):
		self.name = ""
		self.value = 0
		self.arcs = []

	def set_name(self, new_name):
		self.name = new_name

	def set_value(self, new_value):
		self.value = new_value

	def new_arc(self, node):
		if node in self.arcs:
			return
		self.arcs.append(node)

	def del_arc(self, node):
		self.arcs.remove(node)
