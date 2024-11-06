import pygame
import random


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        """Инициализирует объект на экране."""
        self.position = position

    def draw(self, surface):
        """Отрисовка объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для описания яблока в игре."""

    def __init__(self, grid_size):
        """Инициализирует объект яблока и его позицию."""
        self.body_color = (255, 0, 0)  # Красный цвет
        self.grid_size = grid_size
        self.randomize_position()

    def randomize_position(self):
        """Задаёт яблоку случайную позицию на игровом поле."""
        self.position = (
            random.randint(0, 31) * self.grid_size,
            random.randint(0, 23) * self.grid_size
        )

    def draw(self, surface):
        """Отрисовывает яблоко на экране."""
        pygame.draw.rect(
            surface,
            self.body_color,
            pygame.Rect(self.position, (self.grid_size, self.grid_size))
        )


class Snake(GameObject):
    """Класс для описания змейки в игре."""

    def __init__(self, grid_size):
        """Инициализирует начальные параметры змейки."""
        self.body_color = (0, 255, 0)  # Зелёный цвет
        self.grid_size = grid_size
        self.length = 1
        self.positions = [(grid_size * 16, grid_size * 12)]
        self.direction = (1, 0)  # По умолчанию движение вправо

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def move(self):
        """Двигает змейку по игровому полю."""
        head_x, head_y = self.positions[0]
        new_position = (
            head_x + self.direction[0] * self.grid_size,
            head_y + self.direction[1] * self.grid_size
        )

        self.positions = [new_position] + self.positions

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки."""
        self.length += 1

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                pygame.Rect(position, (self.grid_size, self.grid_size))
            )

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает параметры змейки."""
        self.length = 1
        self.positions = [(self.grid_size * 16, self.grid_size * 12)]
        self.direction = (1, 0)


def handle_input(snake):
    """Обрабатывает ввод пользователя для управления змейкой."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction((0, -1))
    if keys[pygame.K_DOWN]:
        snake.update_direction((0, 1))
    if keys[pygame.K_LEFT]:
        snake.update_direction((-1, 0))
    if keys[pygame.K_RIGHT]:
        snake.update_direction((1, 0))


def check_collisions(snake, apple, screen_width, screen_height):
    """Проверяет столкновения змейки с яблоком, границами и самой собой."""
    if snake.get_head_position() == apple.position:
        snake.grow()
        apple.randomize_position()

    if snake.get_head_position() in snake.positions[1:]:
        snake.reset()

    head_x, head_y = snake.get_head_position()
    if (head_x < 0 or head_x >= screen_width
            or head_y < 0 or head_y >= screen_height):
        snake.reset()


def main():
    """Главная функция для запуска игры."""
    pygame.init()

    grid_size = 20
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(
        'Snake Game'
    )  # Исправлено на две строки для PEP8
    clock = pygame.time.Clock()

    snake = Snake(grid_size)
    apple = Apple(grid_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_input(snake)
        snake.move()
        check_collisions(snake, apple, screen_width, screen_height)

        screen.fill((0, 0, 0))
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()

        clock.tick(10)

    pygame.quit()


if __name__ == '__main__':
    main()
