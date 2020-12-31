from typing import List, Any


class Node:
	arcs: List[any]

	def __init__(self):
		"""
		class that storage data from the elements in the graph
		"""
		self.name = ""
		self.value = 0
		self.arcs = []
		self.position = (0, 0)
		self.rotation = 0
		self.type = 0

	def set_name(self, new_name):
		self.name = new_name

	def set_value(self, new_value):
		self.value = new_value

	def new_arc(self, node: Node):
		"""
		Create new arcs
		if the arc already exist ignore the creation
		:type node: Node
		"""

		if node in self.arcs:
			return
		self.arcs.append(node)

	def del_arc(self, node):
		self.arcs.remove(node)

	def build(self, node: dict):
		"""
		Build a node from a dict
		use: "arcs","name","value","position","rotation","type"
		:type node: dict
		"""
		self.arcs = node["arcs"]
		self.name = node["name"]
		self.value = node["value"]
		self.position = node["position"]
		self.rotation = node["rotation"]
		self.type = node["type"]
