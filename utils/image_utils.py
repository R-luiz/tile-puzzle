"""
Image handling utilities for the puzzle game.
Provides functions for loading, resizing, and subdividing images into tiles.
"""

import os
from typing import List, Tuple
import pygame

from utils.constants import IMAGES_FOLDER, TILE_BORDER_WIDTH, TILE_SPACING


def get_available_images() -> List[str]:
    """
    Get list of available image files from the images folder.

    Returns:
        List of image filenames found in the images folder
    """
    if not os.path.exists(IMAGES_FOLDER):
        return []

    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    images = [
        f for f in os.listdir(IMAGES_FOLDER)
        if f.lower().endswith(supported_formats)
    ]
    return sorted(images)


def load_image(image_name: str) -> pygame.Surface:
    """
    Load an image from the images folder.

    Args:
        image_name: Name of the image file

    Returns:
        Pygame surface containing the loaded image

    Raises:
        FileNotFoundError: If image file doesn't exist
    """
    image_path = os.path.join(IMAGES_FOLDER, image_name)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    return pygame.image.load(image_path)


def calculate_fitted_size(
    original_width: int,
    original_height: int,
    max_width: int,
    max_height: int
) -> Tuple[int, int]:
    """
    Calculate the size to fit an image within given dimensions while maintaining aspect ratio.

    Args:
        original_width: Original image width
        original_height: Original image height
        max_width: Maximum allowed width
        max_height: Maximum allowed height

    Returns:
        Tuple of (fitted_width, fitted_height)
    """
    aspect_ratio = original_width / original_height

    # Try fitting to width
    fitted_width = max_width
    fitted_height = int(fitted_width / aspect_ratio)

    # If height exceeds max, fit to height instead
    if fitted_height > max_height:
        fitted_height = max_height
        fitted_width = int(fitted_height * aspect_ratio)

    return fitted_width, fitted_height


def resize_image_to_fit(
    image: pygame.Surface,
    max_width: int,
    max_height: int
) -> pygame.Surface:
    """
    Resize an image to fit within given dimensions while maintaining aspect ratio.

    Args:
        image: Pygame surface to resize
        max_width: Maximum width
        max_height: Maximum height

    Returns:
        Resized pygame surface
    """
    original_width, original_height = image.get_size()
    fitted_width, fitted_height = calculate_fitted_size(
        original_width, original_height, max_width, max_height
    )

    return pygame.transform.smoothscale(image, (fitted_width, fitted_height))


def create_puzzle_tiles(
    image: pygame.Surface,
    tiles_x: int,
    tiles_y: int
) -> Tuple[List[List[pygame.Surface]], int, int]:
    """
    Subdivide an image into puzzle tiles.

    Args:
        image: Pygame surface to subdivide
        tiles_x: Number of tiles horizontally
        tiles_y: Number of tiles vertically

    Returns:
        Tuple of (2D list of tile surfaces, tile_width, tile_height)
    """
    image_width, image_height = image.get_size()
    tile_width = image_width // tiles_x
    tile_height = image_height // tiles_y

    tiles = []
    for row in range(tiles_y):
        tile_row = []
        for col in range(tiles_x):
            # Calculate the rectangle to extract from the original image
            rect = pygame.Rect(
                col * tile_width,
                row * tile_height,
                tile_width,
                tile_height
            )

            # Extract the tile from the original image
            tile_surface = image.subsurface(rect).copy()
            tile_row.append(tile_surface)

        tiles.append(tile_row)

    return tiles, tile_width, tile_height


def calculate_tile_display_rect(
    row: int,
    col: int,
    tile_width: int,
    tile_height: int,
    start_x: int,
    start_y: int
) -> pygame.Rect:
    """
    Calculate the display rectangle for a tile including spacing.

    Args:
        row: Tile row index
        col: Tile column index
        tile_width: Width of each tile
        tile_height: Height of each tile
        start_x: Starting X position for the puzzle grid
        start_y: Starting Y position for the puzzle grid

    Returns:
        Pygame Rect for the tile position
    """
    x = start_x + col * (tile_width + TILE_SPACING)
    y = start_y + row * (tile_height + TILE_SPACING)

    return pygame.Rect(x, y, tile_width, tile_height)
