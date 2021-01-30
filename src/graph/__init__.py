import json
from typing import List, Any

from graph.Node import Node


class Graph:
	paths: List[List[int]]
	nodes: List[Node]

	def __init__(self):
		"""
		create a empty graph class

		"""
		self.nodes = []
		self.paths = []
		self.sorted_up = []
		self.sorted_down = []
		pass

	def insert_node(self, node: Node):
		"""
		Insert a node and its arcs in the graph
		:type node: Node
		"""
		self.nodes.append(node)
		path = []
		for i in self.nodes:
			if i in node.arcs:
				path.append(1)
			else:
				path.append(0)
		for i in self.paths:
			i.append(0)
		self.paths.append(path)

	def del_node(self, node):
		"""
		delete a Node and it arcs from the graph
		:param node: Node or Node name
		"""
		node = self.find_node(node)
		index = self.nodes.index(node)
		self.paths.pop(index)
		for i in self.paths:
			i.pop(index)
		self.nodes.remove(node)

	def find_node(self, name):
		"""
		Search in graph nodes the node by their name
		:param name: Node or Node name
		:return: Node
		"""
		if name.__class__ != str:
			return name
		for i in self.nodes:
			if i.name == name:
				return i
		else:
			return -1

	def new_arc(self, start_node, end_node):
		"""
		Create a new arc
		:param start_node: start Node or it name
		:param end_node: end Node or it name
		"""
		start_node = self.find_node(start_node)
		end_node = self.find_node(end_node)
		if -1 == start_node or -1 == end_node:
			return
		start_node.new_arc(end_node)
		self.paths[self.nodes.index(start_node)][self.nodes.index(end_node)] = 1

	def del_arc(self, start_node, end_node):
		"""
		Delete a arc
		:param start_node:
		:param end_node:
		"""
		start_node = self.find_node(start_node)
		end_node = self.find_node(end_node)
		if -1 == start_node or -1 == end_node:
			return
		start_node.arcs.remove(end_node)
		self.paths[self.nodes.index(start_node)][self.nodes.index(end_node)] = 0

	def update_graph_arcs(self):
		"""
		Update the adjacency matrix with Nodes arc list
		"""
		paths = []
		for i in self.nodes:
			path = []
			for a in self.nodes:
				if a in i.arcs:
					path.append(1)
				else:
					path.append(0)
			paths.append(path)
		self.paths = paths

	def update_node_arcs(self):
		"""
		Update the Nodes arcs with the adjacency matrix
		"""
		for i in self.nodes:
			i.arcs = []
		a = 0
		while a < len(self.paths):
			b = 0
			while b < len(self.paths):
				if self.paths[a][b] == 1:
					self.nodes[a].new_arc(self.nodes[b])
				b += 1
			a += 1

	def graph_dump(self, save: str):
		"""
		Generate a .graph file where the graph is saved
		:param save: name for the save file
		:return: the save file text
		"""
		self.update_graph_arcs()
		text = "\n"
		for i in self.nodes:
			node = Node()
			node.name = i.name
			node.value = i.value
			node.position = i.position
			node.rotation = i.rotation
			node.type = i.type
			for a in i.arcs:
				node.arcs.append(a.name)
			text = text + "\n" + "@" + json.dumps(node.__dict__)
		text = text + "\n"
		for i in self.paths:
			text = text + "\n" + json.dumps(i)

		file = open(("saves/" + save + ".graph"), "w")  # Creation of personal file for graph
		file.write(text)
		file.close()
		return text

	def graph_load(self, save: str):
		"""
		Load a .graph file in this object ¡Do not create a new one by itself!
		:param save: the addrres or text of the save file
		:return:
		"""
		if save[-7:-1] != ".graph":
			save = open(save).read().splitlines()
		elif save.find("@{"):
			save = save.splitlines()
		else:
			return
		self.nodes = []
		self.paths = []

		for line in save:
			if len(line) == 0:
				continue
			if line[0] == "@":
				json_node = line[1:]
				json_node = json.loads(json_node)
				node = Node()
				node.build(json_node)
				self.nodes.append(node)
			elif line[0] == "[":
				self.paths.append(json.loads(line))
			else:
				pass
		self.update_node_arcs()
		self.update_graph_arcs()

	def sort(self):
		"""
place holder for sort algorithms
		"""
		list_A = self.nodes.copy()
		list_B = self.nodes.copy()
		self.sorted_up = self.quicksort(list_A)
		self.sorted_down = self.mergesort(list_B)
		self.sorted_down
		for a in self.sorted_up:
			print(a.name)

		print("\n")
		for a in self.sorted_down:
			print(a.name)
		pass

	def quicksort(self, list):
		print("Lista: ", list)
		if len(list) == 1 or len(list) == 0:
			return list
		else:
			pivot = list[0].name
			i = 0  # El i es utilizado como contador para cuando aparezca un elemento menor al pivot
			# Recorre la lista
			for j in range(len(list) - 1):
				if list[j + 1].name < pivot:
					list[j + 1], list[i + 1] = list[i + 1], list[j + 1]
					i += 1

			list[0], list[i] = list[i], list[0]  # Intercambiar el pivot por el último elemento menor encontrado
			# Dividir la lista
			firts = self.quicksort(list[:i])
			print("Firts", firts)
			second = self.quicksort(list[i + 1:])
			print("Second", second)
			firts.append(list[i])

		return firts + second

	# Function performs the comparisons and joins the elements to show the result
	def merge(self, left, right):
		result = []
		i, j = 0, 0
		while i < len(left) and j < len(right):
			if left[i].name > right[j].name:
				result.append(left[i])
				i += 1
			else:
				result.append(right[j])
				j += 1
		result += left[i:]
		result += right[j:]
		return result

	# Function that divides the list and points to the middle
	def mergesort(self, list):
		if len(list) <= 1:
			return list
		mid = int(len(list) / 2)
		left = self.mergesort(list[:mid])
		right = self.mergesort(list[mid:])
		return self.merge(left, right)

	def dijkstra(self, group: [], matrix=None):
		if matrix is None:
			matrix = self.paths
		start = group[0]
		end = group[1]
		# the position of the end and the start has importance because it is a Directed Graph:
		start_index = self.nodes.index(start)
		end_index = self.nodes.index(end)
		length = len(self.nodes)
		dist = [10000] * length
		paths_min = [[]] * length
		dist[start_index] = 0
		queue = []

		# get a id for all the nodes with their position in list
		for i in range(length):
			queue.append(i)

		while queue:
			# select the minimum weight and add path
			min = self.dijkstra_min(dist, queue)
			queue.remove(min)
			for i in range(length):
				if matrix[min][i] > 0 and i in queue:
					if dist[min] + matrix[min][i] < dist[i]:
						dist[i] = dist[min] + matrix[min][i]
						paths_min[i] = paths_min[min] + [self.nodes[min]]
			print(paths_min)
		return paths_min[end_index]

	def dijkstra_min(self, dist, queue):
		minimum = 100000
		min_index = -1
		# chose the minimum element
		for i in range(len(dist)):
			if (dist[i] < minimum) and (i in queue):
				minimum = dist[i]
				min_index = i
		return min_index
		pass

