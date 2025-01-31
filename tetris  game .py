import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes and their colors
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]   # J
]

COLORS = [CYAN, MAGENTA, YELLOW, GREEN, RED, ORANGE, BLUE]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Clock
clock = pygame.time.Clock()

# Grid
grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def create_tetromino():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {
        "shape": shape,
        "color": color,
        "x": GRID_WIDTH // 2 - len(shape[0]) // 2,
        "y": 0
    }

def draw_tetromino(tetromino):
    shape = tetromino["shape"]
    color = tetromino["color"]
    x, y = tetromino["x"], tetromino["y"]
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                pygame.draw.rect(screen, color, ((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_grid():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    for i in range(GRID_HEIGHT):
        pygame.draw.line(screen, WHITE, (0, i * BLOCK_SIZE), (WIDTH, i * BLOCK_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(screen, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, HEIGHT))

def is_collision(tetromino):
    shape = tetromino["shape"]
    x, y = tetromino["x"], tetromino["y"]
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                if x + j < 0 or x + j >= GRID_WIDTH or y + i >= GRID_HEIGHT or grid[y + i][x + j] != BLACK:
                    return True
    return False

def merge_tetromino(tetromino):
    shape = tetromino["shape"]
    x, y = tetromino["x"], tetromino["y"]
    for i in range(len(shape)):
        for j in range(len(shape[i])):
            if shape[i][j]:
                grid[y + i][x + j] = tetromino["color"]

def clear_lines():
    lines_cleared = 0
    for i in range(GRID_HEIGHT - 1, -1, -1):
        if BLACK not in grid[i]:
            lines_cleared += 1
            del grid[i]
            grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return lines_cleared

def game_over():
    font = pygame.font.SysFont("comicsans", 50)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(3000)

# Game variables
current_tetromino = create_tetromino()
fall_time = 0
fall_speed = 0.3
score = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_tetromino["x"] -= 1
                if is_collision(current_tetromino):
                    current_tetromino["x"] += 1
            if event.key == pygame.K_RIGHT:
                current_tetromino["x"] += 1
                if is_collision(current_tetromino):
                    current_tetromino["x"] -= 1
            if event.key == pygame.K_DOWN:
                current_tetromino["y"] += 1
                if is_collision(current_tetromino):
                    current_tetromino["y"] -= 1
            if event.key == pygame.K_UP:
                rotated = list(zip(*reversed(current_tetromino["shape"])))
                if not is_collision({"shape": rotated, "x": current_tetromino["x"], "y": current_tetromino["y"]}):
                    current_tetromino["shape"] = rotated

    # Auto-fall
    if fall_time / 1000 >= fall_speed:
        fall_time = 0
        current_tetromino["y"] += 1
        if is_collision(current_tetromino):
            current_tetromino["y"] -= 1
            merge_tetromino(current_tetromino)
            lines_cleared = clear_lines()
            score += lines_cleared * 100
            current_tetromino = create_tetromino()
            if is_collision(current_tetromino):
                game_over()
                running = False

    # Draw everything
    draw_grid()
    draw_tetromino(current_tetromino)
    pygame.display.update()

# Quit Pygame
pygame.quit()