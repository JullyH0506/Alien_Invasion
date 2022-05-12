import sys
from time import sleep
from random import randint
import json

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from star import Star
from button import Button, Instruction, RecordButton
from sound_button import SoundButton, PauseButton, ContinueButton
from title import Title
from ship import Ship
from bullet import Bullet, AlienBullet
from alien import Alien

class AlienInvasion:
	"""Overall class to manage game assets and behavior."""
	
	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.mixer.pre_init(44100, -16, 3, 512)
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width 
		self.settings.screen_height = self.screen.get_rect().height

		pygame.display.set_caption("Alien Invasion")

		# Create an instance to store game statistics,
    # and a scoreboard.
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		# Create an instance of a ship and groups.
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		self.stars = pygame.sprite.Group()
		self.alien_bullets = pygame.sprite.Group()

		# Create stars and an aliens fleet.
		self._create_stars()
		self._create_fleet()

		# Create buttons.
		self._create_buttons()

		# Game title.
		self.game_title = Title(self, "Alien Invasion")
		self.game_over_title = Title(self, "Game Over")

		# Create flags.
		self._create_flags()

		# Check time.
		self.time = pygame.time.Clock()
		self.dbclock = pygame.time.Clock()


	def run_game(self):
		"""Start the main loop for the game."""
		self.settings.start_sound.play()
		while True:
			self._check_events()
			self._update_stars()

			if self.stats.game_active and not self.paused:
				self.ship.update()
				self._update_bullets()
				self._update_alien_bullets()
				self._update_aliens()

			self._update_screen()


	def _create_buttons(self):
		"""Create all buttons."""
		self.play_button = Button(self, "Play")
		self.how_button = Button(self, "How to play")
		self.sound_button = SoundButton(self)
		self.pause_button = PauseButton(self)
		self.continue_button = ContinueButton(self)
		self.record_button = RecordButton(self, "Record")
		self._create_instruction()


	def _create_instruction(self):
		"""Create instruction buttons."""
		inf = self.settings.inf
		self.inst1 = Instruction(self, inf[0])
		self.inst2 = Instruction(self, inf[1])
		self.inst3 = Instruction(self, inf[2])
		self.inst4 = Instruction(self, inf[3])
		self.inst5 = Instruction(self, inf[4])


	def _create_flags(self):
		"""Create flags."""
		self.visible = True
		self.game_over = False
		self.show_inst = False
		self.menu_show = True
		self.draw_record = False  
		self.sounds_playing = True
		self.paused = False
		self.times = 0


	def _check_events(self):
				"""Respond to keypresses and mouse events."""
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self._close_game()
					elif event.type == pygame.KEYDOWN:
						self._check_keydown_events(event)
					elif event.type == pygame.KEYUP:
						self._check_keyup_event(event)
					elif event.type == pygame.MOUSEBUTTONDOWN:
						self._check_mousebuttondown_events(event)


	def _check_play_button(self, mouse_pos):
		"""Start a new game when the player clicks Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self._start_game()


	def _check_sound_button(self, mouse_pos):
		"""Sound control button."""
		button_clicked = self.sound_button.image_rect.collidepoint(mouse_pos)
		# Change the image of a sound button when it is clicked.
		# Change sound flag.
		if button_clicked:
			if self.sounds_playing:
				self.sound_button.image = self.settings.no_sound_image
				self.sounds_playing = False
			else:
				self.sound_button.image = self.settings.sound_image
				self.sounds_playing = True


	def _check_how_button(self, mouse_pos):
		"""Shows intruction buttons when the player clicks How to play."""
		button_clicked = self.how_button.rect.collidepoint(mouse_pos)
		if button_clicked:
			self.show_inst = True
			self.menu_show = False

	def _check_pause_button(self, mouse_pos):
		"""Pause the game when the player clicks Pause"""
		button_clicked = self.pause_button.image_rect.collidepoint(mouse_pos)
		if button_clicked:
			self.paused = True

	def _check_continue_button(self, mouse_pos):
		"""Continue a game when the player clicks Continue"""
		button_clicked = self.continue_button.image_rect.collidepoint(mouse_pos)
		if button_clicked:
			self.paused = False


	def _start_game(self):
		"""Start a new game."""
		# Reset the game statistics.
		self.settings.initialize_dynamic_settings()
		self.stats.reset_stats()
		self.stats.game_active = True
		self.sb.prep_images()

		# Get rid of any remaining aliens and bullets.
		self.aliens.empty()
		self.bullets.empty()

		self.draw_record = False

		# Create a new fleet and center the ship.
		self._create_fleet()
		self.ship.center_ship()

		# Hide the mouse cursor.
		pygame.mouse.set_visible(False)

		# Change the flags.
		self.visible = False
		self.times = 0

		# Pause.
		sleep(0.5)


	def _check_keydown_events(self, event):
		"""Respond to keypresses."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			self._close_game()
		elif event.key == pygame.K_SPACE:
			if self.stats.game_active and self.sounds_playing:
				# Play fire_sound when the player is firing.
				self.settings.fire_sound.play()
			self.fire_bullet()
		elif event.key == pygame.K_p and not self.stats.game_active:
			self._start_game()


	def _check_keyup_event(self, event):
		"""Respond to key releases."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False


	def _check_mousebuttondown_events(self, event):
		"""Respond to mouse clicks."""
		if event.button == 1:
			mouse_pos = pygame.mouse.get_pos()
			if self.dbclock.tick() < self.settings.DOUBLECLICKTIME:
				# If cursor is visible hide it on doubleclick
				# if it isn't show it on doubleclick
				# Change flag.
				if self.visible:
					pygame.mouse.set_visible(False)
					self.visible = False
				else:
					pygame.mouse.set_visible(True)
					self.visible = True
			self._check_sound_button(mouse_pos)
			if self.paused:
				self._check_continue_button(mouse_pos)
			else:
				self._check_play_button(mouse_pos)
				self._check_how_button(mouse_pos)
				self._check_pause_button(mouse_pos)


	def fire_bullet(self):
		"""Create a new bullet and add it to the bullets group."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)


	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
		self.bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_colllisions()


	def _check_bullet_alien_colllisions(self):
		"""Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

			if self.sounds_playing:
				self.settings.destroy_sound.play()
		if not self.aliens:
			self._start_new_level()


	def _start_new_level(self):
		"""Starts a new level."""
		# Destroy existing bullets and create new fleet.
		self.bullets.empty()
		self._create_fleet()
		self.settings.increase_speed()

		# Increase level.
		self.stats.level += 1
		self.sb.prep_level()


	def alien_fire(self):
		"""Create a new alien bullet and add it to the alien_bullets group."""
		if len(self.alien_bullets) < self.settings.alien_bullets_allowed:
			new_bullet = AlienBullet(self)
			self.alien_bullets.add(new_bullet)


	def _update_alien_bullets(self):
		"""Update position of alien bullets and get rid of old bullets."""
		# Update bullet positions.
		self.alien_bullets.update()

		# Get rid of bullets that have disappeared.
		for bullet in self.alien_bullets.copy():
			if bullet.rect.top >= self.settings.screen_height:
				self.alien_bullets.remove(bullet)

		self._check_bullet_ship_collisions()


	def _check_bullet_ship_collisions(self):
		"""Respond to an alien bullet - ship collisions."""
		# Remove any alien bullets that have collided.
		# Do not remove ship.
		collision = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
		if collision:
			self.stats.score -= self.settings.minus_points
			if self.sounds_playing:
				self.settings.lost_sound.play()
			if self.stats.ships_left > 0:
				self.stats.ships_left -= 1
			else:
				self._game_over()
			self.sb.prep_score()
			self.sb.prep_ships()


	def _update_aliens(self): 
		"""
		Check if the fleet is at an edge,
    then update the positions of all aliens in the fleet.
    """
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collisions.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()


	def _create_stars(self):
		"""Create starry sky."""
		# Create a star.
		star = Star(self)
		# Find the number of stars in a row.
		star_width, star_height = star.rect.size
		available_space_x = self.settings.screen_width - (star_width)
		self.number_stars_x = available_space_x // (5 * star_width) + 3

		# Determine the number of rows of stars that fit on the screen.
		avilable_space_y = self.settings.screen_height
		number_rows = avilable_space_y // (5 * star_height)

		for row_number in range(number_rows):
			self._create_row(row_number)


	def _create_row(self, row_number):
		"""Place a star in a row."""
		for star_number in range(self.number_stars_x):
			self._create_star(star_number, row_number)


	def _create_star(self, star_number, row_number):
		"""Create a single star."""
		star = Star(self)
		star_width, star_height = star.rect.size
		star.rect.x = 2 * star_width + 5 * star_width * star_number
		star.y = 2 * star.rect.height + 5 * star.rect.height * row_number
		star.rect.y = star.y
		# Make a little different spacing between stars in a row.
		star.rect.x += randint(-20, 20)

		self.stars.add(star)


	def _update_stars(self):
		"""
		If a row of stars have disappeared at an edge,
		then create a new row and update stars' position.
		"""
		self.stars.update()

		make_new_stars = False
		for star in self.stars.copy():
			if star.check_dissappeared():
				self.stars.remove(star)
				make_new_stars = True

		if make_new_stars:
			self._create_row(0)


	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# Determine the number of rows of aliens that fit on the screen.
		ship_height = self.ship.rect.height
		avilable_space_y = (self.settings.screen_height - 
			(3 * alien_height) - ship_height)
		number_rows = avilable_space_y // (2 * alien_height)

		# Create the full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)


	def _create_alien(self, alien_number, row_number):
		"""Create an alien and place it in the row."""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)


	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break


	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleet's direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1


	def _ship_hit(self):
		"""Respond to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			# Decrement ships_left, and update scoreboard.
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			# Get rid of any remaining aliens and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship.
			self._create_fleet()
			self.ship.center_ship()

			# Pause.
			sleep(0.5)
		else:
			self._game_over()


	def _game_over(self):
		"""Game over."""

		# Play a game_over sound.
		if self.sounds_playing:
				self.settings.game_over_sound.play()

		# Change flags.
		self.stats.game_active = False
		self.game_over = True
		self.menu_show = True

		pygame.mouse.set_visible(True)
		self.visible = True

		# Pause
		sleep(0.5)


	def _check_aliens_bottom(self):
		"""Check if any aliens have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat this the same as if the ship got hit.
				self._ship_hit()
				break


	def _show_instruction(self):
		"""Show instruction buttons."""
		self.inst1.draw_button(self.game_title.msg_image_rect.bottom + 25)
		self.inst2.draw_button(self.inst1.rect.bottom + 25)
		self.inst3.draw_button(self.inst2.rect.bottom + 25)
		self.inst4.draw_button(self.inst3.rect.bottom + 25)
		self.inst5.draw_button(self.inst4.rect.bottom + 25)
		self.play_button.draw_button(self.inst5.rect.bottom + 25)


	def _show_menu(self):
		"""Show menu buttons."""
		self.play_button.draw_button(self.game_title.msg_image_rect.bottom + 150)
		self.how_button.draw_button(self.play_button.rect.bottom + 50)


	def _active_game(self):
		"""Update images on the screen if the game is being played."""
		# Draw images of a ship, aliens and bullets.
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.aliens.draw(self.screen)

		# Aliens are constantly firing at intervals of TIMEALIENSFIRING seconds.
		if self.time.tick() < self.settings.TIMEALIENSFIRING:
			self.alien_fire()

		# Draw alien bullets.
		for alien_bullet in self.alien_bullets.sprites():
			alien_bullet.draw_alien_bullet()

		# Draw the score information.
		self.sb.show_score()
		self._showing_record()

		# Draw pause button.
		self.pause_button.draw_button(10, self.sound_button.image_rect.bottom + 15)


	def _showing_record(self):
		"""Draw record and announce a new record."""
		if self.draw_record and self.times < self.settings.SHOWRECORDCICLES:
			self.record_button.draw_button(self.settings.screen_height/2 - self.record_button.height/2)
			self.times += 1
			if self.times > self.settings.SHOWRECORDCICLES:
				self.times = self.settings.SHOWRECORDCICLES


	def _unactive_game(self):
		"""Draw images on the screen when a game is not being played."""
		# Show Game Over title if the player lost.
		if self.game_over:
			self.game_over_title.show_title()
		else:
			self.game_title.show_title()

		# Show menu.
		if self.menu_show:
			self._show_menu()

		#Show instruction.
		if self.show_inst and not self.menu_show:
			self._show_instruction()


	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.stars.draw(self.screen)

		if self.stats.game_active:
			if not self.paused:
				self._active_game()
			else:
				self.game_title.show_title()
				self.continue_button.draw_button(self.settings.screen_width/2 - self.continue_button.image_rect.width,
				 self.settings.screen_height/2 - self.continue_button.image_rect.height)

		if not self.stats.game_active:
			self._unactive_game()

		self.sound_button.draw_button(10, self.ship.rect.width + 15)

		pygame.display.flip()


	def _close_game(self):
		"""Save a record and close the game."""
		saved_high_score = self.stats.get_saved_high_score()
		if self.stats.high_score > saved_high_score:
			with open("high_score.json", 'w') as f:
				json.dump(self.stats.high_score, f)

		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()