import csv
import os
import shutil

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_stats.csv")
BACKUP_PATH = CSV_PATH + ".bak"

WINNER_REMAP = {"player": "bfs", "ai": "a_star"}
SNAKE_REMAP = {"player": "bfs", "ai": "a_star"}


def migrate():
    shutil.copyfile(CSV_PATH, BACKUP_PATH)

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0
    for row in rows:
        if row["difficulty"] != "ai_vs_ai":
            continue
        row["winner"] = WINNER_REMAP.get(row["winner"], row["winner"])
        row["snake"] = SNAKE_REMAP.get(row["snake"], row["snake"])
        updated += 1

    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Migrated {updated} ai_vs_ai rows. Backup at {BACKUP_PATH}")


if __name__ == "__main__":
    migrate()
