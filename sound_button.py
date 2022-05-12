import pygame.image

class SoundButton():
	"""A class that represents a sound button."""

	def __init__(self, ai_game):
		"""Initialize all settings."""
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()

		self.image = pygame.image.load("images/sound.png")
		self.image_rect = self.image.get_rect()


	def draw_button(self, x, y):
		"""Draw button."""
		self.image_rect.x = x
		self.image_rect.y = y
		self.screen.blit(self.image, self.image_rect)

class PauseButton(SoundButton):
	"""A class that represents a pause button. Inherits from SoundButton."""
	def __init__(self, ai_game):
		super().__init__(ai_game)
		self.image = pygame.image.load("images/pause.bmp")

class ContinueButton(SoundButton):
	"""A class that represents a continue button. Inherits from SoundButton."""
	def __init__(self, ai_game):
		super().__init__(ai_game)
		self.image = pygame.image.load("images/continue.bmp")
		self.image_rect = self.image.get_rect()
	def draw_button(self):
		self.image_rect.center = self.screen_rect.center 
		self.screen.blit(self.image, self.image_rect)