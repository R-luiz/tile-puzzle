"""
Home menu screen for image selection.
Displays available images as selectable buttons.
"""

from typing import Optional
import pygame

from utils.constants import (
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_TEXT_HOVER,
    COLOR_BUTTON, COLOR_BUTTON_HOVER,
    MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT, MENU_BUTTON_SPACING,
    FONT_SIZE_TITLE, FONT_SIZE_BUTTON,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from utils.image_utils import get_available_images


class MenuScreen:
    """
    Home menu screen for selecting puzzle images.
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the menu screen.

        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.available_images = get_available_images()
        self.selected_image: Optional[str] = None
        self.hovered_index: Optional[int] = None

        # Initialize fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.button_font = pygame.font.Font(None, FONT_SIZE_BUTTON)

        # Create button rectangles
        self.button_rects = []
        self._create_buttons()

    def _create_buttons(self) -> None:
        """
        Create button rectangles for each available image.
        """
        start_y = 180
        center_x = SCREEN_WIDTH // 2

        for i in range(len(self.available_images)):
            button_rect = pygame.Rect(
                center_x - MENU_BUTTON_WIDTH // 2,
                start_y + i * (MENU_BUTTON_HEIGHT + MENU_BUTTON_SPACING),
                MENU_BUTTON_WIDTH,
                MENU_BUTTON_HEIGHT
            )
            self.button_rects.append(button_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle pygame events for the menu screen.

        Args:
            event: Pygame event to handle

        Returns:
            True if an image was selected, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_mouse_click(event.pos)

        return False

    def _handle_mouse_motion(self, mouse_pos: tuple) -> None:
        """
        Handle mouse motion to update hover state.

        Args:
            mouse_pos: Current mouse position (x, y)
        """
        self.hovered_index = None
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.hovered_index = i
                break

    def _handle_mouse_click(self, mouse_pos: tuple) -> bool:
        """
        Handle mouse click to select an image.

        Args:
            mouse_pos: Mouse position where click occurred

        Returns:
            True if an image was selected, False otherwise
        """
        for i, rect in enumerate(self.button_rects):
            if rect.collidepoint(mouse_pos):
                self.selected_image = self.available_images[i]
                return True
        return False

    def draw(self) -> None:
        """
        Draw the menu screen.
        """
        self.screen.fill(COLOR_BACKGROUND)

        # Draw title
        title_text = self.title_font.render("Select Puzzle Image", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)

        # Draw image selection buttons
        for i, (image_name, button_rect) in enumerate(
            zip(self.available_images, self.button_rects)
        ):
            is_hovered = i == self.hovered_index

            # Draw button background
            button_color = COLOR_BUTTON_HOVER if is_hovered else COLOR_BUTTON
            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)

            # Draw button text
            text_color = COLOR_TEXT_HOVER if is_hovered else COLOR_TEXT
            # Remove file extension for display
            display_name = image_name.rsplit('.', 1)[0]
            button_text = self.button_font.render(display_name, True, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)

        # Draw message if no images available
        if not self.available_images:
            message_text = self.button_font.render(
                "No images found in 'images' folder",
                True,
                COLOR_TEXT
            )
            message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(message_text, message_rect)

    def get_selected_image(self) -> Optional[str]:
        """
        Get the currently selected image.

        Returns:
            Name of the selected image, or None if no selection
        """
        return self.selected_image
