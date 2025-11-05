import pygame
from settings import *
from timer import Timer
from support import load_font

class Menu:
	def __init__(self, player, toggle_menu):

		# general setup
		self.player = player
		self.toggle_menu = toggle_menu
		self.display_surface = pygame.display.get_surface()
		self.font = load_font('../font/LycheeSoda.ttf', 30)

		# options
		self.width = 400
		self.space = 10
		self.padding = 8

		# entries
		self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
		self.sell_border = len(self.player.item_inventory) - 1
		self.setup()

		# movement
		self.index = 0
		self.timer = Timer(200)

	def display_money(self):
		text_surf = self.font.render(f'${self.player.money}', False, 'Black')
		text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2,SCREEN_HEIGHT - 20))

		pygame.draw.rect(self.display_surface,'White',text_rect.inflate(10,10),0,4)
		self.display_surface.blit(text_surf,text_rect)

	def setup(self):

		# create the text surfaces
		self.text_surfs = []
		self.total_height = 0

		for item in self.options:
			text_surf = self.font.render(item, False, 'Black')
			self.text_surfs.append(text_surf)
			self.total_height += text_surf.get_height() + (self.padding * 2)

		self.total_height += (len(self.text_surfs) - 1) * self.space
		self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
		self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2,self.menu_top,self.width,self.total_height)

		# buy / sell text surface
		self.buy_text = self.font.render('buy',False,'Black')
		self.sell_text =  self.font.render('sell',False,'Black')

	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()

		if keys[pygame.K_ESCAPE]:
			self.toggle_menu()

		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.index -= 1
				self.timer.activate()

			if keys[pygame.K_DOWN]:
				self.index += 1
				self.timer.activate()

			if keys[pygame.K_SPACE]:
				self.timer.activate()

				# get item
				current_item = self.options[self.index]

				# sell
				if self.index <= self.sell_border:
					if self.player.item_inventory[current_item] > 0:
						self.player.item_inventory[current_item] -= 1
						self.player.money += SALE_PRICES[current_item]

				# buy
				else:
					seed_price = PURCHASE_PRICES[current_item]
					if self.player.money >= seed_price:
						self.player.seed_inventory[current_item] += 1
						self.player.money -= PURCHASE_PRICES[current_item]

		# clamo the values
		if self.index < 0:
			self.index = len(self.options) - 1
		if self.index > len(self.options) - 1:
			self.index = 0

	def show_entry(self, text_surf, amount, top, selected):

		# background
		bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding * 2))
		pygame.draw.rect(self.display_surface, 'White',bg_rect, 0, 4)

		# text
		text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20,bg_rect.centery))
		self.display_surface.blit(text_surf, text_rect)

		# amount
		amount_surf = self.font.render(str(amount), False, 'Black')
		amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20,bg_rect.centery))
		self.display_surface.blit(amount_surf, amount_rect)

		# selected
		if selected:
			pygame.draw.rect(self.display_surface,'black',bg_rect,4,4)
			if self.index <= self.sell_border: # sell
				pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.sell_text,pos_rect)
			else: # buy
				pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
				self.display_surface.blit(self.buy_text,pos_rect)

	def update(self):
		self.input()
		self.display_money()

		for text_index, text_surf in enumerate(self.text_surfs):
			top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
			amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
			amount = amount_list[text_index]
			self.show_entry(text_surf, amount, top, self.index == text_index)

