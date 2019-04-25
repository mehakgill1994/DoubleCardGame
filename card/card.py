from card.miniCard import MiniCard 

class Card:

	id = 1

	def __init__(self):
		self.id = Card.id
		Card.id += 1

		mini1 = MiniCard()
		mini1.set_color('red')
		mini1.set_text('0')
		mini1.set_card(self)

		mini2 = MiniCard()
		mini2.set_color('white')
		mini2.set_text('O')
		mini2.set_card(self)

		mini3 = MiniCard()
		mini3.set_color('red')
		mini3.set_text('O')
		mini3.set_card(self)

		mini4 = MiniCard()
		mini4.set_color('white')
		mini4.set_text('0')
		mini4.set_card(self)

		self.mini_cards = [mini1, mini2, mini3, mini4]
		self.placed_on_board = False
		self.orientation = None



	def set_player(self, player):
		self.player = player

	def miniCard1(self, orientation=None):
		if orientation and orientation in ['5', '6', '7', '8']:
			return self.mini_cards[2]
		else:
			return self.mini_cards[0]

	def miniCard2(self, orientation=None):
		if orientation and orientation in ['5', '6', '7', '8']:
			return self.mini_cards[3]
		else:
			return self.mini_cards[1]