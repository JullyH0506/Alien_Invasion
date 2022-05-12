import pygame.font

class Title():
	"""A class to represent titles."""
	def __init__(self, ai_game, msg):
		"""Initialize title attributes."""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		# Set font and text color.
		self.text_color = (0, 255, 0)
		self.font = pygame.font.SysFont("agencyfb", 85, True)

		self._prep_msg(msg)


	def _prep_msg(self, msg):
		"""Turn msg into a rendered image and set its position."""
		self.msg_image = self.font.render(msg, True, self.text_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.top = self.screen_rect.height/10
		self.msg_image_rect.centerx = self.screen_rect.centerx


	def show_title(self):
		"""Draw title."""
		self.screen.blit(self.msg_image, self.msg_image_rect)