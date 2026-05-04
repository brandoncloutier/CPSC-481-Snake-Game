import pygame
import random
import time
import heapq
import csv
import os
from datetime import datetime
from collections import deque

# most of this code is taken from the geeks2geeks tutorial

# player is controlled using wasd, second player is controlled through arrow keys for now
# to change the second player, use ai.change_direction('left') or 'right' 'up' 'down'

SNAKE_SPEED = 20

running = True

TILE_SIZE = 20
FRUIT_SIZE = 15

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
YELLOW = pygame.Color(255, 255, 0)
CYAN = pygame.Color(0, 255, 255)

pygame.init()
pygame.font.init()
pygame.display.set_caption("AI Snake Project")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
MID_BAR_WIDTH = 20
SPLIT_SCREEN_WIDTH = WINDOW_WIDTH // 2 - MID_BAR_WIDTH
SPLIT_SCREEN_HEIGHT = WINDOW_HEIGHT
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

fps = pygame.time.Clock()

class Statistics:
    def __init__ (self):
        self._apple_counter = 0

        self._current_number_of_turns_taken = 0    
        self._average_number_of_turns_taken = 0

        self._current_number_of_spaces_traversed = 0
        self._average_number_of_spaces_traversed = 0
        
    
    def increment_current_number_of_turns_taken(self):
        self._current_number_of_turns_taken += 1

    def increment_current_number_of_spaces_traversed(self):
        self._current_number_of_spaces_traversed += 1

    def record_apple(self):
        self._apple_counter += 1

        # Incremental mean: new_avg = old_avg + (sample - old_avg) / n
        self._average_number_of_turns_taken += (
            self._current_number_of_turns_taken - self._average_number_of_turns_taken
        ) / self._apple_counter
        self._average_number_of_spaces_traversed += (
            self._current_number_of_spaces_traversed - self._average_number_of_spaces_traversed
        ) / self._apple_counter

        self._current_number_of_turns_taken = 0
        self._current_number_of_spaces_traversed = 0

        print(
            f"Apple #{self._apple_counter} collected | "
            f"avg turns: {self._average_number_of_turns_taken:.2f} | "
            f"avg spaces: {self._average_number_of_spaces_traversed:.2f}"
        )

    def summary(self):
        return {
            "apples": self._apple_counter,
            "avg_turns": round(self._average_number_of_turns_taken, 2),
            "avg_spaces": round(self._average_number_of_spaces_traversed, 2),
        }
    

    


