import pygame
from pygame.sprite import Sprite

class Star(Sprite):
	"""A class to represent a single star in the sky."""

	def __init__(self, ai_game):
		"""Initialize star settings."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		# Load the star image and set its rect attribute.
		self.image = pygame.image.load("images/star.bmp")
		self.rect = self.image.get_rect()

		# Start each new star near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# Store the star's exact vertical position.
		self.y = float(self.rect.y)


	def check_dissappeared(self):
		"""Check if the star have disappeared at the screen edge."""
		if self.rect.top > self.screen.get_rect().bottom:
			return True
		else:
			return False


	def update(self):
		"""Update a star position."""
		self.y += self.settings.star_speed
		self.rect.y = self.y