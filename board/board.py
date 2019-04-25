from board.cell import Cell
import random

class Board:

	BOARD_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	BOARD_ROWS = ['1','2','3','4','5','6','7','8','9','10','11','12']
	BOARD_ROWS_TO_INDEX = {'1': 11,'2': 10,'3': 9,'4': 8,'5': 7,'6': 6,'7': 5,'8': 4,'9': 3,'10': 2,'11': 1,'12': 0}
	HEURISTIC_FACTOR_COLOR = 1
	HEURISTIC_FACTOR_DOTS = 1


	def __init__(self):
		# initialize board cells as array of arrays 
		self.cells = []
		self.heuristic_value = None
		for row in reversed(Board.BOARD_ROWS):
			row = []
			for col in Board.BOARD_COLUMNS:
				row.append(Cell())
			self.cells.append(row)
		#array to store the indexes of top most filled cells in every column
		self.top_array = [0, 0, 0, 0, 0, 0, 0, 0]
		self.ai_strategy = None

	@classmethod
	def get_orientation_and_cell_position(cls, command):
		command_list = command.upper().strip().split(" ")
		if command_list[0] == '0':
			orientation = command_list[1]
			cell_position = command_list[2]
		else:
			orientation = command_list[2]
			cell_position = command_list[3]

		return (orientation, cell_position)

	def get_cell(self, row_index, col_index):
		self.cells[row_index][col_index]

	# return cell based on position like A2
	def get_cell_by_string_position(self, position):
		col_index, row_index = self.get_cell_index_by_string_position(position)
		return self.cells[row_index][col_index]

	# return cells row and col indices based on position like A2
	def get_cell_index_by_string_position(self, position):
		col_index = Board.BOARD_COLUMNS.index(position[0])
		row_index = Board.BOARD_ROWS_TO_INDEX[position[1:]]
		return (col_index, row_index)

	def get_row_column_diagonals(self):
		col_len = len(self.cells)
		row_len = len(self.cells[0])
		cols = [[] for i in range(col_len)]
		rows = [[] for i in range(row_len)]
		fdiag = [[] for i in range(col_len + row_len - 1)]
		bdiag = [[] for i in range(len(fdiag))]
		min_bdiag = -col_len + 1

		for y in range(col_len):
			for x in range(row_len):
				cols[y].append(self.cells[y][x])
				rows[x].append(self.cells[y][x])
				fdiag[x+y].append(self.cells[y][x])
				bdiag[-min_bdiag+x-y].append(self.cells[y][x])

		return (cols, rows, fdiag, bdiag)

	def check_consecutive_color_text(self, rows, player1, player2):
		# use this variable, otherwise will have to create different methods
		# to handle the case where both users are winning simultaneously
		game_finished = False

		for row in rows:
			if len(row) > 3:
				for r in range(len(row) - 3):
					if(row[r].text() is not None
						and row[r].text() == row[r+1].text()
						and row[r+1].text() == row[r+2].text()
						and row[r+2].text() == row[r+3].text()
					):
						# same text
						if player1.strategy.lower() == 'dots':
							player1.winner = True
						else:
							player2.winner = True

						game_finished = True

					if(row[r].color() is not None
						and row[r].color() == row[r+1].color()
						and row[r+1].color() == row[r+2].color()
						and row[r+2].color() == row[r+3].color()
					):
						# same color in row
						if player1.strategy.lower() == 'color':
							player1.winner = True
						else:
							player2.winner = True

						game_finished = True

					if game_finished:
						return True

	def is_game_finished(self, player1, player2):
		# check for all rows
		cols, rows, fdiag, bdiag = self.get_row_column_diagonals()

		if(self.check_consecutive_color_text(cols, player1, player2)
			or self.check_consecutive_color_text(rows, player1, player2)
			or self.check_consecutive_color_text(fdiag, player1, player2)
			or self.check_consecutive_color_text(bdiag, player1, player2)
		):
			return True
		else:
			return False


	def get_cells_by_command(self, command):
		orientation, cell_position = Board.get_orientation_and_cell_position(command)
		position1_col_index, position1_row_index = self.get_cell_index_by_string_position(cell_position)

		if orientation in ['1', '3', '5', '7']:
			position2_col_index = position1_col_index + 1
			position2_row_index = position1_row_index
		else:
			position2_col_index = position1_col_index
			position2_row_index = position1_row_index - 1

		return (self.cells[position1_row_index][position1_col_index], self.cells[position2_row_index][position2_col_index])



	def getNeighbouringCells(self, row_index, col_index):
		neighbours = []
		if row_index == 0 and col_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		elif row_index == 11 and col_index == 7:
			neighbours.append("None")
			neighbours.append("None")
		elif row_index == 0 and col_index == 7:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append("None")
		elif row_index == 11 and col_index == 0:
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		elif row_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		elif col_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		elif row_index == 11:
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		elif col_index == 7:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append("None")
		else:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
		
		return neighbours

	# play a move on board
	def play_move(self, cmd, player, node=None):
		cell1, cell2 = self.get_cells_by_command(cmd)
		orientation, cell_position = Board.get_orientation_and_cell_position(cmd)

		if cmd[0] == '0':
			# regular command, get a random card from player cards
			card = random.choice(player.get_empty_cards())
			if node:
				node.previous_orientation = card.orientation
			#update top_array
			index = Board.BOARD_COLUMNS.index(cell_position[0])
			if orientation in ['1', '3', '5', '7']:
				self.top_array[index] = self.top_array[index] + 1
				self.top_array[index+1] = self.top_array[index] + 1
			else:
				self.top_array[index] = self.top_array[index] + 2
		else:
			# recycling command, need to remove mini cards from cell and get card from the cell
			command_list = cmd.upper().strip().split(" ")
			prev_cell1 = self.get_cell_by_string_position(command_list[0])
			prev_cell2 = self.get_cell_by_string_position(command_list[1])

			card = prev_cell1.miniCard.card

			if node:
				node.previous_orientation = card.orientation


			prev_cell1.remove_miniCard()
			prev_cell2.remove_miniCard()


		if orientation in ['1', '4', '5', '8']:
			cell1.set_miniCard(card.miniCard1(orientation), orientation)
			cell2.set_miniCard(card.miniCard2(orientation), orientation)
		else:
			cell1.set_miniCard(card.miniCard2(orientation), orientation)
			cell2.set_miniCard(card.miniCard1(orientation), orientation)

	# undo a move, remove mini card from cells
	def undo_move(self, cmd, previous_orientation=None):
		cell1, cell2 = self.get_cells_by_command(cmd)
		card = cell1.miniCard.card
		cell1.remove_miniCard()
		cell2.remove_miniCard()
		if cmd[0] != '0':
			new_cmd = "0 %s %s" % (previous_orientation, cmd.split(' ')[0])
			self.play_move(new_cmd, card.player)
		

	def __str__(self):
		# represent board in form of a matrix
		output = ""
		for row_index, row in enumerate(reversed(Board.BOARD_ROWS)):
			output += '\n'
			output += "|%2s|" % row
			for col_index, col in enumerate(Board.BOARD_COLUMNS):
				output += "|%17s|" % self.cells[row_index][col_index]

		output += '\n'
		output += '|  |'
		for col in Board.BOARD_COLUMNS:
			output += "|%17s|" % col


		return output


	def compute_EN(self):
		whiteO = 0
		redO = 0
		white0 = 0
		red0 = 0
		for row_index, row in enumerate(Board.BOARD_ROWS):
			for col_index, col in enumerate(Board.BOARD_COLUMNS, 1):
				cell = self.get_cell_by_string_position(col+row)
				if cell.miniCard != None:
					if(cell.miniCard.color == 'white' and cell.miniCard.text == 'O'):
						whiteO+=(10*row_index) + col_index
					if(cell.miniCard.color == 'red' and cell.miniCard.text == 'O'):
						redO+=(10*row_index) + col_index
					if(cell.miniCard.color == 'white' and cell.miniCard.text == '0'):
						white0+=(10*row_index) + col_index
					if(cell.miniCard.color == 'red' and cell.miniCard.text == '0'):
						red0+=(10*row_index) + col_index

		score = whiteO + (3*white0) - (2*red0) - (1.5*redO)	
		score = round(score, 1)	
		return score		

	def heuristic(self, self_heuristic_value, nextCommand=None):
		
		value = self_heuristic_value
		if(self.ai_strategy == 'color'):
			Board.HEURISTIC_FACTOR_COLOR = 1.2
			Board.HEURISTIC_FACTOR_DOTS = 1
		if(self.ai_strategy == 'dots'):
			Board.HEURISTIC_FACTOR_COLOR = 1
			Board.HEURISTIC_FACTOR_DOTS = 1.2

		if not nextCommand:
			#compute heuristic
			cols, rows, fdiag, bdiag = self.get_row_column_diagonals()
			value+=self.compute_CRD_value(cols, 'c')
			value+=self.compute_CRD_value(rows, 'r')
			value+=self.compute_CRD_value(fdiag, 'fd')
			value+=self.compute_CRD_value(bdiag, 'bd')

		else:
			#use selfValue and compute new value by
			# placing newCommand on to the board
			value+=self.compute_CRD_value_proximity(nextCommand)

		return value



	def compute_CRD_value(self, card_lists, type_of_lists):
		total_dots_value = 0
		total_color_value = 0
		return_value = 0
		#heuristic check 1
		#maximizing color and minimizing dots in this check
		#will reverse this order in the end according to AI strategy
		for row in card_lists:
			row_dots_value = 0
			row_color_value = 0
			if len(row) > 3:
				streak_dots = 1
				streak_color = 1
				card_count = 0
				skip = False
				consecutive_empty_cells = False
				for r in range(len(row)-1):
					#check whether cell is empty
					if row[r].text() is not None or not skip:
						consecutive_empty_cells = False
						card_count+=1
						if row[r].text() == row[r-1].text():
							streak_dots+=1
							# if streak_dots > 2:
							# 	if AI_player_strategy == 'color':
							# 		return_value-=150
						else:
							row_dots_value = row_dots_value + self.streak_value(streak_dots)
							streak_dots = 1
						
						if row[r].color() == row[r-1].color():
							streak_color+=1
							# if streak_color > 2:
							# 	if AI_player_strategy == 'dots':
							# 		return_value-=150
						else:
							row_color_value = row_color_value + self.streak_value(streak_color)
							streak_color=1
						
						if type_of_lists == 'r':
							#if row is full, reset value
							#*****RECYCLING NOT CONSIDERED***
							if card_count == 8:
								row_color_value = 0
								row_dots_value = 0
							
						elif type_of_lists == 'c':
							#check only top 4 cards
							if card_count == 4:
								break
				
						elif type_of_lists == 'fd':
							temp = 1
						else:
							temp = 2

					else:
						#check streaks and add or subtract corresponding values to vaule
						if card_count != 0 and not consecutive_empty_cells:
							row_dots_value = row_dots_value + self.streak_value(streak_dots)
							row_color_value = row_color_value + self.streak_value(streak_color)
							streak_dots = 1
							streak_color = 1
							consecutive_empty_cells = True

			total_color_value+=row_color_value
			total_dots_value+=row_dots_value
			
		return_value = (Board.HEURISTIC_FACTOR_COLOR*total_color_value)-(Board.HEURISTIC_FACTOR_DOTS*total_dots_value)
		if self.ai_strategy == 'dots':
			return_value = -1 * return_value
		return return_value

	def streak_value(self, value):
		if value == 1:
			return 2
		elif value == 2:
			return 25
		elif value == 3:
			return 75
		else:
			return 150 

	def compute_CRD_value_proximity(self, cmd):
		value = 0
		#only handling regular moves
		orientation, cell1_position = Board.get_orientation_and_cell_position(cmd)
		cell2_position = None
		orientation_type = None
		if orientation in ['1','3','5','7']:
			cell2_position = chr(ord(cell1_position[0]) + 1)  + cell1_position[1:]
			orientation_type = 'horizontal'
		else:
			cell2_position = cell1_position[0] + str(int(cell1_position[1:]) + 1)
			orientation_type = 'vertical'

		#calculate adjusted values in the proximity of cell 1
		row, col, fd, bd = self.get_nearest_RCDs(cell1_position)
		
		value+=self.calculate_adjusted_streak_value(row)
		value+=self.calculate_adjusted_streak_value(col)
		value+=self.calculate_adjusted_streak_value(fd)
		value+=self.calculate_adjusted_streak_value(bd)

		#calculate adjusted values in the proximity of cell 2
		row, col, fd, bd = self.get_nearest_RCDs(cell2_position)
		
		value+=self.calculate_adjusted_streak_value(row)
		value+=self.calculate_adjusted_streak_value(col)
		value+=self.calculate_adjusted_streak_value(fd)
		value+=self.calculate_adjusted_streak_value(bd)

		return value



	def get_nearest_RCDs(self, position):
		col_index, row_index = self.get_cell_index_by_string_position(position)
		row = []
		col = []
		fd = []
		bd = []
		for i in range(-3, 4):
			if i != 0:
				if col_index+i >= 0 and col_index+i < 8 and row_index+i >= 0 and row_index+i < 12:
					row.append(self.cells[row_index][col_index+i])
					col.append(self.cells[row_index+i][col_index])
					fd.append(self.cells[row_index+i][col_index+i])
					if col_index+i >= 0 and col_index+i < 8 and row_index-i >= 0 and row_index-i < 12:
						bd.append(self.cells[row_index-i][col_index+i])
					else:
						bd.append(None)
				elif col_index+i >= 0 and col_index+i < 8:
					row.append(self.cells[row_index][col_index+i])
					col.append(None)
					fd.append(None)
					bd.append(None)
				elif row_index+i >= 0 and row_index+i < 12:
					col.append(self.cells[row_index+i][col_index])
					row.append(None)
					fd.append(None)
					bd.append(None)
				else:
					row.append(None)
					col.append(None)
					fd.append(None)
					bd.append(None)
			else:
				row.append(self.cells[row_index][col_index])
				col.append(self.cells[row_index][col_index])
				fd.append(self.cells[row_index][col_index])
				bd.append(self.cells[row_index][col_index])
		
		return row, col, fd, bd


	def calculate_adjusted_streak_value(self, row):
		return_value = 0
		return_color_value = 0
		return_dots_value = 0
		target_cell = row[3]
		streak_color_break = False
		streak_dots_break = False
		previous_color_streak_left = 1
		previous_color_streak_right = 1
		previous_dots_streak_left = 1
		previous_dots_streak_right = 1
		new_color_streak = 1
		new_dots_streak = 1

		#left side of target
		for i in range(1, 3):
			if row[3-i] is not None and row[3-i-1] is not None and row[3-i].text() is not None:
				if not streak_dots_break:		
					if row[3-i].text() == row[3-i-1].text():
						previous_dots_streak_left+=1
					else:
						streak_dots_break = True
				if not streak_color_break:		
					if row[3-i].color() == row[3-i-1].color():
						previous_color_streak_left+=1
					else:
						streak_dots_break = True
			else:
				streak_color_break = True
				streak_dots_break = True

		if row[2] is not None:
			if row[3].text() ==  row[2].text():
				return_dots_value+=(Board.HEURISTIC_FACTOR_DOTS*self.streak_value(previous_dots_streak_left))
				new_dots_streak+=previous_dots_streak_left
			if row[3].color() ==  row[2].color():
				return_color_value+=(Board.HEURISTIC_FACTOR_COLOR*self.streak_value(previous_color_streak_left))
				new_color_streak+=previous_color_streak_left

		#right side of target
		streak_color_break = False
		streak_dots_break = False
		for i in range(1, 3):
			if row[3+i] is not None and row[3+i+1] is not None and row[3+i].text() is not None:
				if not streak_dots_break:		
					if row[3+i].text() == row[3+i+1].text():
						previous_dots_streak_right+=1
					else:
						streak_dots_break = True
				if not streak_color_break:		
					if row[3+i].color() == row[3+i+1].color():
						previous_color_streak_right+=1
					else:
						streak_dots_break = True
			else:
				streak_color_break = True
				streak_dots_break = True
		
		if row[4] is not None:
			if row[3].text() ==  row[4].text():
				return_dots_value+=(Board.HEURISTIC_FACTOR_DOTS*self.streak_value(previous_dots_streak_right))
				#handling the case so that the same cell doesnt get included twice
				if new_dots_streak != 1:
					new_dots_streak-=1
				new_dots_streak+=previous_dots_streak_right
			if row[3].color() ==  row[4].color():
				return_color_value+=(Board.HEURISTIC_FACTOR_COLOR*self.streak_value(previous_color_streak_right))
				if new_color_streak != 1:
					new_color_streak-=1
				new_color_streak+=previous_color_streak_right

		if self.ai_strategy == 'color':
			return_value-+return_color_value
			return_value+=return_dots_value
		else:
			return_value+=return_color_value
			return_value-=return_dots_value
			
		return_color_value = 0
		return_dots_value = 0


		if new_dots_streak != 1:
			return_dots_value+=(Board.HEURISTIC_FACTOR_DOTS*self.streak_value(new_dots_streak))
		else:
			return_dots_value+=(Board.HEURISTIC_FACTOR_DOTS*self.streak_value(1))
		
		if new_color_streak != 1:	
			return_color_value+=(Board.HEURISTIC_FACTOR_COLOR*self.streak_value(new_color_streak))
		else:
			return_color_value+=(Board.HEURISTIC_FACTOR_COLOR*self.streak_value(1))
			
		if self.ai_strategy == 'color':
			return_value+=return_color_value
			return_value-=return_dots_value
		else:
			return_value-=return_color_value
			return_value+=return_dots_value

		return return_value

	def getNeighbouringCellsForNaiveHeuristic(self, row_index, col_index):
		neighbours = []
		if row_index == 0 and col_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
		elif row_index == 11 and col_index == 7:
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append("None")
		elif row_index == 0 and col_index == 7:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index+1]))
		elif row_index == 11 and col_index == 0:
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
		elif row_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index+1]))
		elif col_index == 0:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
		elif row_index == 11:
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append("None")
		elif col_index == 7:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append("None")
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index+1]))
		else:
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index+1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index+1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index-1]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index]))
			neighbours.append(self.get_cell_by_string_position(Board.BOARD_COLUMNS[col_index-1] + Board.BOARD_ROWS[row_index+1]))
		
		return neighbours

	def computeNaiveNeighbourValue(self, cell_position):
		value = 0
		target_cell = self.get_cell_by_string_position(cell_position)
		col_index, row_index = self.get_cell_index_by_string_position(cell_position)
		neighbours = self.getNeighbouringCellsForNaiveHeuristic(row_index, col_index)
		for neighbour in neighbours:
			if neighbour != 'None' and neighbour.miniCard:
				if self.ai_strategy == 'color':
					if neighbour.miniCard.color == target_cell.miniCard.color:
						value+=1
				else:
					if neighbour.miniCard.text == target_cell.miniCard.text:
						value+=1
				
		return value


	def naive_heuristic(self, cmd):
		value = 0

		orientation, cell1_position = Board.get_orientation_and_cell_position(cmd)
		cell2_position = None
		orientation_type = None
		if orientation in ['1','3','5','7']:
			cell2_position = chr(ord(cell1_position[0]) + 1)  + cell1_position[1:]
			orientation_type = 'horizontal'
		else:
			cell2_position = cell1_position[0] + str(int(cell1_position[1:]) + 1)
			orientation_type = 'vertical'

		#check for cell 1
		value+=self.computeNaiveNeighbourValue(cell1_position)

		#check for cell 2
		value+=self.computeNaiveNeighbourValue(cell2_position)

		return value