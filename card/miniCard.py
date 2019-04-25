class MiniCard:
	def __init__(self):
		self.cell = None
		self.color = None
		self.text = None
		self.card = None

	def set_color(self, color):
		self.color = color

	def set_card(self, card):
		self.card = card

	def set_text(self, text):
		self.text = text
		
	def set_cell(self, cell):
		self.cell = cell
		cell.miniCard = self
		self.card.placed_on_board = True

	def __str__(self):
		return "%s(%s)(%s/%s)" % (self.text, self.color, self.card.id, self.card.orientation)