from card.card import Card
from player.player import Player
from command.command import Command
from board.board import Board
import time

def main():
	players = []
	p1 = Player('player1')
	p2 = Player('player2')

	players.extend([p1,p2])

	board = Board()

	NORMAL_DEPTH_LEVEL = 3
	RECYCLE_DEPTH_LEVEL = 2
	GAME_DRAW_COUNT = 40

	# set if player is human or AI
	is_human = input("Is player1 human? Enter yes or no\n")
	if is_human.upper() == "YES":
		p1.is_human = True
		p2.is_human = False
	else:
		p1.is_human = False
		p2.is_human = True
	
	#set strategy
	if p1.is_human:
		value = input("Enter player1's strategy (dots or color)\n")
		
		while value.upper() not in ["DOTS", "COLOR"]:
			value = input("Enter player1's strategy (dots or color)\n")
	else:
		value = "color"
		print("Player1 choosen strategy %s \n" % value)
	
	p1.strategy = value
	if value == 'dots':
		p2.strategy = 'color'
	else:
		p2.strategy = 'dots'

	if p1.is_human:
		board.ai_strategy = p2.strategy
	else:
		board.ai_strategy = p1.strategy

	game_completed = False

	# set if want to use alpha beta or minimax
	is_alpha_beata = input("Do you want to use alpha beta?\n")
	if is_alpha_beata.upper() == "YES":
		is_alpha_beata = True
	else:
		is_alpha_beata = False

	# set if want to read commands from a file
	read_file = input("Do you want to read input from a file? Enter yes, to read from file\n")
	read_file = read_file.upper() == 'YES'
	if read_file:
		file = open('sampleCommand.txt')

	# set if want to trace the result in a file
	new_file = None
	trace_result = input("Do you want to trace the result?\n")
	trace_result = trace_result.upper() == 'YES'
	if trace_result:
		new_file_name = input("enter file name\n")
		new_file = open(new_file_name, "w")

	cmd = ''
	score = None

	# using this counter intelligently to print spaces in trace file
	counter = 0
	moves_played_count = 0
	current_move_start_time = None
	current_move_end_time = None

	while not game_completed and moves_played_count < GAME_DRAW_COUNT:
		# reset static variables to trace result of each iteration
		Player.EN_LEVEL_3_COUNT = 0
		Player.EN_LEVEL_2_LIST = []
		board.heuristic_value = None
		for player in players:
			moves_played_count += 1
			
			if moves_played_count > 24:
				depth_level = RECYCLE_DEPTH_LEVEL
			else:
				depth_level = NORMAL_DEPTH_LEVEL

			print(str(board))
			possibleMoves = Command.returnPossibleMoves(board, player, cmd)

			if not read_file:
				if player.is_human:
					print("Player : %s's turn, please enter a valid command to place a card" % player.name)
					cmd = input("$$ ").strip().upper()
				else:
					#player is AI and we need to find appropriate command automatically for AI player
					cmd, score = player.minimax(board, depth_level, cmd, players, is_alpha_beata)
					print("======== AI move: %s =======" % cmd)
					
					# write content in the trace file
					if not player.is_human and new_file:
						if counter != 0:
							new_file.write("\n\n")

						new_file.write("%s\n"%Player.EN_LEVEL_3_COUNT)
						new_file.write("%s"%score)
						new_file.write("\n")
						for en in Player.EN_LEVEL_2_LIST:
							new_file.write("\n%s"%en)
			else:
				# read commands from the file
				new_cmd = file.readline().strip().upper()
				if new_cmd == '':
					# end of file is reached, close the file and exit program
					file.close()
					read_file = False
					
					# continue normal flow of game by asking user to input command
					if player.is_human:
						print("Player : %s's turn, please enter a valid command to place a card" % player.name)
						cmd = input("$$ ").strip().upper()
					else:
						#player is AI and we need to find appropriate command automatically for AI player
						cmd, score = player.minimax(board, depth_level, cmd, players, is_alpha_beata)
						print("======== AI move: %s =======" % cmd)
						
						# write content in the trace file
						if not player.is_human and new_file:
							if counter != 0:
								new_file.write("\n\n")

							new_file.write("%s\n"%Player.EN_LEVEL_3_COUNT)
							new_file.write("%s"%score)
							new_file.write("\n")
							for en in Player.EN_LEVEL_2_LIST:
								new_file.write("\n%s"%en)
				else:
					# need to use this new_cmd temporary variable because we need to keep track of the previous command
					# and if end of file is reached it replaces it with empty string
					cmd = new_cmd		
			
			# if command is not valid then ask user to play the command again
			if player.is_human:
				while cmd not in possibleMoves:				
					if not read_file:
						# invalid command while manually entering values, allow user to input again
						print("invalid command, try again")
						cmd = input("$$ ").strip().upper()
					else:
						# invalid command from the file, close the file and exit program
						print("invalid command %s" % cmd)
						file.close()
						exit()
			else:
				if cmd not in possibleMoves:
					# invalid command by AI, close all files and terminate program
					print("invalid command by AI player so finish the game.")
					if read_file:
						file.close()
					if new_file:
						new_file.close()
					exit()
				
			# play move
			board.play_move(cmd, player)

			if player.is_human:
				current_move_start_time = time.time()
			else:
				current_move_end_time = time.time()

			if current_move_start_time and current_move_end_time and (current_move_end_time > current_move_start_time):
				print("===== Time for next move ============= %s =======" % (current_move_end_time - current_move_start_time + .5))

			# if game is finished, print winner
			if board.is_game_finished(p1, p2):
				if p1.winner and p2.winner:
					print("Player : %s won the game" % player.name)
				elif p1.winner:
					print("Player : %s won the game" % p1.name)
				else:
					print("Player : %s won the game" % p2.name)

				game_completed = True
				break

			# if game draw count reaches
			if moves_played_count == GAME_DRAW_COUNT:
				print("=== Game Draw ===")
				break

		
		# increase counter so need to print empty spaces above
		if not read_file:
			counter += 1

	# close file resources and print board in the end
	if read_file:
		file.close()
	if new_file:
		new_file.close()
	print(str(board))

main()