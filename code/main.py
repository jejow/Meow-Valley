import pygame, sys
from settings import *
from level import Level
from menu import MainMenu, SettingsMenu, PauseMenu, Notification
from game_state import GameState

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Meow Valley')
		self.clock = pygame.time.Clock()
		
		# Game states
		self.state = 'main_menu'  # main_menu, playing, settings, paused
		self.level = None
		
		# Menus
		self.main_menu = MainMenu()
		self.settings_menu = SettingsMenu()
		self.pause_menu = PauseMenu()
		self.notification = Notification()
		
		# Save system
		self.game_state = GameState()
		
		# Sound settings
		self.music_volume = 0.5
		self.sound_volume = 0.5
		
		# Input tracking
		self.esc_pressed = False
		self.esc_timer = 0
		self.input_cooldown = 0.2  # seconds
	
	def start_new_game(self):
		"""Start a new game"""
		self.level = Level()
		self.apply_sound_settings()
		self.state = 'playing'
	
	def load_game(self):
		"""Load a saved game"""
		if not self.game_state.save_exists():
			self.notification.show("No save file found!")
			return False
		
		game_data = self.game_state.load_game()
		if game_data:
			self.level = Level()
			self.game_state.apply_loaded_data(game_data, self.level.player, self.level)
			self.apply_sound_settings()
			self.state = 'playing'
			self.notification.show("Game loaded successfully!")
			return True
		self.notification.show("Failed to load game!")
		return False
	
	def save_game(self):
		"""Save current game"""
		if self.level:
			success = self.game_state.save_game(self.level.player, self.level)
			if success:
				self.notification.show("Game saved!")
			else:
				self.notification.show("Failed to save game!")
			return success
		return False
	
	def apply_sound_settings(self):
		"""Apply sound settings to the game"""
		if self.level and hasattr(self.level, 'music'):
			self.level.music.set_volume(self.music_volume)
		if self.level and hasattr(self.level, 'success'):
			self.level.success.set_volume(self.sound_volume)
	
	def handle_main_menu(self):
		"""Handle main menu logic"""
		action = self.main_menu.update()
		
		if action == 'New Game':
			self.start_new_game()
			self.main_menu.selected_action = None
		
		elif action == 'Load Game':
			if not self.load_game():
				print("Could not load game. Starting new game instead.")
				self.start_new_game()
			self.main_menu.selected_action = None
		
		elif action == 'Settings':
			self.state = 'settings'
			self.settings_menu.active = True
			self.main_menu.selected_action = None
		
		elif action == 'Quit':
			pygame.quit()
			sys.exit()
	
	def handle_settings_menu(self):
		"""Handle settings menu logic"""
		music_vol, sound_vol = self.settings_menu.update()
		self.music_volume = music_vol
		self.sound_volume = sound_vol
		
		if not self.settings_menu.active:
			# Return to appropriate state
			if hasattr(self, 'state') and self.state == 'settings_from_pause':
				self.state = 'paused'
			else:
				self.state = 'main_menu'
			
			if self.level:
				self.apply_sound_settings()
	
	def handle_playing(self, dt):
		"""Handle gameplay logic"""
		self.esc_timer += dt
		keys = pygame.key.get_pressed()
		
		# Check ESC key with proper debouncing
		if keys[pygame.K_ESCAPE]:
			if not self.esc_pressed and self.esc_timer > self.input_cooldown:
				if not self.level.shop_active:
					self.state = 'paused'
					self.pause_menu.active = True
					self.pause_menu.esc_was_pressed = True  # Prevent immediate close
					self.esc_pressed = True
					self.esc_timer = 0
					return
		else:
			self.esc_pressed = False
		
		# Save game with F5
		if keys[pygame.K_F5]:
			self.save_game()
		
		self.level.run(dt)
		self.notification.update(dt)
	
	def handle_paused(self, dt):
		"""Handle pause menu logic"""
		self.esc_timer += dt
		
		# Draw the game underneath
		self.level.display_surface.fill('black')
		self.level.all_sprites.custom_draw(self.level.player)
		self.level.overlay.display()
		
		# Draw pause menu on top
		action = self.pause_menu.update()
		
		# Update and show notifications
		self.notification.update(dt)
		
		# Reset ESC press state when key is released
		keys = pygame.key.get_pressed()
		if not keys[pygame.K_ESCAPE]:
			self.esc_pressed = False
		
		if action == 'Resume':
			self.state = 'playing'
			self.pause_menu.active = False
			self.esc_timer = 0
			self.esc_pressed = True  # Prevent immediate re-pause
		
		elif action == 'Save Game':
			self.save_game()
		
		elif action == 'Settings':
			self.state = 'settings_from_pause'
			self.settings_menu.active = True
		
		elif action == 'Main Menu':
			# Auto-save before returning to menu
			self.save_game()
			self.state = 'main_menu'
			self.pause_menu.active = False
			self.esc_pressed = False

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					# Auto-save on quit
					if self.state == 'playing':
						self.save_game()
					pygame.quit()
					sys.exit()
  
			dt = self.clock.tick() / 1000
			
			if self.state == 'main_menu':
				self.handle_main_menu()
			elif self.state == 'settings' or self.state == 'settings_from_pause':
				self.handle_settings_menu()
			elif self.state == 'playing':
				self.handle_playing(dt)
			elif self.state == 'paused':
				self.handle_paused(dt)
			
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()