class SnakePlayer:
    def __init__(
        self, screen_width, screen_height, offset=0, tile_size=TILE_SIZE, fruit_size=FRUIT_SIZE
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        self.tile_size = tile_size
        self.fruit_size = fruit_size
        self.grid_width = self.screen_width // self.tile_size
        self.grid_height = self.screen_height // self.tile_size

        self.score = 0

        self.direction = "right"
        self.turn_to = self.direction

        start_x, start_y = grid_to_pixel(1, 2, self.tile_size)
        self.snake_pos = [start_x + self.offset, start_y]
        self.snake_body = [
            # Initial Body
            [start_x + self.offset, start_y],
            [start_x - self.tile_size + self.offset, start_y],
            [start_x - (self.tile_size * 2) + self.offset, start_y],
            [start_x - (self.tile_size * 3) + self.offset, start_y],
        ]

        self.fruit_pos = [0, 0]
        self.fruit_spawned = False

        self.cached_path = []

        self.statistics = Statistics()

    def change_direction(self, turn_to):
        if turn_to == "left" and self.direction != "right" and turn_to != self.direction:
            self.direction = "left"
            self.statistics.increment_current_number_of_turns_taken()
        
        elif turn_to == "right" and self.direction != "left" and turn_to != self.direction:
            self.direction = "right"
            self.statistics.increment_current_number_of_turns_taken()
            
        elif turn_to == "up" and self.direction != "down" and turn_to != self.direction:
            self.direction = "up"
            self.statistics.increment_current_number_of_turns_taken()
            
        elif turn_to == "down" and self.direction != "up" and turn_to != self.direction:
            self.direction = "down"
            self.statistics.increment_current_number_of_turns_taken()
            

    def update(self):
        if self.direction == "up":
            self.snake_pos[1] -= self.tile_size
        if self.direction == "down":
            self.snake_pos[1] += self.tile_size
        if self.direction == "right":
            self.snake_pos[0] += self.tile_size
        if self.direction == "left":
            self.snake_pos[0] -= self.tile_size

        self.snake_body.insert(0, list(self.snake_pos))
        if (self.snake_pos[0] == self.fruit_pos[0] and self.snake_pos[1] == self.fruit_pos[1]):
            self.score += 10
            self.statistics.record_apple()
            self.fruit_spawned = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawned:
            while True:
                grid_x = random.randrange(0, self.grid_width)
                grid_y = random.randrange(0, self.grid_height)
                fruit_pos = [
                    grid_x * self.tile_size + self.offset,
                    grid_y * self.tile_size,
                ]
                if fruit_pos not in self.snake_body:
                    self.fruit_pos = fruit_pos
                    break

        self.fruit_spawned = True
        self.statistics.increment_current_number_of_spaces_traversed()

    def is_self_collision(self):
        for tile in self.snake_body[1:]:
            if self.snake_pos[0] == tile[0] and self.snake_pos[1] == tile[1]:
                return True
        return False

    def is_out_of_bounds(self, min_x, max_x, min_y, max_y):
        if (self.snake_pos[0] < min_x or self.snake_pos[0] >= max_x or self.snake_pos[1] < min_y or self.snake_pos[1] >= max_y):
            return True
        return False

    def render(self, surface, color):
        for tile in self.snake_body:
            pygame.draw.rect(surface, color, pygame.Rect(tile[0], tile[1], self.tile_size, self.tile_size))

        pygame.draw.rect(surface, RED, pygame.Rect(self.fruit_pos[0], self.fruit_pos[1], self.fruit_size, self.fruit_size),)


def pixel_to_grid(pixel_x, pixel_y, grid_size=TILE_SIZE):
    return pixel_x // grid_size, pixel_y // grid_size


def grid_to_pixel(grid_x, grid_y, grid_size=TILE_SIZE):
    return grid_x * grid_size, grid_y * grid_size


STATS_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_stats.csv")
STATS_CSV_FIELDS = [
    "timestamp", "difficulty", "winner", "snake", "score", "apples", "avg_turns", "avg_spaces",
]


def log_game_stats(difficulty, winner, player, ai):
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = []
    for label, snake in (("player", player), ("ai", ai)):
        stats = snake.statistics.summary()
        rows.append({
            "timestamp": timestamp,
            "difficulty": difficulty,
            "winner": winner,
            "snake": label,
            "score": snake.score,
            "apples": stats["apples"],
            "avg_turns": stats["avg_turns"],
            "avg_spaces": stats["avg_spaces"],
        })

    write_header = not os.path.exists(STATS_CSV_PATH) or os.path.getsize(STATS_CSV_PATH) == 0
    with open(STATS_CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=STATS_CSV_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def render_score(surface, score_value, player_id, split_screen_width, mid_bar_width, color):
    font = pygame.font.SysFont("arial", 30)
    score_surface = font.render("Score: " + str(score_value), True, color)

    score_rect = score_surface.get_rect()
    score_rect.topleft = (10 + player_id * (split_screen_width + mid_bar_width), 10)

    surface.blit(score_surface, score_rect)


def game_over(surface, score_value, player_id, split_screen_width, split_screen_height, color):
    font = pygame.font.SysFont("arial", 30)
    line_height = 40
    game_over_surface = font.render("Game Over!", True, color)
    text_surface = font.render("Score: " + str(score_value), True, color)

    game_rect = game_over_surface.get_rect()
    game_rect.midtop = ( split_screen_width / 2 + player_id * split_screen_width, split_screen_height / 2 - line_height / 2)

    text_rect = text_surface.get_rect()
    text_rect.midtop = (split_screen_width / 2 + player_id * split_screen_width, split_screen_height / 2 + line_height / 2)

    surface.blit(game_over_surface, game_rect)
    surface.blit(text_surface, text_rect)
    pygame.display.flip()


def draw_menu(surface):
    surface.fill(BLACK)

    title_font = pygame.font.SysFont("arial", 50)
    option_font = pygame.font.SysFont("arial", 30)

    title_surface = title_font.render("AI Snake Project", True, WHITE)
    easy_surface = option_font.render("Press 1 for Easy Mode (DFS)", True, GREEN)
    medium_surface = option_font.render("Press 2 for Medium Mode (BFS)", True, YELLOW)
    hard_surface = option_font.render("Press 3 for Hard Mode (A*)", True, RED)
    ai_vs_ai_surface = option_font.render("Press 4 for BFS vs A*", True, CYAN)
    quit_surface = option_font.render("Press ESC to Quit", True, WHITE)

    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
    easy_rect = easy_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    medium_rect = medium_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    hard_rect = hard_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
    ai_vs_ai_rect = ai_vs_ai_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
    quit_rect = quit_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 170))

    surface.blit(title_surface, title_rect)
    surface.blit(easy_surface, easy_rect)
    surface.blit(medium_surface, medium_rect)
    surface.blit(hard_surface, hard_rect)
    surface.blit(ai_vs_ai_surface, ai_vs_ai_rect)
    surface.blit(quit_surface, quit_rect)

    pygame.display.update()


