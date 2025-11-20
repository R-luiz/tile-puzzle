"""
Main game screen for the puzzle game.
Displays the puzzle image subdivided into tiles with borders and spacing.
"""

from typing import List
import pygame

from utils.constants import (
    COLOR_BACKGROUND, COLOR_TILE_BORDER, COLOR_TEXT,
    TILE_BORDER_WIDTH, TILE_SPACING,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_SIZE_LABEL
)
from utils.image_utils import (
    load_image, resize_image_to_fit,
    create_puzzle_tiles, calculate_tile_display_rect
)


class GameScreen:
    """
    Main game screen displaying the puzzle.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        image_name: str,
        tiles_x: int,
        tiles_y: int
    ):
        """
        Initialize the game screen.

        Args:
            screen: Pygame display surface
            image_name: Name of the image to use for the puzzle
            tiles_x: Number of tiles horizontally
            tiles_y: Number of tiles vertically
        """
        self.screen = screen
        self.image_name = image_name
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y

        # Initialize fonts
        self.label_font = pygame.font.Font(None, FONT_SIZE_LABEL)

        # Load and prepare the puzzle image
        self._prepare_puzzle()

    def _prepare_puzzle(self) -> None:
        """
        Load the image, resize it to fit the screen, and create puzzle tiles.
        """
        # Load the original image
        original_image = load_image(self.image_name)

        # Calculate available space for the puzzle (leaving margins)
        margin_top = 80
        margin_bottom = 40
        margin_sides = 40

        available_width = SCREEN_WIDTH - (2 * margin_sides)
        available_height = SCREEN_HEIGHT - margin_top - margin_bottom

        # Account for spacing between tiles
        total_spacing_x = (self.tiles_x - 1) * TILE_SPACING
        total_spacing_y = (self.tiles_y - 1) * TILE_SPACING

        max_puzzle_width = available_width - total_spacing_x
        max_puzzle_height = available_height - total_spacing_y

        # Resize image to fit available space
        self.puzzle_image = resize_image_to_fit(
            original_image,
            max_puzzle_width,
            max_puzzle_height
        )

        # Create puzzle tiles
        self.tiles, self.tile_width, self.tile_height = create_puzzle_tiles(
            self.puzzle_image,
            self.tiles_x,
            self.tiles_y
        )

        # Calculate starting position to center the puzzle
        puzzle_total_width = (
            self.tiles_x * self.tile_width +
            (self.tiles_x - 1) * TILE_SPACING
        )
        puzzle_total_height = (
            self.tiles_y * self.tile_height +
            (self.tiles_y - 1) * TILE_SPACING
        )

        self.puzzle_start_x = (SCREEN_WIDTH - puzzle_total_width) // 2
        self.puzzle_start_y = margin_top + (available_height - puzzle_total_height) // 2

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the game screen.

        Args:
            event: Pygame event to handle

        Returns:
            True if game should exit, False otherwise
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True

        return False

    def draw(self) -> None:
        """
        Draw the game screen with puzzle tiles.
        """
        self.screen.fill(COLOR_BACKGROUND)

        # Draw title
        title_text = self.label_font.render(
            f"Puzzle: {self.image_name.rsplit('.', 1)[0]} ({self.tiles_x}x{self.tiles_y})",
            True,
            COLOR_TEXT
        )
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title_text, title_rect)

        # Draw all puzzle tiles
        for row in range(self.tiles_y):
            for col in range(self.tiles_x):
                self._draw_tile(row, col)

        # Draw instructions
        instructions = self.label_font.render(
            "Press ESC to return to menu",
            True,
            COLOR_TEXT
        )
        instructions_rect = instructions.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        )
        self.screen.blit(instructions, instructions_rect)

    def _draw_tile(self, row: int, col: int) -> None:
        """
        Draw a single puzzle tile with border.

        Args:
            row: Tile row index
            col: Tile column index
        """
        # Get the tile surface
        tile_surface = self.tiles[row][col]

        # Calculate tile position
        tile_rect = calculate_tile_display_rect(
            row, col,
            self.tile_width, self.tile_height,
            self.puzzle_start_x, self.puzzle_start_y
        )

        # Draw the tile image
        self.screen.blit(tile_surface, tile_rect)

        # Draw border around the tile
        pygame.draw.rect(
            self.screen,
            COLOR_TILE_BORDER,
            tile_rect,
            TILE_BORDER_WIDTH
        )
