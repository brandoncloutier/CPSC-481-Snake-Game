import pygame
import random
import time

#most of this code is taken from the geeks2geeks tutorial

#player is controlled using wasd, second player is controlled through arrow keys for now
#to change the second player, use ai.change_direction('left') or 'right' 'up' 'down'

snake_speed = 20

window_width = 1280
window_height = 720

mid_bar_width = 20

#could make this scalable depending on how many players, but im gonna keep it as is for 2 ppl.
split_screen_width = window_width // 2 - mid_bar_width
split_screen_height = window_height

running = True

class SnakePlayer:
    def __init__(self, screen_width, screen_height, offset = 0, tile_size = 20, fruit_size = 20):
        self.snake_speed = 20
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset

        self.tile_size = tile_size
        self.fruit_size = fruit_size

        self.running = True
        self.score = 0

        self.direction = 'right'
        self.turn_to = self.direction

        self.snake_pos = [20 + self.offset, 40]
        self.snake_body = [
                [20 + self.offset, 40],
                [20 - self.snake_speed + self.offset, 40],
                [20 - (self.snake_speed * 2) + self.offset, 40],
                [20 - (self.snake_speed * 3) + self.offset, 40]
            ]
        
        self.fruit_pos = [0,0]
        self.fruit_spawned = False
    
    def change_direction(self, turn_to):
        if turn_to == "left" and self.direction != 'right':
            self.direction = 'left'
        if turn_to == 'right' and self.direction != 'left':
            self.direction = 'right'
        if turn_to == 'up' and self.direction != 'down':
            self.direction = 'up'
        if turn_to == 'down' and self.direction != 'up':
            self.direction = 'down'
    
    def game_tick(self):
        if self.direction == 'up':
            self.snake_pos[1] -= tile_size
        if self.direction == 'down':
            self.snake_pos[1] += tile_size
        if self.direction == 'right':
            self.snake_pos[0] += tile_size
        if self.direction == 'left':
            self.snake_pos[0] -= tile_size

        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.fruit_pos[0] and self.snake_pos[1] == self.fruit_pos[1]:
            self.score += 10
            self.fruit_spawned = False
        else:
            self.snake_body.pop()

        if not self.fruit_spawned:
            self.fruit_pos = [(random.randrange(1, self.screen_width//20) * 20 + self.offset),
            (random.randrange(1, self.screen_height//20) * 20)]
            
        self.fruit_spawned = True   

        return self.snake_pos, self.snake_body, self.score, self.fruit_pos
    
def pixel_to_grid(pixel_x, pixel_y, grid_size=20):
    return pixel_x//grid_size, pixel_y//grid_size

def grid_to_pixel(grid_x, grid_y, grid_size=20):
    return grid_x * grid_size, grid_y * grid_size
    

tile_size = 20
fruit_size = 15

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

score = [0, 0]

pygame.init()
pygame.font.init()

pygame.display.set_caption("AI Snake Project")
window = pygame.display.set_mode((window_width, window_height))

fps = pygame.time.Clock()

def spawn_fruit(fruit_pos):
    pygame.draw.rect(window, red, pygame.Rect(fruit_pos[0], fruit_pos[1], 20, 20))

if __name__ == "__main__":
    player = SnakePlayer(split_screen_width, split_screen_height)

    ai = SnakePlayer(split_screen_width, split_screen_height, offset=split_screen_width + mid_bar_width)

    def render_score(player_id):
        font = pygame.font.SysFont('arial', 30)
        score_surface = font.render('Score: ' + str(score[player_id]), True, white)

        score_rect = score_surface.get_rect()
        score_rect.topleft = (10 + player_id * (split_screen_width + mid_bar_width), 10)

        window.blit(score_surface, score_rect)

    def game_over(player_id):
        font = pygame.font.SysFont('arial', 30)
        line_height = 40
        game_over_surface = font.render('Game Over!', True, white)
        text_surface = font.render('Score: ' + str(score[player_id]), True, white)

        game_rect = game_over_surface.get_rect()
        game_rect.midtop = (split_screen_width/2 + player_id * split_screen_width, split_screen_height/2 - line_height/2)

        text_rect = text_surface.get_rect()
        text_rect.midtop = (split_screen_width/2 + player_id * split_screen_width, split_screen_height/2 + line_height/2)
    

        window.blit(game_over_surface, game_rect)
        window.blit(text_surface, text_rect)
        pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                   player.change_direction('up')
                if event.key == pygame.K_s:
                    player.change_direction('down')
                if event.key == pygame.K_d:
                    player.change_direction('right')
                if event.key == pygame.K_a:
                    player.change_direction('left')

                if event.key == pygame.K_UP:
                    ai.change_direction('up')
                if event.key == pygame.K_DOWN:
                    ai.change_direction('down')
                if event.key == pygame.K_RIGHT:
                    ai.change_direction('right')
                if event.key == pygame.K_LEFT:
                    ai.change_direction('left')

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        #check to make sure the player isn't trying to turn 180 degrees into themself.            
        player_pos, player_body, score[0], player_fruit = player.game_tick()

        ai_pos, ai_body, score[1], ai_fruit = ai.game_tick()

        for tile in player_body[1:]:
            if player_pos[0] == tile[0] and player_pos[1] == tile[1]:
                player_id = 0
                running = False
        
        for tile in ai_body[1:]:
            if ai_pos[0] == tile[0] and ai_pos[1] == tile[1]:
                player_id = 1
                running = False

        if player_pos[0] >= split_screen_width or player_pos[0] < 0:
            print("player went outside of play zone1")
            player_id = 0
            running = False
        if player_pos[1] >= split_screen_height or player_pos[1] < 0:
            print("player went outside of play zone1")
            player_id = 0
            running = False

        if ai_pos[0] > window_width or ai_pos[0] < split_screen_width:
            print("ai went outside of play zone")
            player_id = 1
            running = False
        if ai_pos[1] > window_height or ai_pos[1] < 0:
            print("ai went outside of play zone1")
            player_id = 1
            running = False

        window.fill(black) # make sure that any drawing code is after this point, or else it doesn't show up.

        pygame.draw.rect(window, white, pygame.Rect(split_screen_width, 0, mid_bar_width, window_height))

        render_score(0)
        render_score(1)

        for tile in player_body:
            pygame.draw.rect(window, white, pygame.Rect(tile[0], tile[1], tile_size, tile_size))

        for tile in ai_body:
            pygame.draw.rect(window, white, pygame.Rect(tile[0], tile[1], tile_size, tile_size))
    
        spawn_fruit(player_fruit) 
        spawn_fruit(ai_fruit)

        pygame.display.update()

        fps.tick(snake_speed)
    
    print(player_id)
    game_over(player_id)
    time.sleep(2)