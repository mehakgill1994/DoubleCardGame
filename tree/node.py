import math
import random

class Node:

	def __init__(self, board, move, parent, player):
		self.board = board
		self.move = move
		self.parent = parent
		self.player = player
		self.prune = False