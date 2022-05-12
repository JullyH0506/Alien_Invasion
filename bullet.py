import pygame
from pygame.sprite import Sprite
from random import choice

class Bullet(Sprite):
	"""A class to manage bullets fired from the ship."""

	def __init__(self, ai_game):
		"""Create a bullet object at the ship's current position."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)


	def update(self):
		"""Move the bullet up the screen."""
        # Update the decimal position of the bullet.
		self.y -=self.settings.bullet_speed_factor
		# Update the rect position.
		self.rect.y = self.y 


	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Sprite):
	"""A class to manage bullets fired by the alien."""

	def __init__(self, ai_game):
		"""Create a alien bullet object at a position of a random alien."""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.alien_bullet_color

		# Create a alien bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width,
			self.settings.alien_bullet_height)
		firing_alien = choice(ai_game.aliens.sprites())
		self.rect.midbottom = firing_alien.rect.midbottom

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)


	def update(self):
		"""Move the alien bullet down the screen."""
        # Update the decimal position of the bullet.
		self.y += self.settings.alien_bullet_speed_factor
		# Update the rect position.
		self.rect.y = self.y


	def draw_alien_bullet(self):
		"""Draw the alien bullet to the screen."""
		pygame.draw.ellipse(self.screen, self.color, self.rect)