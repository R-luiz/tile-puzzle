"""
Main entry point for the puzzle game.
Manages game states and the main game loop.
"""

import sys
from enum import Enum
import pygame

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLOR_BACKGROUND
from screens.menu_screen import MenuScreen
from screens.config_screen import ConfigScreen
from screens.game_screen import GameScreen


class GameState(Enum):
    """
    Enumeration of possible game states.
    """
    MENU = "menu"
    CONFIG = "config"
    GAME = "game"
    QUIT = "quit"


class PuzzleGame:
    """
    Main game class managing the puzzle game flow.
    """

    def __init__(self):
        """
        Initialize the puzzle game.
        """
        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Puzzle Game")

        # Set up the clock for FPS management
        self.clock = pygame.time.Clock()

        # Initialize game state
        self.current_state = GameState.MENU
        self.running = True

        # Screen instances
        self.menu_screen = None
        self.config_screen = None
        self.game_screen = None

        # Game data
        self.selected_image = None
        self.tiles_x = 0
        self.tiles_y = 0

    def run(self) -> None:
        """
        Main game loop.
        """
        while self.running:
            # Handle events
            self._handle_events()

            # Update current screen
            self._update()

            # Draw current screen
            self._draw()

            # Update display
            pygame.display.flip()

            # Maintain FPS
            self.clock.tick(FPS)

        # Clean up
        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        """
        Handle pygame events based on current state.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.current_state = GameState.QUIT
                return

            # State-specific event handling
            if self.current_state == GameState.MENU:
                self._handle_menu_events(event)
            elif self.current_state == GameState.CONFIG:
                self._handle_config_events(event)
            elif self.current_state == GameState.GAME:
                self._handle_game_events(event)

    def _handle_menu_events(self, event: pygame.event.Event) -> None:
        """
        Handle events for the menu screen.

        Args:
            event: Pygame event to handle
        """
        if self.menu_screen is None:
            self.menu_screen = MenuScreen(self.screen)

        if self.menu_screen.handle_event(event):
            # Image was selected, move to configuration
            self.selected_image = self.menu_screen.get_selected_image()
            self.current_state = GameState.CONFIG
            self.config_screen = None  # Reset config screen

    def _handle_config_events(self, event: pygame.event.Event) -> None:
        """
        Handle events for the configuration screen.

        Args:
            event: Pygame event to handle
        """
        if self.config_screen is None:
            self.config_screen = ConfigScreen(self.screen, self.selected_image)

        if self.config_screen.handle_event(event):
            # Configuration complete, start game
            self.tiles_x, self.tiles_y = self.config_screen.get_tile_config()
            self.current_state = GameState.GAME
            self.game_screen = None  # Reset game screen

    def _handle_game_events(self, event: pygame.event.Event) -> None:
        """
        Handle events for the game screen.

        Args:
            event: Pygame event to handle
        """
        if self.game_screen is None:
            self.game_screen = GameScreen(
                self.screen,
                self.selected_image,
                self.tiles_x,
                self.tiles_y
            )

        if self.game_screen.handle_event(event):
            # Return to menu
            self.current_state = GameState.MENU
            self.menu_screen = None  # Reset menu screen

    def _update(self) -> None:
        """
        Update game state.
        Currently no per-frame updates needed, but kept for future expansion.
        """
        pass

    def _draw(self) -> None:
        """
        Draw the current screen based on game state.
        """
        # Clear screen
        self.screen.fill(COLOR_BACKGROUND)

        # Draw appropriate screen
        if self.current_state == GameState.MENU:
            if self.menu_screen is None:
                self.menu_screen = MenuScreen(self.screen)
            self.menu_screen.draw()

        elif self.current_state == GameState.CONFIG:
            if self.config_screen is None:
                self.config_screen = ConfigScreen(self.screen, self.selected_image)
            self.config_screen.draw()

        elif self.current_state == GameState.GAME:
            if self.game_screen is None:
                self.game_screen = GameScreen(
                    self.screen,
                    self.selected_image,
                    self.tiles_x,
                    self.tiles_y
                )
            self.game_screen.draw()


def main():
    """
    Main entry point for the application.
    """
    try:
        game = PuzzleGame()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
