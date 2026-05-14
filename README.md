# AI Snake Project

A split-screen Snake game built with [pygame](https://www.pygame.org/) for CPSC 481. The left half of the screen is one snake and the right half is another. Depending on the mode you pick, you either play against an AI snake or watch two AI snakes compete.

The AI snakes find their way to fruit using classic pathfinding algorithms:

- **Easy** — AI uses Depth-First Search (DFS)
- **Medium** — AI uses Breadth-First Search (BFS)
- **Hard** — AI uses A\* search
- **BFS vs A\*** — two AI snakes race each other, BFS on the left and A\* on the right

When a snake crashes (into itself or a wall) it stops, but the game keeps running so the other snake can keep going. Every finished game appends a row of stats (score, apples eaten, average turns and spaces traveled per apple, winner) to `game_stats.csv`.

## Controls

- **WASD** — move the player snake (left side), in Easy/Medium/Hard modes
- **1 / 2 / 3 / 4** — pick a mode from the start menu
- **ESC** — quit

## Requirements

- Python 3
- [pygame](https://www.pygame.org/) — the game itself
- [matplotlib](https://matplotlib.org/), [numpy](https://numpy.org/), [scipy](https://scipy.org/) — only needed for the stats plotting script

Install everything with:

```bash
pip install pygame matplotlib numpy scipy
```

## Running the game

From the project directory:

```bash
python main.py
```

This opens the start menu where you choose a mode with the number keys.

To skip the menu and jump straight into a mode, set the `SNAKE_MODE` environment variable to `easy`, `medium`, `hard`, or `ai_vs_ai`:

```bash
SNAKE_MODE=ai_vs_ai python main.py
```

## Running AI vs AI on a loop

To repeatedly run BFS vs A\* games back-to-back (useful for collecting stats), run:

```bash
python run_ai_vs_ai_loop.py
```

It launches `main.py` in `ai_vs_ai` mode over and over until you stop it with Ctrl+C.

## Viewing the stats

`statistics.py` reads `game_stats.csv` and plots distributions of turns, spaces, and score using matplotlib. Pass a mode to plot:

```bash
python statistics.py easy
python statistics.py medium
python statistics.py hard
python statistics.py ai_vs_ai
```

You can also plot just the score distribution by appending `_score`:

```bash
python statistics.py ai_vs_ai_score
```
