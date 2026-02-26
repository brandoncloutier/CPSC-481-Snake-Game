import pygame
import random
import time

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

    def change_direction(self, turn_to):
        if turn_to == "left" and self.direction != "right":
            self.direction = "left"
        if turn_to == "right" and self.direction != "left":
            self.direction = "right"
        if turn_to == "up" and self.direction != "down":
            self.direction = "up"
        if turn_to == "down" and self.direction != "up":
            self.direction = "down"

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
            self.fruit_spawned = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawned:
            grid_x = random.randrange(0, self.grid_width)
            grid_y = random.randrange(0, self.grid_height)
            self.fruit_pos = [
                grid_x * self.tile_size + self.offset,
                grid_y * self.tile_size,
            ]

        self.fruit_spawned = True

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

if __name__ == "__main__":
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
                if event.key == pygame.K_w:
                    player.change_direction("up")
                if event.key == pygame.K_s:
                    player.change_direction("down")
                if event.key == pygame.K_d:
                    player.change_direction("right")
                if event.key == pygame.K_a:
                    player.change_direction("left")

                if event.key == pygame.K_UP:
                    ai.change_direction("up")
                if event.key == pygame.K_DOWN:
                    ai.change_direction("down")
                if event.key == pygame.K_RIGHT:
                    ai.change_direction("right")
                if event.key == pygame.K_LEFT:
                    ai.change_direction("left")

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
        player.update()

        # Fetching game state of AI
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
    print(player_id)
    final_score = player.score if player_id == 0 else ai.score
    game_over(window, final_score, player_id, SPLIT_SCREEN_WIDTH, SPLIT_SCREEN_HEIGHT, WHITE)
    time.sleep(2)