#
# """TEST GRAPH"""
#
# graph = Graph()
#
# node1 = Node()
# node1.set_name("one")
# graph.insert_node(node1)
#
# node2 = Node()
# node2.set_name("two")
# graph.insert_node(node2)
#
# node3 = Node()
# node3.set_name("Three")
# graph.insert_node(node3)
#
# node4 = Node()
# node4.set_name("fourth")
# graph.insert_node(node4)
#
# node5 = Node()
# node5.set_name("five")
# graph.insert_node(node5)
#
# graph.new_arc(node1, "two")
# graph.new_arc("two", "one")
# graph.del_arc("two", "one")
# # graph.new_arc("two", "one")
# # graph.new_arc(node3, "one")
# graph.new_arc(node3, node2)
# graph.new_arc(node2, node4)
# graph.new_arc(node4, node1)
# graph.new_arc(node5, "one")
# graph.new_arc(node5, "five")
#
# # print(graph.__dict__)
# # print(graph.graph_dump("graph one"))
# # graph.graph_load("saves/graph one.graph")
# # print(graph.graph_dump("graph one"))
# a = graph.dijkstra([node3, node1])
# print("a")
# print(a)
# for i in a:
# 	print(i.name)
# 	print("A D")
#
# ##
# # one connect to two
# # two connect to one
# # three connect to one and two
# # fourth is not connect to any
# # five is connect to one and five
# ##
