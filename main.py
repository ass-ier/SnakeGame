import pygame
import random

pygame.init()

WIDTH, HEIGHT, CELL_SIZE = 400, 400, 20
SNAKE_COLOR, FOOD_COLOR = (0, 255, 0), (255, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next_node = self.head
        self.head = new_node

    def remove_last(self):
        if self.head is None:
            return
        if self.head.next_node is None:
            self.head = None
            return
        current = self.head
        while current.next_node.next_node is not None:
            current = current.next_node
        current.next_node = None

class Snake:
    def __init__(self):
        self.body = LinkedList()
        self.body.insert_at_beginning((100, 100))
        self.direction = "RIGHT"

    def move(self):
        head_x, head_y = self.body.head.data
        if self.direction == "UP":
            head_y -= CELL_SIZE
        elif self.direction == "DOWN":
            head_y += CELL_SIZE
        elif self.direction == "LEFT":
            head_x -= CELL_SIZE
        elif self.direction == "RIGHT":
            head_x += CELL_SIZE

        self.body.insert_at_beginning((head_x, head_y))
        self.body.remove_last()

    def grow(self):
        head_x, head_y = self.body.head.data
        if self.direction == "UP":
            head_y -= CELL_SIZE
        elif self.direction == "DOWN":
            head_y += CELL_SIZE
        elif self.direction == "LEFT":
            head_x -= CELL_SIZE
        elif self.direction == "RIGHT":
            head_x += CELL_SIZE

        self.body.insert_at_beginning((head_x, head_y))

    def change_direction(self, new_direction):
        if (new_direction == "UP" and not self.direction == "DOWN" or
            new_direction == "DOWN" and not self.direction == "UP" or
            new_direction == "LEFT" and not self.direction == "RIGHT" or
            new_direction == "RIGHT" and not self.direction == "LEFT"):
            self.direction = new_direction

class Food:
    def __init__(self):
        self.x, self.y = random.randrange(1, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE, random.randrange(1, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

    def spawn(self):
        self.x, self.y = random.randrange(1, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE, random.randrange(1, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE

    def draw(self):
        pygame.draw.rect(win, FOOD_COLOR, (self.x, self.y, CELL_SIZE, CELL_SIZE))


snake = Snake()
food = Food()
score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    snake.move()
    if snake.body.head.data == (food.x, food.y):
        food.spawn()
        snake.grow()
        score += 1

    # Check for collision with walls or itself
    head_x, head_y = snake.body.head.data
    current_node = snake.body.head.next_node
    collision = False

    while current_node is not None:
        if (head_x, head_y) == current_node.data:
            collision = True
            break
        current_node = current_node.next_node

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or collision:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render("Your Score: " + str(score), True, (255, 255, 255))
        win.fill((0, 0, 0))
        win.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - game_over_text.get_height()))
        win.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 + score_text.get_height()))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before exiting
        pygame.quit()
        quit()

    win.fill((0, 0, 0))  # Clear the screen
    current_node = snake.body.head
    while current_node is not None:
        pygame.draw.rect(win, SNAKE_COLOR, (current_node.data[0], current_node.data[1], CELL_SIZE, CELL_SIZE))
        current_node = current_node.next_node
    food.draw()
    pygame.display.set_caption("Snake Game - Score: " + str(score))  # Display score in the window title
    pygame.display.update()
    clock.tick(5)  # Snake's speed (increase the value for faster movement)
