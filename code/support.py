from os import walk
from pathlib import Path
import pygame

# Get the directory where this file (support.py) is located
BASE_DIR = Path(__file__).parent.parent

def get_asset_path(relative_path):
	"""Convert relative path to absolute path from project root"""
	return BASE_DIR / relative_path

def import_folder(path):
	surface_list = []
	
	# Convert to absolute path if it's relative
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	else:
		path = Path(path)

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path / image
			image_surf = pygame.image.load(str(full_path)).convert_alpha()
			surface_list.append(image_surf)

	return surface_list

def import_folder_dict(path):
	surface_dict = {}
	
	# Convert to absolute path if it's relative
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	else:
		path = Path(path)

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path / image
			image_surf = pygame.image.load(str(full_path)).convert_alpha()
			surface_dict[image.split('.')[0]] = image_surf

	return surface_dict

def load_sound(path):
	"""Load a sound file with automatic path resolution"""
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	return pygame.mixer.Sound(str(path))

def load_image(path, convert_alpha=False):
	"""Load an image file with automatic path resolution"""
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	
	image = pygame.image.load(str(path))
	if convert_alpha:
		return image.convert_alpha()
	return image

def load_font(path, size):
	"""Load a font file with automatic path resolution"""
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	return pygame.font.Font(str(path), size)

def load_tmx_map(path):
	"""Load a TMX map file with automatic path resolution"""
	from pytmx.util_pygame import load_pygame
	if isinstance(path, str) and path.startswith('..'):
		path = get_asset_path(path[3:])  # Remove '../' prefix
	return load_pygame(str(path))