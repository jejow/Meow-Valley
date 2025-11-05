import json
import os
import pygame
from settings import LAYERS, TILE_SIZE

class GameState:
	"""Manages saving and loading game state"""
	
	def __init__(self):
		self.save_dir = '../saves'
		self.save_file = 'savegame.json'
		self.ensure_save_directory()
	
	def ensure_save_directory(self):
		"""Create saves directory if it doesn't exist"""
		if not os.path.exists(self.save_dir):
			os.makedirs(self.save_dir)
	
	def save_game(self, player, level):
		"""Save current game state"""
		try:
			game_data = {
				'player': {
					'pos': [player.pos.x, player.pos.y],
					'direction': [player.direction.x, player.direction.y],
					'status': player.status,
					'frame_index': player.frame_index,
					'money': player.money,
					'item_inventory': player.item_inventory,
					'seed_inventory': player.seed_inventory,
					'selected_tool': player.selected_tool,
					'selected_seed': player.selected_seed,
					'tool_index': player.tool_index,
					'seed_index': player.seed_index,
					'sleep': player.sleep,
					'timers': self.serialize_timers(player.timers),
				},
				'level': {
					'raining': level.raining,
					'sky_color': level.sky.start_color,
					'soil_grid': self.serialize_soil_grid(level.soil_layer),
					'plants': self.serialize_plants(level.soil_layer.plant_sprites),
					'trees': self.serialize_trees(level.tree_sprites),
					'water_tiles': self.serialize_water_tiles(level.soil_layer.water_sprites),
					'transition': {
						'color': level.transition.color,
						'speed': level.transition.speed
					}
				},
				'meta': {
					'save_time': pygame.time.get_ticks(),
					'version': '1.0'
				}
			}
			
			save_path = os.path.join(self.save_dir, self.save_file)
			with open(save_path, 'w') as f:
				json.dump(game_data, f, indent=4)
			
			return True
		except Exception as e:
			print(f"Error saving game: {e}")
			import traceback
			traceback.print_exc()
			return False
	
	def load_game(self):
		"""Load saved game state"""
		try:
			save_path = os.path.join(self.save_dir, self.save_file)
			
			if not os.path.exists(save_path):
				return None
			
			with open(save_path, 'r') as f:
				game_data = json.load(f)
			
			return game_data
		except Exception as e:
			print(f"Error loading game: {e}")
			import traceback
			traceback.print_exc()
			return None
	
	def save_exists(self):
		"""Check if a save file exists"""
		save_path = os.path.join(self.save_dir, self.save_file)
		return os.path.exists(save_path)
	
	def serialize_soil_grid(self, soil_layer):
		"""Convert soil grid to serializable format"""
		serialized = []
		for row in soil_layer.grid:
			serialized_row = []
			for cell in row:
				if cell and len(cell) > 0:
					# cell is a list in the original code
					serialized_row.append(cell if isinstance(cell, list) else list(cell))
				else:
					serialized_row.append([])
			serialized.append(serialized_row)
		return serialized
	
	def serialize_plants(self, plant_sprites):
		"""Convert plant sprites to serializable format"""
		plants = []
		if plant_sprites:
			for plant in plant_sprites.sprites():
				plant_data = {
					'plant_type': plant.plant_type,
					'pos': [plant.rect.x, plant.rect.y],
					'age': plant.age,
					'harvestable': plant.harvestable,
					'soil_pos': [plant.soil.rect.x, plant.soil.rect.y]
				}
				plants.append(plant_data)
		return plants
	
	def serialize_trees(self, tree_sprites):
		"""Convert tree sprites to serializable format"""
		trees = []
		if tree_sprites:
			for tree in tree_sprites.sprites():
				# Check if it's actually a Tree object (not WildFlower or other sprites)
				if hasattr(tree, 'health') and hasattr(tree, 'alive'):
					tree_data = {
						'pos': [tree.rect.x, tree.rect.y],
						'health': tree.health,
						'alive': tree.alive,
						'apple_count': len(tree.apple_sprites.sprites()) if hasattr(tree, 'apple_sprites') else 0
					}
					trees.append(tree_data)
		return trees
	
	def serialize_timers(self, timers):
		"""Convert player timers to serializable format"""
		serialized = {}
		for name, timer in timers.items():
			serialized[name] = {
				'active': timer.active,
				'start_time': timer.start_time,
				'duration': timer.duration
			}
		return serialized
	
	def serialize_water_tiles(self, water_sprites):
		"""Convert water tiles to serializable format"""
		water_tiles = []
		if water_sprites:
			for water in water_sprites.sprites():
				water_tiles.append([water.rect.x, water.rect.y])
		return water_tiles
	
	def apply_loaded_data(self, game_data, player, level):
		"""Apply loaded data to game objects"""
		try:
			# Update player
			player_data = game_data['player']
			player.pos = pygame.math.Vector2(player_data['pos'])
			player.rect.center = player.pos
			player.hitbox.center = player.pos
			
			# Restore player direction and animation state
			player.direction = pygame.math.Vector2(player_data.get('direction', [0, 0]))
			player.status = player_data.get('status', 'down_idle')
			player.frame_index = player_data.get('frame_index', 0)
			
			# Restore inventory and money
			player.money = player_data['money']
			player.item_inventory = player_data['item_inventory']
			player.seed_inventory = player_data['seed_inventory']
			
			# Restore selected items
			if 'selected_tool' in player_data:
				player.selected_tool = player_data['selected_tool']
				player.tool_index = player_data.get('tool_index', 0)
			if 'selected_seed' in player_data:
				player.selected_seed = player_data['selected_seed']
				player.seed_index = player_data.get('seed_index', 0)
			
			# Restore sleep state
			player.sleep = player_data.get('sleep', False)
			
			# Restore timers
			if 'timers' in player_data:
				self.restore_timers(player.timers, player_data['timers'])
			
			# Update level
			level_data = game_data['level']
			level.raining = level_data['raining']
			level.soil_layer.raining = level_data['raining']
			
			# Restore sky color
			if 'sky_color' in level_data:
				level.sky.start_color = level_data['sky_color']
			
			# Restore transition state
			if 'transition' in level_data:
				level.transition.color = level_data['transition']['color']
				level.transition.speed = level_data['transition']['speed']
			
			# Restore soil grid
			self.restore_soil_grid(level.soil_layer, level_data['soil_grid'])
			
			# Recreate soil tiles first
			level.soil_layer.create_soil_tiles()
			
			# Restore water tiles
			if 'water_tiles' in level_data:
				self.restore_water_tiles(level, level_data['water_tiles'])
			
			# Restore plants
			self.restore_plants(level, level_data['plants'])
			
			# Restore trees
			if 'trees' in level_data:
				self.restore_trees(level, level_data['trees'])
			
			return True
		except Exception as e:
			print(f"Error applying loaded data: {e}")
			import traceback
			traceback.print_exc()
			return False
	
	def restore_soil_grid(self, soil_layer, grid_data):
		"""Restore soil grid from saved data"""
		for y, row in enumerate(grid_data):
			for x, cell in enumerate(row):
				if cell and len(cell) > 0:
					# Keep it as a list, not a set
					soil_layer.grid[y][x] = cell if isinstance(cell, list) else list(cell)
				else:
					soil_layer.grid[y][x] = []
	
	def restore_plants(self, level, plants_data):
		"""Restore plants from saved data"""
		from soil import Plant
		
		# Clear existing plants
		if level.soil_layer.plant_sprites:
			for plant in level.soil_layer.plant_sprites.sprites():
				plant.kill()
		
		# Recreate plants from saved data
		for plant_data in plants_data:
			# Find the soil sprite at the saved position
			soil_pos = plant_data['soil_pos']
			soil_sprite = None
			
			for sprite in level.soil_layer.soil_sprites.sprites():
				if sprite.rect.x == soil_pos[0] and sprite.rect.y == soil_pos[1]:
					soil_sprite = sprite
					break
			
			if soil_sprite:
				# Create the plant
				plant = Plant(
					plant_type=plant_data['plant_type'],
					groups=[level.all_sprites, level.soil_layer.plant_sprites, level.collision_sprites],
					soil=soil_sprite,
					check_watered=level.soil_layer.check_watered
				)
				
				# Restore plant state
				plant.age = plant_data['age']
				plant.harvestable = plant_data['harvestable']
				
				# Update plant image and position based on age
				if int(plant.age) > 0:
					plant.z = LAYERS['main']
					plant.hitbox = plant.rect.copy().inflate(-26, -plant.rect.height * 0.4)
				
				if plant.age >= plant.max_age:
					plant.age = plant.max_age
					plant.harvestable = True
				
				plant.image = plant.frames[int(plant.age)]
				plant.rect = plant.image.get_rect(midbottom=soil_sprite.rect.midbottom + pygame.math.Vector2(0, plant.y_offset))
	
	def restore_trees(self, level, trees_data):
		"""Restore tree health and state from saved data"""
		tree_index = 0
		
		if level.tree_sprites:
			for tree in level.tree_sprites.sprites():
				# Check if it's actually a Tree object
				if hasattr(tree, 'health') and hasattr(tree, 'alive') and tree_index < len(trees_data):
					tree_data = trees_data[tree_index]
					
					# Restore tree health and state
					tree.health = tree_data['health']
					tree.alive = tree_data['alive']
					
					# If tree is dead, update its appearance
					if not tree.alive:
						tree.image = tree.stump_surf
						tree.rect = tree.image.get_rect(midbottom=tree.rect.midbottom)
						tree.hitbox = tree.rect.copy().inflate(-10, -tree.rect.height * 0.6)
					
					# Update apple count (remove excess or keep current if less)
					current_apples = len(tree.apple_sprites.sprites()) if hasattr(tree, 'apple_sprites') else 0
					saved_apples = tree_data['apple_count']
					
					# Remove excess apples
					while current_apples > saved_apples and current_apples > 0:
						apple = tree.apple_sprites.sprites()[0]
						apple.kill()
						current_apples -= 1
					
					tree_index += 1
	
	def restore_timers(self, timers, timer_data):
		"""Restore player timers from saved data"""
		current_time = pygame.time.get_ticks()
		
		for name, data in timer_data.items():
			if name in timers:
				timer = timers[name]
				timer.active = data['active']
				timer.duration = data['duration']
				
				# Adjust start_time based on current time
				if data['active'] and data['start_time'] > 0:
					# Keep the timer active with adjusted start time
					timer.start_time = current_time - (data['start_time'] % data['duration'])
				else:
					timer.start_time = data['start_time']
	
	def restore_water_tiles(self, level, water_tiles_data):
		"""Restore water tiles from saved data"""
		from random import choice
		from soil import WaterTile
		
		# Clear existing water sprites
		for sprite in level.soil_layer.water_sprites.sprites():
			sprite.kill()
		
		# Recreate water tiles
		for pos in water_tiles_data:
			surf = choice(level.soil_layer.water_surfs)
			WaterTile(
				pos=(pos[0], pos[1]),
				surf=surf,
				groups=[level.all_sprites, level.soil_layer.water_sprites]
			)