class MainMenu:
	def __init__(self):
		# general setup
		self.display_surface = pygame.display.get_surface()
		self.font_large = load_font('../font/LycheeSoda.ttf', 50)
		self.font = load_font('../font/LycheeSoda.ttf', 30)
		
		# menu options
		self.options = ['New Game', 'Load Game', 'Settings', 'Quit']
		self.index = 0
		self.timer = Timer(200)
		
		# states
		self.active = True
		self.in_settings = False
		self.selected_action = None
		
		# sound settings
		self.sound_volume = 0.5
		self.music_volume = 0.5
		
	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()
		
		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.index = (self.index - 1) % len(self.options)
				self.timer.activate()
			
			if keys[pygame.K_DOWN]:
				self.index = (self.index + 1) % len(self.options)
				self.timer.activate()
			
			if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
				self.timer.activate()
				self.selected_action = self.options[self.index]
				
			if keys[pygame.K_ESCAPE] and self.in_settings:
				self.in_settings = False
				self.timer.activate()
	
	def draw_title(self):
		title = self.font_large.render('Meow Valley', False, 'White')
		title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 100))
		self.display_surface.blit(title, title_rect)
	
	def draw_menu_options(self):
		start_y = SCREEN_HEIGHT / 2 - 50
		
		for i, option in enumerate(self.options):
			color = 'Yellow' if i == self.index else 'White'
			text = self.font.render(option, False, color)
			text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, start_y + i * 50))
			
			# Draw selection indicator
			if i == self.index:
				pygame.draw.rect(self.display_surface, 'Yellow', 
								text_rect.inflate(20, 10), 3, 5)
			
			self.display_surface.blit(text, text_rect)
	
	def update(self):
		if not self.in_settings:
			self.input()
			self.display_surface.fill('black')
			self.draw_title()
			self.draw_menu_options()
		
		return self.selected_action

class SettingsMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = load_font('../font/LycheeSoda.ttf', 30)
		self.font_small = load_font('../font/LycheeSoda.ttf', 20)
		
		# settings
		self.music_volume = 50  # 0-100
		self.sound_volume = 50  # 0-100
		
		# menu
		self.options = ['Music Volume', 'Sound Volume', 'Back']
		self.index = 0
		self.timer = Timer(200)
		self.active = False
	
	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()
		
		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.index = (self.index - 1) % len(self.options)
				self.timer.activate()
			
			if keys[pygame.K_DOWN]:
				self.index = (self.index + 1) % len(self.options)
				self.timer.activate()
			
			# Adjust volumes
			if self.index == 0:  # Music Volume
				if keys[pygame.K_LEFT] and self.music_volume > 0:
					self.music_volume -= 5
					self.timer.activate()
				if keys[pygame.K_RIGHT] and self.music_volume < 100:
					self.music_volume += 5
					self.timer.activate()
			
			elif self.index == 1:  # Sound Volume
				if keys[pygame.K_LEFT] and self.sound_volume > 0:
					self.sound_volume -= 5
					self.timer.activate()
				if keys[pygame.K_RIGHT] and self.sound_volume < 100:
					self.sound_volume += 5
					self.timer.activate()
			
			if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
				if self.index == 2:  # Back
					self.active = False
					self.timer.activate()
			
			if keys[pygame.K_ESCAPE]:
				self.active = False
				self.timer.activate()
	
	def draw_volume_bar(self, y_pos, volume):
		bar_width = 200
		bar_height = 20
		bar_x = SCREEN_WIDTH / 2 + 50
		
		# Background bar
		bg_rect = pygame.Rect(bar_x, y_pos - bar_height / 2, bar_width, bar_height)
		pygame.draw.rect(self.display_surface, 'Gray', bg_rect, 0, 3)
		
		# Volume bar
		fill_width = (volume / 100) * bar_width
		fill_rect = pygame.Rect(bar_x, y_pos - bar_height / 2, fill_width, bar_height)
		pygame.draw.rect(self.display_surface, 'Green', fill_rect, 0, 3)
		
		# Border
		pygame.draw.rect(self.display_surface, 'White', bg_rect, 2, 3)
		
		# Volume percentage
		vol_text = self.font_small.render(f'{int(volume)}%', False, 'White')
		vol_rect = vol_text.get_rect(midleft=(bar_x + bar_width + 20, y_pos))
		self.display_surface.blit(vol_text, vol_rect)
	
	def update(self):
		self.input()
		self.display_surface.fill('black')
		
		# Title
		title = self.font.render('Settings', False, 'White')
		title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 100))
		self.display_surface.blit(title, title_rect)
		
		# Options
		start_y = SCREEN_HEIGHT / 2 - 50
		
		for i, option in enumerate(self.options):
			color = 'Yellow' if i == self.index else 'White'
			text = self.font.render(option, False, color)
			
			if i < 2:  # Volume options
				text_rect = text.get_rect(midright=(SCREEN_WIDTH / 2 - 10, start_y + i * 60))
			else:  # Back option
				text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, start_y + i * 60 + 20))
			
			self.display_surface.blit(text, text_rect)
			
			# Draw volume bars
			if i == 0:
				self.draw_volume_bar(start_y, self.music_volume)
			elif i == 1:
				self.draw_volume_bar(start_y + 60, self.sound_volume)
			
			# Selection indicator
			if i == self.index and i < 2:
				hint = self.font_small.render('< Use Arrow Keys >', False, 'Gray')
				hint_rect = hint.get_rect(center=(SCREEN_WIDTH / 2, start_y + i * 60 + 30))
				self.display_surface.blit(hint, hint_rect)
		
		return self.music_volume / 100, self.sound_volume / 100

class PauseMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font_large = load_font('../font/LycheeSoda.ttf', 50)
		self.font = load_font('../font/LycheeSoda.ttf', 30)
		
		# menu options
		self.options = ['Resume', 'Save Game', 'Settings', 'Main Menu']
		self.index = 0
		self.timer = Timer(150)  # Reduced timer for better responsiveness
		self.active = False
		self.selected_action = None
		
		# Track ESC key state
		self.esc_was_pressed = True  # Start as True to prevent immediate close
	
	def input(self):
		keys = pygame.key.get_pressed()
		self.timer.update()
		
		if not self.timer.active:
			if keys[pygame.K_UP]:
				self.index = (self.index - 1) % len(self.options)
				self.timer.activate()
			
			if keys[pygame.K_DOWN]:
				self.index = (self.index + 1) % len(self.options)
				self.timer.activate()
			
			if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
				self.timer.activate()
				self.selected_action = self.options[self.index]
			
			# Only trigger ESC if it was released and pressed again
			if keys[pygame.K_ESCAPE]:
				if not self.esc_was_pressed:
					self.selected_action = 'Resume'
					self.timer.activate()
					self.esc_was_pressed = True
			else:
				self.esc_was_pressed = False
	
	def update(self):
		self.input()
		
		# Semi-transparent overlay
		overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
		overlay.set_alpha(128)
		overlay.fill('black')
		self.display_surface.blit(overlay, (0, 0))
		
		# Title
		title = self.font_large.render('Paused', False, 'White')
		title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 150))
		self.display_surface.blit(title, title_rect)
		
		# Menu options
		start_y = SCREEN_HEIGHT / 2 - 50
		
		for i, option in enumerate(self.options):
			color = 'Yellow' if i == self.index else 'White'
			text = self.font.render(option, False, color)
			text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, start_y + i * 50))
			
			# Draw selection indicator
			if i == self.index:
				pygame.draw.rect(self.display_surface, 'Yellow', 
								text_rect.inflate(20, 10), 3, 5)
			
			self.display_surface.blit(text, text_rect)
		
		# Instructions
		hint = pygame.font.Font(None, 24).render('Press ESC to resume', False, 'Gray')
		hint_rect = hint.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))
		self.display_surface.blit(hint, hint_rect)
		
		action = self.selected_action
		self.selected_action = None
		return action

class Notification:
	"""Shows temporary notifications to the player"""
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = load_font('../font/LycheeSoda.ttf', 25)
		self.messages = []  # List of (message, time_remaining)
		self.message_duration = 2.0  # seconds
	
	def show(self, message):
		"""Add a new notification message"""
		self.messages.append([message, self.message_duration])
	
	def update(self, dt):
		"""Update and display notifications"""
		# Update timers
		self.messages = [[msg, time - dt] for msg, time in self.messages if time > 0]
		
		# Display messages
		y_offset = 50
		for message, time_remaining in self.messages:
			# Fade out effect
			alpha = min(255, int(255 * (time_remaining / self.message_duration)))
			
			text_surf = self.font.render(message, False, 'White')
			text_surf.set_alpha(alpha)
			text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, y_offset))
			
			# Background
			bg_rect = text_rect.inflate(20, 10)
			bg_surf = pygame.Surface(bg_rect.size)
			bg_surf.set_alpha(alpha // 2)
			bg_surf.fill('black')
			
			self.display_surface.blit(bg_surf, bg_rect)
			self.display_surface.blit(text_surf, text_rect)
			
			y_offset += 40

