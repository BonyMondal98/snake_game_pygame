import pygame
from pygame.locals import *
import time
import random
from pygame.mixer import Sound

size = 40


class Apple:
    def __init__(self):
        self.apple_image = pygame.image.load("resources/apple.jpg").convert()

        # block is multiplied by 3 this will not render over the snake
        self.x = size*3
        self.y = size*3

    def draw(self, surface):
        surface.blit(self.apple_image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(1, 14)*size
        self.y = random.randint(1, 11)*size


# class snake use to draw the snake and draw along the x and y axis

class snake:
    def __init__(self, length):
        self.length = length
        # self.count=0.1
        self.x_axis = [size]*length
        self.y_axis = [size]*length
        self.block = pygame.image.load("resources/block.jpg").convert()

        # Initialize a direction iin downwards
        self.direction = "down"

    def draw(self, surface):
        for i in range(self.length):
            surface.blit(self.block, (self.x_axis[i], self.y_axis[i]))
        pygame.display.update()

    # Increase the the length of the snake
    def increase_length(self):
        self.length += 1
        self.x_axis.append(40)
        self.y_axis.append(40)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_right(self):
        self.direction = "right"

    def move_left(self):
        self.direction = "left"

    def walk(self, surface):
        # keep tracking of the other blocks
        for i in range(self.length-1, 0, -1):
            self.y_axis[i] = self.y_axis[i-1]
            self.x_axis[i] = self.x_axis[i-1]

        if self.direction == "up":
            self.y_axis[0] -= 40
        if self.direction == "down":
            self.y_axis[0] += 40
        if self.direction == "left":
            self.x_axis[0] -= 40
        if self.direction == "right":
            self.x_axis[0] += 40

        self.draw(surface)


# class Game use to call snake class and control event loop

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.background_music()
        self.surface = pygame.display.set_mode((600, 500))
        self.surface.fill((92, 84, 54))
        self.snake = snake(1)
        self.snake.draw(self.surface)
        self.apple = Apple()
        self.apple.draw(self.surface)

    def sound_effect(self, sound):
        effect = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(effect)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2+40:
            if y1 >= y2 and y1 < y2+40:
                return True
        return False

    def score_show(self):
        length = self.snake.length-1
        font = pygame.font.SysFont("arial", 20)
        score = font.render(
            f"Score: {length}", True, (255, 255, 255))
        self.surface.blit(score, (500, 10))

    def game_over(self):
        length = self.snake.length-1
        font = pygame.font.SysFont("arial", 20)
        score = font.render(
            f"The Game is over! Your score is: {length}", True, (255, 255, 255))
        restart = font.render(
            f"Press Enter to restart the game! or Press ESC to exit the game!", True, (255, 255, 255))
        self.surface.blit(score, (150, 200))
        self.surface.blit(restart, (35, 250))
        pygame.display.update()

    def background_image(self):
        background = pygame.image.load("resources/background.jpg")
        self.surface.blit(background, (0, 0))

    def background_music(self):
        pygame.mixer.music.load(
            "resources/background-music.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.background_image()
        self.snake.walk(self.surface)
        self.apple.draw(self.surface)
        self.score_show()
        if self.is_collision(self.snake.x_axis[0], self.snake.y_axis[0], self.apple.x, self.apple.y):
            self.sound_effect("ding")
            self.apple.move()
            self.snake.increase_length()
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x_axis[0], self.snake.y_axis[0], self.snake.x_axis[i], self.snake.y_axis[i]):
                self.sound_effect("Tada-sound")
                # Raise an exception for collision
                raise "game over"
        pygame.display.update()

    def run(self):
        running = True
        pause = False
        while running:

            # Handling events for key down, up, left, right, esc, close
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.snake.length = 1

                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception:
                # Catch the exception and call the function
                self.game_over()
                pygame.mixer.music.pause()
                pause = True
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
