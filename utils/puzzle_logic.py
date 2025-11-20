"""
Puzzle logic for managing tile positions, shuffling, and win detection.
"""

import random
from typing import List, Tuple, Optional


class PuzzleState:
    """
    Manages the state of the puzzle including tile positions and win detection.
    """

    def __init__(self, tiles_x: int, tiles_y: int):
        """
        Initialize puzzle state.

        Args:
            tiles_x: Number of tiles horizontally
            tiles_y: Number of tiles vertically
        """
        self.tiles_x = tiles_x
        self.tiles_y = tiles_y
        self.total_tiles = tiles_x * tiles_y

        # Initialize tile positions - each position stores (row, col) of the tile that should be there
        # Position [row][col] contains the original tile coordinates
        self.tile_positions: List[List[Tuple[int, int]]] = []
        self._initialize_solved_state()

    def _initialize_solved_state(self) -> None:
        """
        Initialize the puzzle in solved state.
        Each position contains its own coordinates (solved state).
        """
        self.tile_positions = []
        for row in range(self.tiles_y):
            row_positions = []
            for col in range(self.tiles_x):
                row_positions.append((row, col))
            self.tile_positions.append(row_positions)

    def shuffle(self, num_swaps: int = None) -> None:
        """
        Shuffle the puzzle by performing random swaps.

        Args:
            num_swaps: Number of random swaps to perform (default: total_tiles * 5)
        """
        if num_swaps is None:
            num_swaps = self.total_tiles * 5

        for _ in range(num_swaps):
            # Pick two random positions
            row1, col1 = random.randint(0, self.tiles_y - 1), random.randint(0, self.tiles_x - 1)
            row2, col2 = random.randint(0, self.tiles_y - 1), random.randint(0, self.tiles_x - 1)

            # Swap them
            self.swap_tiles(row1, col1, row2, col2)

    def swap_tiles(self, row1: int, col1: int, row2: int, col2: int) -> None:
        """
        Swap two tiles at the given positions.

        Args:
            row1: Row of first tile
            col1: Column of first tile
            row2: Row of second tile
            col2: Column of second tile
        """
        # Swap the tile identities at these positions
        temp = self.tile_positions[row1][col1]
        self.tile_positions[row1][col1] = self.tile_positions[row2][col2]
        self.tile_positions[row2][col2] = temp

    def get_tile_at_position(self, row: int, col: int) -> Tuple[int, int]:
        """
        Get which tile is currently at the given position.

        Args:
            row: Row position
            col: Column position

        Returns:
            Tuple of (original_row, original_col) of the tile at this position
        """
        return self.tile_positions[row][col]

    def is_solved(self) -> bool:
        """
        Check if the puzzle is in solved state.

        Returns:
            True if puzzle is solved, False otherwise
        """
        for row in range(self.tiles_y):
            for col in range(self.tiles_x):
                # Check if tile at this position is the correct one
                tile_coords = self.tile_positions[row][col]
                if tile_coords != (row, col):
                    return False
        return True

    def get_correctness_grid(self) -> List[List[bool]]:
        """
        Get a grid showing which tiles are in the correct position.

        Returns:
            2D list of booleans, True if tile is correctly placed
        """
        correctness = []
        for row in range(self.tiles_y):
            row_correctness = []
            for col in range(self.tiles_x):
                tile_coords = self.tile_positions[row][col]
                is_correct = tile_coords == (row, col)
                row_correctness.append(is_correct)
            correctness.append(row_correctness)
        return correctness

    def reset_to_solved(self) -> None:
        """
        Reset the puzzle to solved state.
        """
        self._initialize_solved_state()