def start_menu(surface):
    while True:
        draw_menu(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "medium"
                if event.key == pygame.K_3:
                    return "hard"
                if event.key == pygame.K_4:
                    return "ai_vs_ai"
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


def get_neighbors(position, min_x, max_x, min_y, max_y, tile_size):
    x, y = position
    neighbors = [
        (x + tile_size, y),
        (x - tile_size, y),
        (x, y + tile_size),
        (x, y - tile_size),
    ]

    valid_neighbors = []

    for neighbor_x, neighbor_y in neighbors:
        if neighbor_x >= min_x and neighbor_x < max_x and neighbor_y >= min_y and neighbor_y < max_y:
            valid_neighbors.append((neighbor_x, neighbor_y))

    return valid_neighbors


def dfs(ai, min_x, max_x, min_y, max_y):
    start = (ai.snake_pos[0], ai.snake_pos[1])
    goal = (ai.fruit_pos[0], ai.fruit_pos[1])

    stack = [start]
    visited = set()
    visited.add(start)
    parent = {}

    blocked = set()
    for tile in ai.snake_body[1:]:
        blocked.add((tile[0], tile[1]))

    while stack:
        current = stack.pop()

        if current == goal:
            break

        neighbors = get_neighbors(current, min_x, max_x, min_y, max_y, ai.tile_size)

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in blocked:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    if goal not in parent and goal != start:
        return []

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def bfs(ai, min_x, max_x, min_y, max_y):
    start = (ai.snake_pos[0], ai.snake_pos[1])
    goal = (ai.fruit_pos[0], ai.fruit_pos[1])

    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {}

    blocked = set()
    for tile in ai.snake_body[1:]:
        blocked.add((tile[0], tile[1]))

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        neighbors = get_neighbors(current, min_x, max_x, min_y, max_y, ai.tile_size)

        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in blocked:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent and goal != start:
        return []

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


def a_star(ai, min_x, max_x, min_y, max_y):
    start = (ai.snake_pos[0], ai.snake_pos[1])
    goal = (ai.fruit_pos[0], ai.fruit_pos[1])

    # Manhattan distance heuristic function
    def heuristic(a, b):
        return (abs(a[0] - b[0]) + abs(a[1] - b[1])) // ai.tile_size

    blocked = set()
    for tile in ai.snake_body[1:]:
        blocked.add((tile[0], tile[1]))

    open_set = [(heuristic(start, goal), 0, start)]
    came_from = {}
    g_score = {start: 0}
    counter = 1

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current, min_x, max_x, min_y, max_y, ai.tile_size):
            if neighbor in blocked:
                continue

            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, counter, neighbor))
                counter += 1

    return []


def ai_move_from_path(ai, path):
    if len(path) == 0:
        return

    next_pos = path[0]

    if next_pos[0] > ai.snake_pos[0]:
        ai.change_direction("right")
    if next_pos[0] < ai.snake_pos[0]:
        ai.change_direction("left")
    if next_pos[1] > ai.snake_pos[1]:
        ai.change_direction("down")
    if next_pos[1] < ai.snake_pos[1]:
        ai.change_direction("up")


def ai_move(snake, algorithm, min_x, max_x, min_y, max_y):
    if algorithm == "dfs":
        if not snake.cached_path:
            snake.cached_path = dfs(snake, min_x, max_x, min_y, max_y)
        ai_move_from_path(snake, snake.cached_path)
        if snake.cached_path:
            snake.cached_path.pop(0)

    if algorithm == "bfs":
        path = bfs(snake, min_x, max_x, min_y, max_y)
        ai_move_from_path(snake, path)

    if algorithm == "a_star":
        path = a_star(snake, min_x, max_x, min_y, max_y)
        ai_move_from_path(snake, path)


