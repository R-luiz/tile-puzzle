"""
Configuration screen for setting puzzle tile dimensions.
Allows user to input the number of tiles in X and Y directions.
"""

from typing import Optional, Tuple
import pygame

from utils.constants import (
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_TEXT_HOVER,
    COLOR_BUTTON, COLOR_BUTTON_HOVER,
    COLOR_INPUT_BOX, COLOR_INPUT_BOX_ACTIVE,
    MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT,
    INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT,
    FONT_SIZE_TITLE, FONT_SIZE_LABEL, FONT_SIZE_INPUT, FONT_SIZE_BUTTON,
    SCREEN_WIDTH, SCREEN_HEIGHT,
    MIN_TILES, MAX_TILES, DEFAULT_TILES_X, DEFAULT_TILES_Y
)


class ConfigScreen:
    """
    Configuration screen for setting puzzle dimensions.
    """

    def __init__(self, screen: pygame.Surface, image_name: str):
        """
        Initialize the configuration screen.

        Args:
            screen: Pygame display surface
            image_name: Name of the selected image
        """
        self.screen = screen
        self.image_name = image_name

        # Tile configuration
        self.tiles_x = DEFAULT_TILES_X
        self.tiles_y = DEFAULT_TILES_Y
        self.input_x = str(DEFAULT_TILES_X)
        self.input_y = str(DEFAULT_TILES_Y)

        # Active input field
        self.active_input: Optional[str] = None  # 'x', 'y', or None
        self.hovered_button = False

        # Initialize fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.label_font = pygame.font.Font(None, FONT_SIZE_LABEL)
        self.input_font = pygame.font.Font(None, FONT_SIZE_INPUT)
        self.button_font = pygame.font.Font(None, FONT_SIZE_BUTTON)

        # Create UI elements
        center_x = SCREEN_WIDTH // 2
        self.input_box_x = pygame.Rect(
            center_x - INPUT_BOX_WIDTH - 30,
            300,
            INPUT_BOX_WIDTH,
            INPUT_BOX_HEIGHT
        )
        self.input_box_y = pygame.Rect(
            center_x + 30,
            300,
            INPUT_BOX_WIDTH,
            INPUT_BOX_HEIGHT
        )
        self.start_button = pygame.Rect(
            center_x - MENU_BUTTON_WIDTH // 2,
            450,
            MENU_BUTTON_WIDTH,
            MENU_BUTTON_HEIGHT
        )

        self.config_complete = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the configuration screen.

        Args:
            event: Pygame event to handle

        Returns:
            True if configuration is complete, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_mouse_click(event.pos)

        elif event.type == pygame.KEYDOWN:
            self._handle_keydown(event)

        return False

    def _handle_mouse_motion(self, mouse_pos: tuple) -> None:
        """
        Handle mouse motion to update hover states.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.hovered_button = self.start_button.collidepoint(mouse_pos)

    def _handle_mouse_click(self, mouse_pos: tuple) -> bool:
        """
        Handle mouse click to select input boxes or start button.

        Args:
            mouse_pos: Mouse position where click occurred

        Returns:
            True if start button was clicked with valid input, False otherwise
        """
        # Check input boxes
        if self.input_box_x.collidepoint(mouse_pos):
            self.active_input = 'x'
        elif self.input_box_y.collidepoint(mouse_pos):
            self.active_input = 'y'
        elif self.start_button.collidepoint(mouse_pos):
            # Validate and start game
            if self._validate_input():
                self.config_complete = True
                return True
        else:
            self.active_input = None

        return False

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """
        Handle keyboard input for entering tile numbers.

        Args:
            event: Pygame keyboard event
        """
        if self.active_input is None:
            return

        if event.key == pygame.K_RETURN:
            # Move to next input or validate
            if self.active_input == 'x':
                self.active_input = 'y'
            elif self.active_input == 'y':
                if self._validate_input():
                    self.config_complete = True
        elif event.key == pygame.K_TAB:
            # Switch between inputs
            self.active_input = 'y' if self.active_input == 'x' else 'x'
        elif event.key == pygame.K_BACKSPACE:
            # Remove last character
            if self.active_input == 'x':
                self.input_x = self.input_x[:-1]
            else:
                self.input_y = self.input_y[:-1]
        elif event.unicode.isdigit():
            # Add digit to current input (max 2 digits)
            if self.active_input == 'x' and len(self.input_x) < 2:
                self.input_x += event.unicode
            elif self.active_input == 'y' and len(self.input_y) < 2:
                self.input_y += event.unicode

    def _validate_input(self) -> bool:
        """
        Validate the input tile dimensions.

        Returns:
            True if input is valid, False otherwise
        """
        try:
            x = int(self.input_x) if self.input_x else 0
            y = int(self.input_y) if self.input_y else 0

            if MIN_TILES <= x <= MAX_TILES and MIN_TILES <= y <= MAX_TILES:
                self.tiles_x = x
                self.tiles_y = y
                return True
        except ValueError:
            pass

        return False

    def draw(self) -> None:
        """
        Draw the configuration screen.
        """
        self.screen.fill(COLOR_BACKGROUND)

        # Draw title
        title_text = self.title_font.render("Configure Puzzle", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)

        # Draw image name
        image_display = self.image_name.rsplit('.', 1)[0]
        image_text = self.label_font.render(f"Image: {image_display}", True, COLOR_TEXT)
        image_rect = image_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.screen.blit(image_text, image_rect)

        # Draw labels
        label_y = 250
        x_label = self.label_font.render("Tiles X:", True, COLOR_TEXT)
        y_label = self.label_font.render("Tiles Y:", True, COLOR_TEXT)
        self.screen.blit(
            x_label,
            x_label.get_rect(center=(self.input_box_x.centerx, label_y))
        )
        self.screen.blit(
            y_label,
            y_label.get_rect(center=(self.input_box_y.centerx, label_y))
        )

        # Draw input boxes
        self._draw_input_box(self.input_box_x, self.input_x, self.active_input == 'x')
        self._draw_input_box(self.input_box_y, self.input_y, self.active_input == 'y')

        # Draw range hint
        hint_text = self.label_font.render(
            f"Range: {MIN_TILES}-{MAX_TILES}",
            True,
            COLOR_TEXT
        )
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
        self.screen.blit(hint_text, hint_rect)

        # Draw start button
        button_color = COLOR_BUTTON_HOVER if self.hovered_button else COLOR_BUTTON
        pygame.draw.rect(self.screen, button_color, self.start_button, border_radius=8)

        button_text_color = COLOR_TEXT_HOVER if self.hovered_button else COLOR_TEXT
        button_text = self.button_font.render("Start Game", True, button_text_color)
        text_rect = button_text.get_rect(center=self.start_button.center)
        self.screen.blit(button_text, text_rect)

    def _draw_input_box(self, rect: pygame.Rect, text: str, is_active: bool) -> None:
        """
        Draw an input box with its current value.

        Args:
            rect: Rectangle defining the input box position and size
            text: Current text in the input box
            is_active: Whether this input box is currently active
        """
        # Draw box background
        box_color = COLOR_INPUT_BOX_ACTIVE if is_active else COLOR_INPUT_BOX
        pygame.draw.rect(self.screen, box_color, rect, border_radius=5)

        # Draw border for active box
        if is_active:
            pygame.draw.rect(self.screen, COLOR_TEXT_HOVER, rect, 3, border_radius=5)

        # Draw text
        if text:
            input_text = self.input_font.render(text, True, COLOR_TEXT)
            text_rect = input_text.get_rect(center=rect.center)
            self.screen.blit(input_text, text_rect)

    def get_tile_config(self) -> Tuple[int, int]:
        """
        Get the configured tile dimensions.

        Returns:
            Tuple of (tiles_x, tiles_y)
        """
        return self.tiles_x, self.tiles_y
