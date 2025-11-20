# Puzzle Game

A fully interactive puzzle game built with Python and Pygame. Select an image, configure the puzzle dimensions, and solve the puzzle by dragging and dropping tiles to recreate the original image!

## Features

- **Interactive Drag & Drop** - Drag tiles to swap positions and solve the puzzle
- **Image Selection Menu** - Choose from images in your images folder
- **Customizable Puzzle Size** - Configure tiles from 2x2 up to 20x20
- **Auto-Shuffle** - Puzzle automatically shuffles when you start
- **Win Detection** - Victory screen when puzzle is solved
- **Solution Helper** - Press Space to highlight correctly placed tiles
- **Responsive Design** - Images automatically resize to fit your screen
- **Smooth Visual Feedback** - Hover effects, drag transparency, and clean borders

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## How to Play

1. **Select Image** - Click on an image from the menu to select it for your puzzle
2. **Configure Tiles** - Enter the number of tiles for X (horizontal) and Y (vertical) dimensions
   - Use keyboard to type numbers (2-20 range)
   - Press Tab to switch between fields
   - Press Enter or click "Start Game" to begin
3. **Solve the Puzzle** - The puzzle starts shuffled - drag tiles to swap and recreate the image
   - Click and hold a tile to start dragging
   - Drag it over another tile and release to swap positions
   - Use the Solution button or Space key to see which tiles are correctly placed
   - Press S to shuffle again, R to restart
   - Victory screen appears when puzzle is solved!

## Adding Your Own Images

Simply add image files (JPEG, PNG, BMP, or GIF) to the `images/` folder. The game will automatically detect and display them in the selection menu.

## Controls

### Menu & Configuration
- **Mouse** - Click to select images and buttons
- **Keyboard** - Type numbers for tile configuration
- **Tab** - Switch between input fields
- **Enter** - Confirm input and start game

### During Gameplay
- **Mouse Drag** - Click and drag tiles to swap positions
- **S Key** - Shuffle the puzzle
- **R Key** - Restart (shuffle) the puzzle
- **Space Key** - Toggle solution mode (highlights correct tiles in green)
- **Shuffle Button** - Click to shuffle the puzzle
- **Restart Button** - Click to restart the puzzle
- **Solution Button** - Click to toggle solution hints
- **ESC** - Return to main menu

## Requirements

- Python 3.7+
- Pygame 2.5.2

## Project Structure

- `main.py` - Main game entry point
- `screens/` - Game screens (menu, config, game)
- `utils/` - Utility functions and constants
- `images/` - Puzzle image assets

## License

This project is open source and available for personal and educational use.
