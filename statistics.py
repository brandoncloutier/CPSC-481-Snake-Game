import argparse
import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_stats.csv")

SNAKE_COLORS = {"player": "tab:blue", "ai": "tab:red"}


def load_stats(path, difficulty):
    by_snake = defaultdict(lambda: {"avg_turns": [], "avg_spaces": []})
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["difficulty"] != difficulty:
                continue
            # Skip games where the snake never ate an apple — averages are 0 and not meaningful
            if int(row["apples"]) == 0:
                continue
            by_snake[row["snake"]]["avg_turns"].append(float(row["avg_turns"]))
            by_snake[row["snake"]]["avg_spaces"].append(float(row["avg_spaces"]))
    return by_snake


def plot_distribution(ax, values_by_snake, title, xlabel):
    all_values = [v for vals in values_by_snake.values() for v in vals]
    if not all_values:
        ax.set_title(f"{title} (no data)")
        return

    span = max(all_values) - min(all_values) or 1.0
    xs = np.linspace(min(all_values) - span * 0.2, max(all_values) + span * 0.2, 300)

    for snake, values in values_by_snake.items():
        if len(values) < 2:
            continue
        kde = gaussian_kde(values)
        ys = kde(xs)
        color = SNAKE_COLORS.get(snake, "tab:gray")
        label = f"{snake} (μ={np.mean(values):.2f}, σ={np.std(values):.2f}, n={len(values)})"
        ax.plot(xs, ys, color=color, linewidth=2, label=label)
        ax.fill_between(xs, ys, alpha=0.2, color=color)
        ax.axvline(np.mean(values), color=color, linestyle="--", alpha=0.6)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Density")
    ax.legend()


def main():
    parser = argparse.ArgumentParser(description="Plot player vs AI stat distributions for a given difficulty.")
    parser.add_argument("difficulty", choices=["easy", "medium", "hard", "ai_vs_ai"], help="Which difficulty's games to plot")
    args = parser.parse_args()

    data = load_stats(CSV_PATH, args.difficulty)

    fig, (ax_turns, ax_spaces) = plt.subplots(1, 2, figsize=(13, 5))

    plot_distribution(
        ax_turns,
        {snake: d["avg_turns"] for snake, d in data.items()},
        "Average Turns per Apple",
        "Avg turns",
    )
    plot_distribution(
        ax_spaces,
        {snake: d["avg_spaces"] for snake, d in data.items()},
        "Average Spaces per Apple",
        "Avg spaces",
    )

    fig.suptitle(f"Player vs AI — {args.difficulty} mode")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
