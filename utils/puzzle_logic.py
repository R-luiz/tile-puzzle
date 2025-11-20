"""
Puzzle logic for managing tile positions, shuffling, and win detection.
Includes merged tile group mechanics for adjacent correctly placed tiles.
"""

import random
from typing import List, Tuple, Optional, Set, FrozenSet


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

        # Track merged tile groups
        self.merged_groups: List[Set[Tuple[int, int]]] = []
        self._update_merged_groups()

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

            # Swap them (this will update merged groups)
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

        # Update merged groups after swap
        self._update_merged_groups()

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
        self._update_merged_groups()

    def _update_merged_groups(self) -> None:
        """
        Update the merged tile groups by finding all connected correctly placed tiles.
        """
        visited = set()
        self.merged_groups = []

        for row in range(self.tiles_y):
            for col in range(self.tiles_x):
                if (row, col) not in visited:
                    # Check if this tile is correctly placed
                    if self.tile_positions[row][col] == (row, col):
                        # Start a new group with BFS/DFS
                        group = self._find_connected_correct_tiles(row, col, visited)
                        if len(group) > 1:  # Only track groups of 2 or more
                            self.merged_groups.append(group)

    def _find_connected_correct_tiles(
        self,
        start_row: int,
        start_col: int,
        visited: Set[Tuple[int, int]]
    ) -> Set[Tuple[int, int]]:
        """
        Find all correctly placed tiles connected to the starting position.

        Args:
            start_row: Starting row position
            start_col: Starting column position
            visited: Set of already visited positions

        Returns:
            Set of positions in the connected group
        """
        group = set()
        stack = [(start_row, start_col)]

        while stack:
            row, col = stack.pop()

            if (row, col) in visited:
                continue

            # Check if this tile is correctly placed
            if self.tile_positions[row][col] != (row, col):
                continue

            visited.add((row, col))
            group.add((row, col))

            # Check all 4 adjacent positions
            neighbors = [
                (row - 1, col),  # Up
                (row + 1, col),  # Down
                (row, col - 1),  # Left
                (row, col + 1)   # Right
            ]

            for n_row, n_col in neighbors:
                if (0 <= n_row < self.tiles_y and
                    0 <= n_col < self.tiles_x and
                    (n_row, n_col) not in visited):
                    stack.append((n_row, n_col))

        return group

    def get_group_containing_position(self, row: int, col: int) -> Optional[Set[Tuple[int, int]]]:
        """
        Get the merged group that contains the given position.

        Args:
            row: Row position
            col: Column position

        Returns:
            Set of positions in the group, or None if position is not in a merged group
        """
        for group in self.merged_groups:
            if (row, col) in group:
                return group
        return None

    def can_swap_groups(
        self,
        source_group: Set[Tuple[int, int]],
        target_row: int,
        target_col: int
    ) -> bool:
        """
        Check if a merged group can be swapped to a target location.

        Args:
            source_group: Set of positions in the source group
            target_row: Target row position
            target_col: Target column position

        Returns:
            True if swap is valid, False otherwise
        """
        # Find the offset from the first tile in the source group to the target
        source_positions = sorted(list(source_group))
        if not source_positions:
            return False

        first_source = source_positions[0]
        row_offset = target_row - first_source[0]
        col_offset = target_col - first_source[1]

        # Calculate where all tiles in the group would end up
        target_positions = set()
        for s_row, s_col in source_group:
            new_row = s_row + row_offset
            new_col = s_col + col_offset

            # Check if the new position is within bounds
            if not (0 <= new_row < self.tiles_y and 0 <= new_col < self.tiles_x):
                return False

            target_positions.add((new_row, new_col))

        # Get the group at the target location (if any)
        target_group = self.get_group_containing_position(target_row, target_col)

        # If there's no target group, we can only swap if target is a single tile
        # and source is a single tile
        if target_group is None:
            return len(source_group) == 1

        # Both must be groups of the same size and shape
        if len(target_group) != len(source_group):
            return False

        # Check if all target positions are occupied by tiles (in the target group or not in any group)
        for t_row, t_col in target_positions:
            # This position should either be in the target group or not in any group
            pos_group = self.get_group_containing_position(t_row, t_col)
            if pos_group is not None and pos_group != target_group:
                return False

        return True

    def swap_groups(
        self,
        source_group: Set[Tuple[int, int]],
        target_row: int,
        target_col: int
    ) -> bool:
        """
        Swap a merged group with tiles at the target location.

        Args:
            source_group: Set of positions in the source group
            target_row: Target row position
            target_col: Target column position

        Returns:
            True if swap was successful, False otherwise
        """
        if not self.can_swap_groups(source_group, target_row, target_col):
            return False

        # Find the offset
        source_positions = sorted(list(source_group))
        first_source = source_positions[0]
        row_offset = target_row - first_source[0]
        col_offset = target_col - first_source[1]

        # Calculate target positions
        target_positions = set()
        for s_row, s_col in source_group:
            new_row = s_row + row_offset
            new_col = s_col + col_offset
            target_positions.add((new_row, new_col))

        # Store the tiles at source and target positions
        source_tiles = {}
        target_tiles = {}

        for s_row, s_col in source_group:
            source_tiles[(s_row, s_col)] = self.tile_positions[s_row][s_col]

        for t_row, t_col in target_positions:
            target_tiles[(t_row, t_col)] = self.tile_positions[t_row][t_col]

        # Perform the swap
        for s_row, s_col in source_group:
            new_row = s_row + row_offset
            new_col = s_col + col_offset
            self.tile_positions[s_row][s_col] = target_tiles[(new_row, new_col)]

        for t_row, t_col in target_positions:
            orig_row = t_row - row_offset
            orig_col = t_col - col_offset
            self.tile_positions[t_row][t_col] = source_tiles[(orig_row, orig_col)]

        # Update merged groups
        self._update_merged_groups()

        return True
