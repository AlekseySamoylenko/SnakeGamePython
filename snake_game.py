import pygame
from random import choice

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Colors
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

# Generate all possible cell positions
ALL_CELLS = set(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

# Direction mappings
DIRECTION_MAP = {
    (pygame.K_UP, (0, GRID_SIZE)): (0, -GRID_SIZE),
    (pygame.K_UP, (-GRID_SIZE, 0)): (0, -GRID_SIZE),
    (pygame.K_UP, (GRID_SIZE, 0)): (0, -GRID_SIZE),
    (pygame.K_DOWN, (0, -GRID_SIZE)): (0, GRID_SIZE),
    (pygame.K_DOWN, (-GRID_SIZE, 0)): (0, GRID_SIZE),
    (pygame.K_DOWN, (GRID_SIZE, 0)): (0, GRID_SIZE),
    (pygame.K_LEFT, (GRID_SIZE, 0)): (-GRID_SIZE, 0),
    (pygame.K_LEFT, (0, GRID_SIZE)): (-GRID_SIZE, 0),
    (pygame.K_LEFT, (0, -GRID_SIZE)): (-GRID_SIZE, 0),
    (pygame.K_RIGHT, (-GRID_SIZE, 0)): (GRID_SIZE, 0),
    (pygame.K_RIGHT, (0, GRID_SIZE)): (GRID_SIZE, 0),
    (pygame.K_RIGHT, (0, -GRID_SIZE)): (GRID_SIZE, 0),
}

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Изгиб Питона')

# Clock for controlling game speed
clock = pygame.time.Clock()


class GameObject:
    """Base class for all game objects."""

    def __init__(self):
        """Initialize base game object with center position."""
        self.position = CENTER_POSITION
        self.body_color = None

    def draw(self, surface):
        """Abstract method for drawing the object."""
        pass

    def draw_cell(self, surface, position, color):
        """Draw a single cell at the given position with the given color."""
        rect = pygame.Rect(
            position[0],
            position[1],
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, color, rect)


class Apple(GameObject):
    """Class representing the apple in the game."""

    def __init__(self):
        """Initialize apple with red color and random position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """Set random position for the apple avoiding snake's body."""
        available_cells = ALL_CELLS - set(snake_positions)
        self.position = choice(tuple(available_cells))

    def draw(self, surface):
        """Draw the apple on the game surface."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Class representing the snake in the game."""

    def __init__(self):
        """Initialize snake with default attributes."""
        super().__init__()
        self.reset()

    def get_head_position(self):
        """Return the position of snake's head."""
        return self.positions[0]

    def update_direction(self, key):
        """Update snake's direction based on key press."""
        self.direction = DIRECTION_MAP.get(
            (key, self.direction),
            self.direction
        )

    def move(self):
        """Update snake's position based on current direction."""
        head = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head[0] + dx) % SCREEN_WIDTH,
            (head[1] + dy) % SCREEN_HEIGHT
        )

        # Check for collision with self (only if snake is long enough)
        if len(self.positions) > 3 and new_head in self.positions[2:]:
            self.reset()
        else:
            has_length = len(self.positions) > self.length
            self.last = self.positions[-1] if has_length else None
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = (GRID_SIZE, 0)  # Start moving right
        self.last = None
        self.update_score()

    def update_score(self):
        """Update the window caption with current score."""
        caption = f'Изгиб Питона | Длина змейки: {self.length}'
        pygame.display.set_caption(caption)

    def draw(self, surface):
        """Draw the snake on the game surface."""
        # Draw head
        self.draw_cell(surface, self.positions[0], self.body_color)

        # Draw new segments
        if len(self.positions) > 1:
            self.draw_cell(surface, self.positions[1], self.body_color)

        # Clear the last position
        if self.last:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Handle keyboard input for snake direction."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit()
            elif event.key in [
                pygame.K_UP, pygame.K_DOWN,
                pygame.K_LEFT, pygame.K_RIGHT
            ]:
                snake.update_direction(event.key)


def main():
    """Main game loop."""
    snake = Snake()
    apple = Apple()

    while True:
        # Handle input
        handle_keys(snake)

        # Update game state
        snake.move()

        # Check if snake ate the apple
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.update_score()
            apple.randomize_position(snake.positions)

        # Draw everything
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        # Control game speed
        clock.tick(20)


if __name__ == '__main__':
    main() 