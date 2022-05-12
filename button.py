import pygame.font

class Button():
	"""A class that represents a button."""
	def __init__(self, ai_game, msg):
		"""Initialize button attributes."""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		self.msg = msg

		# Set the dimensions and properties of the button.
		self.width, self.height = (25/128)*self.screen_rect.width, (25/216) * self.screen_rect.height
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont("agencyfb", 48, True)


	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and center text on the button."""
		self.msg_image = self.font.render(msg, True, self.text_color,
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center


	def draw_button(self, pos_y):
		# Draw blank button and then draw message.

		# Create a button rect and then center it.
		self.rect = pygame.Rect(0, pos_y, self.width, self.height)

		self.rect.centerx = self.screen_rect.centerx

		# Button message is created only once.
		self._prep_msg(self.msg)

		pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=20)
		self.screen.blit(self.msg_image, self.msg_image_rect)


class Instruction(Button):
	"""A class that represents an instruction button. Inherits from Button class."""

	def __init__(self, ai_game, msg):
		super().__init__(ai_game, msg)
		self.width, self.height = self.screen_rect.width/2, (25/288) * self.screen_rect.height
		self.button_color = (155, 158, 237)
		self.font = pygame.font.SysFont("agencyfb", 40, True)


class RecordButton(Button):
	"""A class that represents a button about a new record. Inherits from Button class."""

	def __init__(self, ai_game, msg):
		super().__init__(ai_game, msg)
		self.button_color = (255, 220, 0)