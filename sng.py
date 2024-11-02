import pygame
import random

# Определение констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # черный

# Определение направлений
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовка объекта на экране."""
        pygame.draw.rect(surface, self.body_color,
                         pygame.Rect(self.position[0],
                                     self.position[1],
                                     GRID_SIZE, GRID_SIZE))


class Apple(GameObject):
    """Класс яблока, наследуемый от GameObject."""

    def __init__(self, position=(0, 0), body_color=(255, 0, 0),
                 grid_size=GRID_SIZE):
        """Инициализация яблока с заданной позицией и цветом."""
        super().__init__(position, body_color)
        self.grid_size = grid_size

    def randomize_position(self):
        """Рандомизация позиции яблока на экране."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * self.grid_size,
            random.randint(0, GRID_HEIGHT - 1) * self.grid_size
        )


class Snake(GameObject):
    """Класс змейки, наследуемый от GameObject."""

    def __init__(self, position=(0, 0), body_color=(0, 255, 0),
                 grid_size=GRID_SIZE):
        """Инициализация змейки с заданной позицией и цветом."""
        super().__init__(position, body_color)
        self.positions = [position]
        self.direction = RIGHT
        self.grid_size = grid_size

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку в текущем направлении."""
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x * self.grid_size)) % SCREEN_WIDTH,
               (cur[1] + (y * self.grid_size)) % SCREEN_HEIGHT)
        if new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > 1:
                self.positions.pop()

    def reset(self):
        """Сбрасывает состояние змейки при столкновении."""
        self.positions = [self.position]
        self.direction = RIGHT

    def update_direction(self, new_direction):
        """Обновляет направление змейки, если оно не противоположно текущему."""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction


# Функция обработки клавиш
def handle_keys(snake):
    """Обрабатывает нажатия клавиш управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


# Основная игровая функция
def main():
    """Основная функция игры."""
    global screen, clock
    snake = Snake(position=(100, 100))
    apple = Apple()
    apple.randomize_position()

    while True:
        handle_keys(snake)
        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.flip()

        clock.tick(10)


if __name__ == '__main__':
    main()
