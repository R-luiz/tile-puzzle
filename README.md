# Puzzle Game

A simple and elegant puzzle game built with Python and Pygame. Select an image, configure the puzzle dimensions, and enjoy viewing your images subdivided into beautiful tiles.

## Features

- **Image Selection Menu** - Choose from images in your images folder
- **Customizable Puzzle Size** - Configure tiles from 2x2 up to 20x20
- **Responsive Design** - Images automatically resize to fit your screen
- **Clean Visual Design** - Smooth borders and spacing between tiles

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
3. **View Puzzle** - Enjoy your image subdivided into tiles
   - Press ESC to return to the menu

## Adding Your Own Images

Simply add image files (JPEG, PNG, BMP, or GIF) to the `images/` folder. The game will automatically detect and display them in the selection menu.

## Controls

- **Mouse** - Click to select images and buttons, interact with UI
- **Keyboard** - Type numbers for tile configuration
- **Tab** - Switch between input fields
- **Enter** - Confirm input
- **ESC** - Return to menu from game screen

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
