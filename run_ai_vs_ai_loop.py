import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN = os.path.join(HERE, "main.py")


def main():
    env = os.environ.copy()
    env["SNAKE_MODE"] = "ai_vs_ai"

    run = 0
    try:
        while True:
            run += 1
            print(f"--- run #{run} ---")
            result = subprocess.run([sys.executable, MAIN], env=env)
            if result.returncode not in (0, None):
                print(f"main.py exited with code {result.returncode}")
    except KeyboardInterrupt:
        print(f"\nstopped after {run} run(s)")


if __name__ == "__main__":
    main()
