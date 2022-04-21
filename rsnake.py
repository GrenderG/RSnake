import pygame
import random
import os


# noinspection PyClassHasNoInit
class Colors:
    WHITE = (255, 255, 255)
    YELLOW = (251, 208, 0)
    BLACK = (0, 0, 0)
    RED = (229, 37, 33)
    GREEN = (49, 162, 61)
    DARK_GREEN = (41, 137, 51)
    BLUE = (4, 156, 216)
    BROWN = (243, 211, 138)
    OLIVE = (128, 128, 0)
    SILVER = (192, 192, 192)


# noinspection PyClassHasNoInit
class Direction:
    NONE = 0
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
MENU_SIZE = 40
MENU_PADDING = 8

SCREEN_TITLE = 'Snake Game for RetroFW'
SCORE_TEXT = 'Size: %u'
GAME_OVER_TEXT = 'You Lost! Press Y to Play Again or X to Quit'

pygame.init()
display = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)
pygame.mouse.set_visible(False)

clock = pygame.time.Clock()
main_font_style = pygame.font.Font(os.path.abspath('etc/fonts/Caramel_Sweets.ttf'), 20)


def draw_menu(score):
    pygame.draw.polygon(display, Colors.OLIVE, [(0, SCREEN_HEIGHT - MENU_SIZE),
                                                (SCREEN_WIDTH, SCREEN_HEIGHT - MENU_SIZE),
                                                SCREEN_SIZE,
                                                (0, SCREEN_HEIGHT)])
    msg = main_font_style.render(SCORE_TEXT % score, True, Colors.WHITE)
    display.blit(msg, [MENU_PADDING, SCREEN_HEIGHT - MENU_SIZE + (msg.get_height() / 2)])


def draw_snake(snake_block, snake_parts):
    for index, part in enumerate(snake_parts):
        color = Colors.DARK_GREEN if index == len(snake_parts) - 1 else Colors.GREEN
        pygame.draw.rect(display, color, [part[0], part[1], snake_block, snake_block])


def message(text, color):
    msg = main_font_style.render(text, True, color)
    msg_rect = msg.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 3))
    display.blit(msg, msg_rect)


def main_loop():
    def gen_food_coords(is_first=False):
        new_food_x = round(random.randrange(0, SCREEN_WIDTH - block_size) / block_size) * block_size
        new_food_y = round(random.randrange(0, SCREEN_HEIGHT - MENU_SIZE - block_size) / block_size) * block_size
        if is_first:
            if new_food_x == SCREEN_WIDTH / 2 and new_food_y == (SCREEN_HEIGHT - MENU_SIZE) / 2:
                return False, -1, -1
        else:
            for part in snake_parts:
                if part[0] == new_food_x and part[1] == new_food_y:
                    return False, -1, -1
        return True, new_food_x, new_food_y

    game_over = False
    close_game = False

    x1 = SCREEN_WIDTH / 2
    y1 = (SCREEN_HEIGHT - MENU_SIZE) / 2

    current_direction = Direction.NONE

    snake_parts = []
    snake_length = 3
    block_size = 20
    snake_speed = 5

    # Spawn the first fruit and make sure it doesn't spawn in the same spot as the snake.
    while True:
        res, food_x, food_y = gen_food_coords(is_first=True)
        if res:
            break

    while not game_over:
        # Triggers when the game ends.
        while close_game:
            display.fill(Colors.BLACK)
            message(GAME_OVER_TEXT, Colors.WHITE)
            draw_menu(snake_length)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # X
                        game_over = True
                        close_game = False
                    if event.key == pygame.K_LSHIFT:  # Y
                        return True

        # Main event I/O handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if current_direction != Direction.RIGHT:
                        current_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    if current_direction != Direction.LEFT:
                        current_direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if current_direction != Direction.DOWN:
                        current_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if current_direction != Direction.UP:
                        current_direction = Direction.DOWN

                # Only handle 1 key input per tick.
                break

        # Snake out of bounds.
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT - MENU_SIZE or y1 < 0:
            close_game = True
            continue

        # Make the snake move.
        if current_direction == Direction.LEFT:
            x1 += -block_size
        elif current_direction == Direction.UP:
            y1 += -block_size
        elif current_direction == Direction.RIGHT:
            x1 += block_size
        elif current_direction == Direction.DOWN:
            y1 += block_size

        # Make sure the background is refreshed.
        display.fill(Colors.BROWN)
        # Draw fruit
        pygame.draw.rect(display, Colors.RED, [food_x, food_y, block_size, block_size])
        # Update snake head and add it to the part list.
        snake_head = [x1, y1]
        snake_parts.append(snake_head)

        # Delete the tail of the snake (to make it appear as moving).
        if len(snake_parts) > snake_length:
            del snake_parts[0]

        # Check snake collision on itself if the size > 3.
        if len(snake_parts) > 3:
            for x in snake_parts[:-1]:
                if x == snake_head:
                    close_game = True
                    continue

        draw_snake(block_size, snake_parts)
        draw_menu(snake_length)
        pygame.display.update()

        # The snake reached a fruit, generate a new one, make the snake bigger and increase speed if needed.
        if x1 == food_x and y1 == food_y:
            # Spawn fruit but prevent it from spawning inside the snake.
            while True:
                res, food_x, food_y = gen_food_coords()
                if res:
                    break

            snake_length += 1
            if snake_speed < 15:
                snake_speed += 1

        clock.tick(snake_speed)

    return False


keep_running = True
while keep_running:
    keep_running = main_loop()

pygame.quit()
quit()
