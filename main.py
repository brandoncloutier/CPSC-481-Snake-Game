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

score = [0, 0]

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
        self, screen_width, screen_height, offset=0, TILE_SIZE=20, FRUIT_SIZE=20
    ):
        self.SNAKE_SPEED = 20
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        self.TILE_SIZE = TILE_SIZE
        self.FRUIT_SIZE = FRUIT_SIZE

        self.running = True
        self.score = 0

        self.direction = "right"
        self.turn_to = self.direction

        self.snake_pos = [20 + self.offset, 40]
        self.snake_body = [
            [20 + self.offset, 40],
            [20 - self.SNAKE_SPEED + self.offset, 40],
            [20 - (self.SNAKE_SPEED * 2) + self.offset, 40],
            [20 - (self.SNAKE_SPEED * 3) + self.offset, 40],
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

    def game_tick(self):
        if self.direction == "up":
            self.snake_pos[1] -= TILE_SIZE
        if self.direction == "down":
            self.snake_pos[1] += TILE_SIZE
        if self.direction == "right":
            self.snake_pos[0] += TILE_SIZE
        if self.direction == "left":
            self.snake_pos[0] -= TILE_SIZE

        self.snake_body.insert(0, list(self.snake_pos))
        if (
            self.snake_pos[0] == self.fruit_pos[0]
            and self.snake_pos[1] == self.fruit_pos[1]
        ):
            self.score += 10
            self.fruit_spawned = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawned:
            self.fruit_pos = [
                (random.randrange(1, self.screen_width // 20) * 20 + self.offset),
                (random.randrange(1, self.screen_height // 20) * 20),
            ]

        self.fruit_spawned = True

        return self.snake_pos, self.snake_body, self.score, self.fruit_pos


def pixel_to_grid(pixel_x, pixel_y, grid_size=20):
    return pixel_x // grid_size, pixel_y // grid_size


def grid_to_pixel(grid_x, grid_y, grid_size=20):
    return grid_x * grid_size, grid_y * grid_size


def render_score(player_id):
    font = pygame.font.SysFont("arial", 30)
    score_surface = font.render("Score: " + str(score[player_id]), True, WHITE)

    score_rect = score_surface.get_rect()
    score_rect.topleft = (10 + player_id * (SPLIT_SCREEN_WIDTH + MID_BAR_WIDTH), 10)

    window.blit(score_surface, score_rect)


def game_over(player_id):
    font = pygame.font.SysFont("arial", 30)
    line_height = 40
    game_over_surface = font.render("Game Over!", True, WHITE)
    text_surface = font.render("Score: " + str(score[player_id]), True, WHITE)

    game_rect = game_over_surface.get_rect()
    game_rect.midtop = (
        SPLIT_SCREEN_WIDTH / 2 + player_id * SPLIT_SCREEN_WIDTH,
        SPLIT_SCREEN_HEIGHT / 2 - line_height / 2,
    )

    text_rect = text_surface.get_rect()
    text_rect.midtop = (
        SPLIT_SCREEN_WIDTH / 2 + player_id * SPLIT_SCREEN_WIDTH,
        SPLIT_SCREEN_HEIGHT / 2 + line_height / 2,
    )

    window.blit(game_over_surface, game_rect)
    window.blit(text_surface, text_rect)
    pygame.display.flip()


def spawn_fruit(fruit_pos):
    pygame.draw.rect(window, RED, pygame.Rect(fruit_pos[0], fruit_pos[1], 20, 20))


if __name__ == "__main__":
    # Initializing Player and AI game objects
    player = SnakePlayer(SPLIT_SCREEN_WIDTH, SPLIT_SCREEN_HEIGHT)
    ai = SnakePlayer(
        SPLIT_SCREEN_WIDTH,
        SPLIT_SCREEN_HEIGHT,
        offset=SPLIT_SCREEN_WIDTH + MID_BAR_WIDTH,
    )

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
        player_pos, player_body, score[0], player_fruit = player.game_tick()

        # Fetching game state of AI
        ai_pos, ai_body, score[1], ai_fruit = ai.game_tick()

        # =================================
        # Checking for game over conditions
        # =================================

        # Checks for Player self collision
        for tile in player_body[1:]:
            if player_pos[0] == tile[0] and player_pos[1] == tile[1]:
                player_id = 0
                running = False

        # Checks for AI self collision
        for tile in ai_body[1:]:
            if ai_pos[0] == tile[0] and ai_pos[1] == tile[1]:
                player_id = 1
                running = False

        # Checks for Player out of bounds
        if player_pos[0] >= SPLIT_SCREEN_WIDTH or player_pos[0] < 0:
            print("player went outside of play zone1")
            player_id = 0
            running = False
        if player_pos[1] >= SPLIT_SCREEN_HEIGHT or player_pos[1] < 0:
            print("player went outside of play zone1")
            player_id = 0
            running = False

        # Checks for AI out of bounds
        if ai_pos[0] > WINDOW_WIDTH or ai_pos[0] < SPLIT_SCREEN_WIDTH:
            print("ai went outside of play zone")
            player_id = 1
            running = False
        if ai_pos[1] > WINDOW_HEIGHT or ai_pos[1] < 0:
            print("ai went outside of play zone1")
            player_id = 1
            running = False

        # ==================
        # Drawing the Canvas
        # ==================
        window.fill(
            BLACK
        )  # make sure that any drawing code is after this point, or else it doesn't show up.

        pygame.draw.rect(
            window,
            WHITE,
            pygame.Rect(SPLIT_SCREEN_WIDTH, 0, MID_BAR_WIDTH, WINDOW_HEIGHT),
        )

        render_score(0)
        render_score(1)

        for tile in player_body:
            pygame.draw.rect(
                window, WHITE, pygame.Rect(tile[0], tile[1], TILE_SIZE, TILE_SIZE)
            )

        for tile in ai_body:
            pygame.draw.rect(
                window, WHITE, pygame.Rect(tile[0], tile[1], TILE_SIZE, TILE_SIZE)
            )

        spawn_fruit(player_fruit)
        spawn_fruit(ai_fruit)

        pygame.display.update()

        fps.tick(SNAKE_SPEED)

    # ================================================================================================
    # END GAME Process
    # ================================================================================================
    print(player_id)
    game_over(player_id)
    time.sleep(2)
