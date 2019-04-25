from card.card import Card
import math
import random
from command.command import Command
from tree.node import Node

class Player:

	EN_LEVEL_3_COUNT = 0
	EN_LEVEL_2_LIST = []

	def __init__(self, name):
		self.name = name
		self.cards = []
		self.assign_cards()
		self.winner = False
		self.is_human = True
	
	def setPlayerStrategy(self, strategy):
		self.strategy = strategy
		
	def assign_cards(self):
		for i in range(12):
			card = Card()
			card.set_player(self)
			self.cards.append(card)

	def get_empty_cards(self):
		cards = []
		for card in self.cards:
			if not card.placed_on_board:
				cards.append(card)

		return cards

	# using this method to append values to an array containing en values for 1 level nodes
	# which is used for tracing
	def append_en_values(self, depth, score, node):
		if depth == 1:
			if not (node.best[1] == math.inf or node.best[1] == -math.inf):
				del Player.EN_LEVEL_2_LIST[-1]
			Player.EN_LEVEL_2_LIST.append(score)

	# update node best values
	def update_node_score(self, score, node, depth, move):
		if self.is_human:
			if score < node.best[1]:
				self.append_en_values(depth, score, node)
				node.best = [move, score]
		else:
			if score > node.best[1]:
				self.append_en_values(depth, score, node)
				node.best = [move, score]

	# prune current node and all the parent nodes 
	def prune_nodes(self, node, parent_score, move, score, parent_node_array, parent_node, depth):
		self.append_en_values(depth, score, node)
		node.prune = True
		node.prune_score = parent_score
		node.best = [move, score]
		for prune_node in parent_node_array:
			if prune_node != parent_node:
				prune_node.best = [node.move, score]

			# parent node and prune node players are same then it can never be pruned, break out of the loop.
			if (parent_node.player.is_human and prune_node.player.is_human) or (not parent_node.player.is_human and not prune_node.player.is_human):
				break
			else:
				prune_node.prune = True
				prune_node.prune_score = parent_score

	def minimax(self, board, depth, cmd, players, is_alpha_beta=False, parent_node = None):
		# human is always minimizing whereas AI is always maximizing
		other_player = players[1] if self == players[0] else players[0]
		ai_player = self if other_player.is_human else other_player

		# create a node for the last command being played
		node = Node(board, cmd, parent_node, self)

		if self.is_human:
			node.best = [None, math.inf]
		else:
			node.best = [None, -math.inf]
		
		if depth == 1:
			board.heuristic_value = board.heuristic(0, cmd)
			#print("level 1 heuristic => " + str(board.heuristic_value))

		#game_finished = board.is_game_finished(self, other_player)
		# use game finish condition for tournament
		if depth == 0 or board.is_game_finished(self, other_player):
			# depth is 0, means we are the required depth so need to increate 
			#the leaf node counter and return en value
			if depth != 0 and board.heuristic_value == None:
				score = board.heuristic(0, cmd)
				# uncomment below line to use the naive heuristic
				#score = board.naive_heuristic(cmd)
			else:
				score = board.heuristic(board.heuristic_value, cmd)
				# uncomment below line to use the naive heuristic
				#score = board.naive_heuristic(cmd)
			Player.EN_LEVEL_3_COUNT += 1
			return [cmd, score]

		for move in Command.returnPossibleMoves(board, self, cmd):
			#print("move:" + move)
			if not node.prune:
				board.play_move(move, self, node)
				next_move, score = other_player.minimax(board, depth - 1, move, players, is_alpha_beta, node)
				board.undo_move(move, node.previous_orientation)
				
				if not node.prune:
					# if alpha beta then compare parent score and prune nodes based on parent and node best values
					if is_alpha_beta:
						if node.parent is not None:
							parent_node_array = []
							parent_node = node.parent
							parent_node_array.append(parent_node)
							while (parent_node.best[1] == math.inf or parent_node.best[1] == -math.inf) and parent_node.parent is not None:
								parent_node = parent_node.parent
								parent_node_array.append(parent_node)

							parent_score = parent_node.best[1]

							if parent_node.player.is_human:
								if not self.is_human and score >= parent_score:
									# prune nodes
									self.prune_nodes(node, parent_score, move, score, parent_node_array, parent_node, depth)
								else:
									self.update_node_score(score, node, depth, move)
							else:
								if self.is_human and score <= parent_score:
									# prune nodes
									self.prune_nodes(node, parent_score, move, score, parent_node_array, parent_node, depth)
								else:
									self.update_node_score(score, node, depth, move)
						else:
							# root node after travering one full depth
							self.update_node_score(score, node, depth, move)
					else:
						self.update_node_score(score, node, depth, move)
			else:
				# node is pruned so we should break and shouldn't check rest of moves
				break

		return node.best