"""
Main game screen for the puzzle game.
Displays the puzzle image subdivided into tiles with drag-and-drop mechanics.
"""

from typing import List, Optional, Tuple
import pygame

from utils.constants import (
    COLOR_BACKGROUND, COLOR_TILE_BORDER, COLOR_TEXT, COLOR_TILE_DRAGGING,
    COLOR_TILE_HOVER, COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT_HOVER,
    COLOR_SUCCESS, COLOR_WIN_OVERLAY,
    TILE_BORDER_WIDTH, TILE_SPACING, TILE_DRAG_ALPHA,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    FONT_SIZE_LABEL, FONT_SIZE_SMALL_BUTTON, FONT_SIZE_WIN,
    GAME_BUTTON_WIDTH, GAME_BUTTON_HEIGHT, GAME_BUTTON_SPACING
)
from utils.image_utils import (
    load_image, resize_image_to_fit,
    create_puzzle_tiles, calculate_tile_display_rect
)
from utils.puzzle_logic import PuzzleState


class GameScreen:
    """
    Main game screen displaying the puzzle with drag-and-drop mechanics.
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
        self.button_font = pygame.font.Font(None, FONT_SIZE_SMALL_BUTTON)
        self.win_font = pygame.font.Font(None, FONT_SIZE_WIN)

        # Load and prepare the puzzle image
        self._prepare_puzzle()

        # Initialize puzzle state
        self.puzzle_state = PuzzleState(tiles_x, tiles_y)
        self.puzzle_state.shuffle()

        # Drag and drop state
        self.dragging_tile: Optional[Tuple[int, int]] = None  # (row, col) being dragged
        self.drag_offset: Tuple[int, int] = (0, 0)
        self.hovered_tile: Optional[Tuple[int, int]] = None

        # UI buttons
        self._create_buttons()
        self.hovered_button: Optional[str] = None

        # Game state
        self.is_won = False
        self.show_solution = False

    def _prepare_puzzle(self) -> None:
        """
        Load the image, resize it to fit the screen, and create puzzle tiles.
        """
        # Load the original image
        original_image = load_image(self.image_name)

        # Calculate available space for the puzzle (leaving margins and space for buttons)
        margin_top = 80
        margin_bottom = 100  # Increased for buttons
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

    def _create_buttons(self) -> None:
        """
        Create UI button rectangles.
        """
        button_y = SCREEN_HEIGHT - 60
        center_x = SCREEN_WIDTH // 2

        # Calculate total width of all buttons with spacing
        total_buttons = 3
        total_width = (
            total_buttons * GAME_BUTTON_WIDTH +
            (total_buttons - 1) * GAME_BUTTON_SPACING
        )
        start_x = center_x - total_width // 2

        self.shuffle_button = pygame.Rect(
            start_x,
            button_y,
            GAME_BUTTON_WIDTH,
            GAME_BUTTON_HEIGHT
        )

        self.restart_button = pygame.Rect(
            start_x + GAME_BUTTON_WIDTH + GAME_BUTTON_SPACING,
            button_y,
            GAME_BUTTON_WIDTH,
            GAME_BUTTON_HEIGHT
        )

        self.solution_button = pygame.Rect(
            start_x + 2 * (GAME_BUTTON_WIDTH + GAME_BUTTON_SPACING),
            button_y,
            GAME_BUTTON_WIDTH,
            GAME_BUTTON_HEIGHT
        )

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
            elif event.key == pygame.K_s:
                self._shuffle_puzzle()
            elif event.key == pygame.K_r:
                self._restart_puzzle()
            elif event.key == pygame.K_SPACE:
                self.show_solution = not self.show_solution

        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_mouse_down(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self._handle_mouse_up(event.pos)

        return False

    def _handle_mouse_motion(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handle mouse motion for hover effects and dragging.

        Args:
            mouse_pos: Current mouse position
        """
        # Update hovered tile
        if self.dragging_tile is None:
            self.hovered_tile = self._get_tile_at_position(mouse_pos)

        # Update hovered button
        self.hovered_button = None
        if self.shuffle_button.collidepoint(mouse_pos):
            self.hovered_button = 'shuffle'
        elif self.restart_button.collidepoint(mouse_pos):
            self.hovered_button = 'restart'
        elif self.solution_button.collidepoint(mouse_pos):
            self.hovered_button = 'solution'

    def _handle_mouse_down(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handle mouse button down for starting drag or clicking buttons.

        Args:
            mouse_pos: Mouse position where click occurred
        """
        # Check buttons first
        if self.shuffle_button.collidepoint(mouse_pos):
            self._shuffle_puzzle()
            return
        elif self.restart_button.collidepoint(mouse_pos):
            self._restart_puzzle()
            return
        elif self.solution_button.collidepoint(mouse_pos):
            self.show_solution = not self.show_solution
            return

        # Start dragging a tile
        tile_coords = self._get_tile_at_position(mouse_pos)
        if tile_coords is not None:
            self.dragging_tile = tile_coords
            row, col = tile_coords
            tile_rect = self._get_tile_rect(row, col)
            self.drag_offset = (
                mouse_pos[0] - tile_rect.x,
                mouse_pos[1] - tile_rect.y
            )

    def _handle_mouse_up(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Handle mouse button up for completing drag.

        Args:
            mouse_pos: Mouse position where release occurred
        """
        if self.dragging_tile is not None:
            # Get the tile we're dropping onto
            drop_tile = self._get_tile_at_position(mouse_pos)

            if drop_tile is not None and drop_tile != self.dragging_tile:
                # Swap the tiles
                row1, col1 = self.dragging_tile
                row2, col2 = drop_tile
                self.puzzle_state.swap_tiles(row1, col1, row2, col2)

                # Check if puzzle is solved
                if self.puzzle_state.is_solved():
                    self.is_won = True

            # Reset dragging state
            self.dragging_tile = None
            self.drag_offset = (0, 0)

    def _get_tile_at_position(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Get which tile (if any) is at the given screen position.

        Args:
            pos: Screen position (x, y)

        Returns:
            Tuple of (row, col) if a tile is at this position, None otherwise
        """
        for row in range(self.tiles_y):
            for col in range(self.tiles_x):
                tile_rect = self._get_tile_rect(row, col)
                if tile_rect.collidepoint(pos):
                    return (row, col)
        return None

    def _get_tile_rect(self, row: int, col: int) -> pygame.Rect:
        """
        Get the rectangle for a tile at the given position.

        Args:
            row: Tile row
            col: Tile column

        Returns:
            Pygame Rect for the tile
        """
        return calculate_tile_display_rect(
            row, col,
            self.tile_width, self.tile_height,
            self.puzzle_start_x, self.puzzle_start_y
        )

    def _shuffle_puzzle(self) -> None:
        """
        Shuffle the puzzle.
        """
        self.puzzle_state.shuffle()
        self.is_won = False
        self.show_solution = False

    def _restart_puzzle(self) -> None:
        """
        Restart the puzzle to solved state and then shuffle.
        """
        self._shuffle_puzzle()

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
                if (row, col) != self.dragging_tile:
                    self._draw_tile(row, col)

        # Draw dragging tile on top
        if self.dragging_tile is not None:
            self._draw_dragging_tile()

        # Draw UI buttons
        self._draw_buttons()

        # Draw win overlay if puzzle is solved
        if self.is_won:
            self._draw_win_overlay()

        # Draw instructions
        instructions = self.button_font.render(
            "Drag tiles to swap | ESC: Menu | S: Shuffle | R: Restart | Space: Toggle Solution",
            True,
            COLOR_TEXT
        )
        instructions_rect = instructions.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15)
        )
        self.screen.blit(instructions, instructions_rect)

    def _draw_tile(self, row: int, col: int) -> None:
        """
        Draw a single puzzle tile with border.

        Args:
            row: Tile row index (position)
            col: Tile column index (position)
        """
        # Get which original tile should be at this position
        tile_original_row, tile_original_col = self.puzzle_state.get_tile_at_position(row, col)

        # Get the tile surface from the original tiles array
        tile_surface = self.tiles[tile_original_row][tile_original_col]

        # Calculate tile display position
        tile_rect = self._get_tile_rect(row, col)

        # Draw the tile image
        self.screen.blit(tile_surface, tile_rect)

        # Determine border color based on state
        border_color = COLOR_TILE_BORDER

        # Highlight if hovering (and not dragging)
        if (row, col) == self.hovered_tile and self.dragging_tile is None:
            border_color = COLOR_TILE_HOVER

        # Show solution mode - highlight correctly placed tiles
        if self.show_solution:
            if (tile_original_row, tile_original_col) == (row, col):
                border_color = COLOR_SUCCESS

        # Draw border around the tile
        pygame.draw.rect(
            self.screen,
            border_color,
            tile_rect,
            TILE_BORDER_WIDTH + (2 if border_color != COLOR_TILE_BORDER else 0)
        )

    def _draw_dragging_tile(self) -> None:
        """
        Draw the tile currently being dragged at the mouse position.
        """
        if self.dragging_tile is None:
            return

        row, col = self.dragging_tile
        mouse_pos = pygame.mouse.get_pos()

        # Get which original tile this is
        tile_original_row, tile_original_col = self.puzzle_state.get_tile_at_position(row, col)
        tile_surface = self.tiles[tile_original_row][tile_original_col].copy()

        # Apply transparency
        tile_surface.set_alpha(TILE_DRAG_ALPHA)

        # Calculate position (centered on mouse with offset)
        draw_x = mouse_pos[0] - self.drag_offset[0]
        draw_y = mouse_pos[1] - self.drag_offset[1]

        # Draw the tile
        self.screen.blit(tile_surface, (draw_x, draw_y))

        # Draw border
        drag_rect = pygame.Rect(draw_x, draw_y, self.tile_width, self.tile_height)
        pygame.draw.rect(
            self.screen,
            COLOR_TILE_DRAGGING,
            drag_rect,
            TILE_BORDER_WIDTH + 2
        )

    def _draw_buttons(self) -> None:
        """
        Draw UI control buttons.
        """
        buttons = [
            (self.shuffle_button, "Shuffle", 'shuffle'),
            (self.restart_button, "Restart", 'restart'),
            (self.solution_button, "Solution" if not self.show_solution else "Hide", 'solution')
        ]

        for button_rect, text, button_id in buttons:
            is_hovered = self.hovered_button == button_id

            # Draw button background
            button_color = COLOR_BUTTON_HOVER if is_hovered else COLOR_BUTTON
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)

            # Draw button text
            text_color = COLOR_TEXT_HOVER if is_hovered else COLOR_TEXT
            button_text = self.button_font.render(text, True, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

    def _draw_win_overlay(self) -> None:
        """
        Draw victory overlay when puzzle is solved.
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_WIN_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        # Draw win message
        win_text = self.win_font.render("Puzzle Solved!", True, COLOR_SUCCESS)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(win_text, win_rect)

        # Draw instruction
        instruction_text = self.label_font.render(
            "Press 'S' to shuffle or ESC to return to menu",
            True,
            COLOR_TEXT
        )
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(instruction_text, instruction_rect)
