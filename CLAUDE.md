# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A puzzle game implemented in Python using Pygame. The game allows users to select an image from a collection, configure the puzzle dimensions, and view the image subdivided into tiles with smooth borders and spacing.

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
│   └── game_screen.py     # Main puzzle display
└── utils/                 # Utility modules
    ├── constants.py       # Game constants and configuration
    └── image_utils.py     # Image processing functions
```

## Architecture

### Game Flow
1. **Menu Screen** - User selects an image from the images folder
2. **Config Screen** - User inputs X and Y tile dimensions (2-20 range)
3. **Game Screen** - Displays the puzzle with tiles, borders, and spacing

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
- `GameScreen` class displays the puzzle with proper sizing and centering
- Image is resized to fit screen while maintaining aspect ratio
- Tiles are rendered with borders and spacing as configured

**utils/image_utils.py**
- `get_available_images()` - Scans images folder for supported formats
- `load_image()` - Loads image from disk
- `resize_image_to_fit()` - Resizes while maintaining aspect ratio
- `create_puzzle_tiles()` - Subdivides image into a 2D grid of tiles
- `calculate_tile_display_rect()` - Calculates tile position with spacing

**utils/constants.py**
- Color definitions for UI elements
- Screen dimensions and FPS settings
- Tile border width and spacing configuration
- Font sizes and UI element dimensions

## Image Handling

The game automatically handles images of varying dimensions:
- Images are resized to fit the screen while maintaining aspect ratio
- Spacing and borders are calculated to ensure tiles don't overflow the screen
- Supports JPEG, PNG, BMP, and GIF formats

Current images in `images/`:
- clair-obscur.jpg (1.2 MB)
- DSC_7858-1024x683.jpg
- P2070414-banner-1024x576.jpg
- SOLItude-Adventurer-4982-1024x706.jpg
- Torsten-Velden-2018-Banda-Sea_38-768x576.jpg
