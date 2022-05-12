import pygame.mixer
import pygame.image

class Settings():
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
        # Screen settings.
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 0, 0)

		# Ship settings.
		self.ship_limit = 3

		# Bullet settings.
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (243, 101, 9)
		self.bullets_allowed = 3

		# Alien bullet settings.
		self.alien_bullet_width = 15
		self.alien_bullet_height = 25
		self.alien_bullet_color = (0, 255, 0)
		self.alien_bullets_allowed = 3

		# Alien settings.
		self.fleet_drop_speed = 10

		# Star settings.
		self.star_speed = 0.5

		# How quickly the game speeds up.
		self.speedup_scale = 1.1
		# How quickly the alien point values increase.
		self.score_scale = 1.5

		# Instruction 'How to play'.
		self.inf = "Use right and left ARROWS to control your ship.Press SPACE to fire.Be CAREFUL: aliens can shoot you.Destroy as many ALIENS as you can.Enter P to play and Q to quit".split(".")

		# Initialize sound effects.
		self._create_sounds()

		# Time to wait for the second click.
		self.DOUBLECLICKTIME = 250

		# Time between alien shots.
		self.TIMEALIENSFIRING = 300

		# Record output settings.
		self.SHOWRECORDCICLES = 35

		self.initialize_dynamic_settings()


	def _create_sounds(self):
		"""Downoload sound effects and dynamic image."""
		# Sound effects.
		self.fire_sound = pygame.mixer.Sound("sounds/whizz.ogg")
		self.fire_sound.set_volume(0.5)
		self.destroy_sound = pygame.mixer.Sound("sounds/fire.ogg")
		self.game_over_sound = pygame.mixer.Sound("sounds/game_over.ogg")
		self.record_sound = pygame.mixer.Sound("sounds/record.ogg")
		self.start_sound = pygame.mixer.Sound("sounds/start.ogg")
		self.lost_sound = pygame.mixer.Sound("sounds/lost.ogg")

		# Dynamic image
		self.sound_image = pygame.image.load("images/sound.png")
		self.no_sound_image = pygame.image.load("images/no_sound.png")


	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3.0
		self.alien_bullet_speed_factor = 1
		self.alien_speed_factor = 1.0

		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring
		self.alien_points = 50
		self.minus_points = 50


	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
		self.minus_points = int(self.minus_points * self.score_scale)