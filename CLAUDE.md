# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A fully interactive puzzle game implemented in Python using Pygame. Players select an image, configure puzzle dimensions, and solve the puzzle by dragging and dropping tiles to recreate the original image. Features include automatic shuffling, win detection, solution hints, and smooth drag-and-drop mechanics.

## Running the Game

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

## Project Structure

```
jeu puzzle/
├── main.py                 # Entry point and game state management
├── requirements.txt        # Python dependencies (pygame)
├── images/                 # Puzzle image assets (JPEG/PNG)
├── screens/               # Screen modules
│   ├── menu_screen.py     # Image selection menu
│   ├── config_screen.py   # Tile configuration input
│   └── game_screen.py     # Main puzzle display with drag-and-drop
└── utils/                 # Utility modules
    ├── constants.py       # Game constants and configuration
    ├── image_utils.py     # Image processing functions
    └── puzzle_logic.py    # Puzzle state and mechanics
```

## Architecture

### Game Flow
1. **Menu Screen** - User selects an image from the images folder
2. **Config Screen** - User inputs X and Y tile dimensions (2-20 range)
3. **Game Screen** - Puzzle is automatically shuffled; player drags tiles to solve

### Key Components

**main.py**
- `PuzzleGame` class manages overall game state using `GameState` enum
- Main game loop handles events, updates, and rendering
- State transitions between MENU → CONFIG → GAME → MENU

**screens/menu_screen.py**
- `MenuScreen` class displays available images as clickable buttons
- Automatically discovers images from the images folder
- Supports hover effects and click selection

**screens/config_screen.py**
- `ConfigScreen` class handles user input for tile dimensions
- Input validation ensures values are within MIN_TILES to MAX_TILES range
- Supports keyboard input, Tab/Enter navigation, and mouse interaction

**screens/game_screen.py**
- `GameScreen` class displays the puzzle with drag-and-drop mechanics
- Tiles can be dragged and dropped to swap positions
- Visual feedback: hover effects, drag transparency, correct tile highlighting
- Win detection automatically triggers when puzzle is solved
- UI controls: Shuffle, Restart, Solution (shows correct tiles in green)
- Keyboard shortcuts: S (shuffle), R (restart), Space (toggle solution), ESC (menu)
- Image is resized to fit screen while maintaining aspect ratio

**utils/image_utils.py**
- `get_available_images()` - Scans images folder for supported formats
- `load_image()` - Loads image from disk
- `resize_image_to_fit()` - Resizes while maintaining aspect ratio
- `create_puzzle_tiles()` - Subdivides image into a 2D grid of tiles
- `calculate_tile_display_rect()` - Calculates tile position with spacing

**utils/constants.py**
- Color definitions for UI elements (including drag, hover, win states)
- Screen dimensions and FPS settings
- Tile border width, spacing, and drag transparency
- Font sizes and UI element dimensions
- Game button dimensions for in-game controls

**utils/puzzle_logic.py**
- `PuzzleState` class manages tile positions and game logic
- `shuffle()` - Randomly shuffles tiles by performing random swaps
- `swap_tiles()` - Swaps two tiles at given positions
- `is_solved()` - Checks if puzzle is in solved state
- `get_tile_at_position()` - Returns which original tile is at a position
- `get_correctness_grid()` - Returns grid showing correctly placed tiles

## Game Mechanics

### Drag and Drop
- Click and hold on any tile to start dragging
- Drag the tile over another tile to swap their positions
- Dragged tile becomes semi-transparent and follows the mouse
- Tiles are swapped when the mouse is released over another tile

### Puzzle State
- Puzzle is automatically shuffled when game starts
- Tile positions are tracked using a 2D grid
- Each position stores which original tile is currently there
- Win condition: all tiles are in their original positions

### Visual Feedback
- **Hover Effect**: Tiles have a blue border when hovered
- **Drag Effect**: Dragged tile becomes semi-transparent with blue border
- **Solution Mode**: Press Space to highlight correctly placed tiles in green
- **Win State**: Semi-transparent green overlay with victory message

### Controls
- **Mouse**: Drag tiles to swap positions, click buttons
- **S Key**: Shuffle the puzzle
- **R Key**: Restart (shuffle) the puzzle
- **Space Key**: Toggle solution mode (shows correct tiles)
- **ESC Key**: Return to main menu

## Image Handling

The game automatically handles images of varying dimensions:
- Images are resized to fit the screen while maintaining aspect ratio
- Spacing and borders are calculated to ensure tiles don't overflow the screen
- Supports JPEG, PNG, BMP, and GIF formats
- Tiles are extracted from the resized image and tracked independently

Current images in `images/`:
- clair-obscur.jpg (1.2 MB)
- DSC_7858-1024x683.jpg
- P2070414-banner-1024x576.jpg
- SOLItude-Adventurer-4982-1024x706.jpg
- Torsten-Velden-2018-Banda-Sea_38-768x576.jpg