DIFFICULTY_TO_ALGORITHM = {
    "easy": "dfs",
    "medium": "bfs",
    "hard": "a_star",
}


if __name__ == "__main__":
    difficulty = os.environ.get("SNAKE_MODE") or start_menu(window)

    # Initializing Player and AI game objects
    player = SnakePlayer(SPLIT_SCREEN_WIDTH, SPLIT_SCREEN_HEIGHT)
    ai = SnakePlayer(SPLIT_SCREEN_WIDTH, SPLIT_SCREEN_HEIGHT, offset=SPLIT_SCREEN_WIDTH + MID_BAR_WIDTH)


    # ================================================================================================
    # MAIN GAME LOOP
    # ================================================================================================
    while running:
        # Checks for player Input and invokes a movement action
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if difficulty != "ai_vs_ai":
                    if event.key == pygame.K_w:
                        player.change_direction("up")
                    if event.key == pygame.K_s:
                        player.change_direction("down")
                    if event.key == pygame.K_d:
                        player.change_direction("right")
                    if event.key == pygame.K_a:
                        player.change_direction("left")

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # TODO: AI code to invoke movement actions
        # Check if a path data structure has direction instructions: (path will be a queue or some data structure)
        #
        # EX: path = [ ((0, 2, "right"), "down", (1, 2, "down")), ...(more direction instructions) ]
        #
        # path = [ Tuple(direction_instrction), Tuple(Direction_instruction) ]
        # Tuple(direction_instrction) = ( (initial_head_row, initial_head_col, "direction currently facing"), "direction instruction", (resulting_head_row, resulting_head_col, "direction currently facing") )
        #
        #  --> If path is empty: -> generate a path with an algorithm (A*) and populate the path data structure
        # Check the next move in the path and set the direction + remove the the front of the data structure
        # This will be called every game tick.

        # Fetching game state of player
        if difficulty == "ai_vs_ai":
            ai_move(player, "bfs", 0, SPLIT_SCREEN_WIDTH, 0, SPLIT_SCREEN_HEIGHT)
        player.update()

        # Fetching game state of AI
        if difficulty == "ai_vs_ai":
            ai_move(ai, "a_star", SPLIT_SCREEN_WIDTH + MID_BAR_WIDTH, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        else:
            ai_move(ai, DIFFICULTY_TO_ALGORITHM[difficulty], SPLIT_SCREEN_WIDTH + MID_BAR_WIDTH, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        ai.update()

        # =================================
        # Checking for game over conditions
        # =================================

        # Checks for Player self collision
        if player.is_self_collision():
            player_id = 0
            running = False

        # Checks for AI self collision
        if ai.is_self_collision():
            player_id = 1
            running = False

        # Checks for Player out of bounds
        if player.is_out_of_bounds(0, SPLIT_SCREEN_WIDTH, 0, SPLIT_SCREEN_HEIGHT):
            print("player went outside of play zone1")
            player_id = 0
            running = False

        # Checks for AI out of bounds
        if ai.is_out_of_bounds(SPLIT_SCREEN_WIDTH, WINDOW_WIDTH, 0, WINDOW_HEIGHT):
            print("ai went outside of play zone")
            player_id = 1
            running = False

        # ==================
        # Drawing the Canvas
        # ==================
        window.fill(BLACK)  # make sure that any drawing code is after this point, or else it doesn't show up.

        pygame.draw.rect(window, WHITE, pygame.Rect(SPLIT_SCREEN_WIDTH, 0, MID_BAR_WIDTH, WINDOW_HEIGHT))

        render_score(window, player.score, 0, SPLIT_SCREEN_WIDTH, MID_BAR_WIDTH, WHITE)
        render_score(window, ai.score, 1, SPLIT_SCREEN_WIDTH, MID_BAR_WIDTH, WHITE)

        player.render(window, WHITE)
        ai.render(window, WHITE)

        pygame.display.update()

        fps.tick(SNAKE_SPEED)

    # ================================================================================================
    # END GAME Process
    # ================================================================================================
    final_score = player.score if player_id == 0 else ai.score
    winner = "ai" if player_id == 0 else "player"
    log_game_stats(difficulty, winner, player, ai)
    game_over(window, final_score, player_id, SPLIT_SCREEN_WIDTH, SPLIT_SCREEN_HEIGHT, WHITE)
    time.sleep(2)
