from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, position: tuple[int] = CENTER) -> None:
        """Инициализация базовых атрибутов игрового объекта."""
        self.position: tuple[int] = position
        self.body_color: tuple[int] = None

    def draw(self) -> None:
        """Абстрактный метод для переопределения в наследниках."""
        pass


class Apple(GameObject):
    """Класс яблока для игры 'Змейка'."""

    def __init__(self, color: tuple[int] = APPLE_COLOR) -> None:
        """Инициализация игрового объекта 'Яблоко'."""
        super().__init__()
        self.body_color: tuple[int] = color
        self.randomize_position()

    def randomize_position(self) -> None:
        """Метод устанавливает случайные координаты яблока на поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self) -> None:
        """Метод отрисовки яблока на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_position(self) -> tuple[int]:
        """Метод get для получения текущей позиции яблока."""
        return self.position


class Snake(GameObject):
    """Класс змейки для игры 'Змейка'."""

    def __init__(self, color: tuple[int] = SNAKE_COLOR) -> None:
        """Инициализация игрового объекта 'Змейка'."""
        super().__init__()
        self.length: int = 1
        self.positions: list[tuple[int]] = [self.position]
        self.direction: tuple[int] = RIGHT
        self.next_direction: tuple[int] = None
        self.body_color: tuple[int] = color
        self.last = None

    def update_direction(self) -> None:
        """Метод обновления направления движения змейки по нажатию клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод обновления позиции змейки на игровом поле."""
        head_x, head_y = self.get_head_position()

        new_head = (
            (head_x + GRID_SIZE * self.direction[0]),
            (head_y + GRID_SIZE * self.direction[1]),
        )

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

        if len(self.positions) > 4 and self.positions[0] in self.positions[1:]:
            self.reset()

    def draw(self) -> None:
        """Метод отрисовки змейки с затиранием следа."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int]:
        """Метод, возвращающий позицию головы змейки на игровом поле."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сброса состояния змейки после столкновения с собой."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        self.next_direction = None

    def eat(self, apple: Apple) -> None:
        """Метод увеличения длины змейки после того, как она съела яблоко."""
        self.positions.insert(0, apple.get_position())

        if self.length == 1:
            self.positions.insert(1, self.get_head_position())

        self.length += 1


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя - нажатий на клавиши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция работы игры 'Змейка'."""
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.get_position():
            snake.eat(apple)
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
