
import pygame
import random

# Initialize pygame library for game development
pygame.init()

# Game Window Dimensions
WIDTH, HEIGHT = 300, 600  # Set width and height of the game screen
CELL_SIZE = 30  # Define the size of each grid cell
COLUMNS = WIDTH // CELL_SIZE  # Calculate number of columns
ROWS = HEIGHT // CELL_SIZE  # Calculate number of rows
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game window
pygame.display.set_caption("Tetris - Block Twist")  # Set window title

# Colors for Blocks and Grid
BLACK = (0, 0, 0)  # Background color
WHITE = (255, 255, 255)  # Grid color
YELLOW = (255, 255, 0)  # Score text color
           #red         #green        #blue        #orange         #purple              
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 165, 0), (128, 0, 128)]  # Block colors

# Define Shapes (Square, L, Reverse L, Single Line)
SHAPES = [
    [[1, 1], [1, 1]],  # Square shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # Reverse L shape (Ulta L)
    [[1, 1, 1, 1]]  # Single line shape
]

# Initialize Game Grid
grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]  # Empty grid
score = 0  # Initialize player score
game_over = False  # Game over flag

# Block Class to Handle Blocks
class Block:
    def __init__(self):
        self.shape = random.choice(SHAPES)  # Randomly select a shape
        self.color = random.choice(COLORS)  # Assign a random color
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2  # Set initial x position
        self.y = 0  # Set initial y position

    # Draw the block on the screen
    def draw(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:  # Check if block cell is filled
                    rect = pygame.Rect((self.x + col) * CELL_SIZE, (self.y + row) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, self.color, rect)  # Draw block

    # Move the block in x or y direction
    def move(self, dx, dy):
        if not self.collision(dx, dy):  # Check for collision
            self.x += dx  # Move in x-direction
            self.y += dy  # Move in y-direction
        else:
            if dy > 0:  # If collision while moving down
                self.lock()  # Lock the block in place
                check_lines()  # Check for full rows
                new_block()  # Generate a new block

    # Rotate the block
    def rotate(self):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]  # Rotate using matrix transpose
        if not self.collision(0, 0, rotated_shape):  # Check if rotation is possible
            self.shape = rotated_shape  # Apply rotation

    # Check for collision with other blocks or boundaries
    def collision(self, dx, dy, shape=None):
        if shape is None:
            shape = self.shape
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if shape[row][col]:  # If cell is occupied
                    new_x = self.x + col + dx
                    new_y = self.y + row + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                        return True  # Collision with boundary
                    if new_y >= 0 and grid[new_y][new_x] is not None:
                        return True  # Collision with existing block
        return False  # No collision

    # Lock block into grid
    def lock(self):
        global game_over
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    grid[self.y + row][self.x + col] = self.color  # Store block color in grid
        if self.y == 0:
            game_over = True  # Game over if block locks at top

# Create New Block
def new_block():
    global block
    block = Block()  # Generate a new block

# Check for Completed Lines and Clear Them
def check_lines():
    global grid, score
    full_rows = [row for row in range(ROWS) if all(grid[row])]  # Find full rows
    if full_rows:
        for row in full_rows:
            grid.pop(row)  # Remove completed row
            grid.insert(0, [None for _ in range(COLUMNS)])  # Add new empty row at top
        score += len(full_rows) * 10  # Increase score

# Draw Grid on Screen
def draw_grid():
    for row in range(ROWS):
        for col in range(COLUMNS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid lines
            if grid[row][col]:
                pygame.draw.rect(screen, grid[row][col], rect)  # Draw occupied blocks

# Draw Score on Screen
def draw_score():
    font = pygame.font.Font(None, 50)
    text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(text, (WIDTH // 2 - 70, 20))  # Display score

# Draw Game Over Screen
def draw_game_over():
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, (255, 0, 0))
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart", True, WHITE)
    screen.blit(text, (WIDTH // 4, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 6, HEIGHT // 2))

# Initialize First Block
block = Block()
running = True  # Game running flag
clock = pygame.time.Clock()  # Game clock

# Game Loop
while running:
    screen.fill(BLACK)  # Clear screen

    if game_over:
        draw_game_over()  # Show game over screen
    else:
        draw_grid()  # Draw game grid
        draw_score()  # Display score
        block.draw()  # Draw current block

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    block.move(-1, 0)  # Move left
                if event.key == pygame.K_RIGHT:
                    block.move(1, 0)  # Move right
                if event.key == pygame.K_DOWN:
                    block.move(0, 1)  # Move down
                if event.key == pygame.K_UP:
                    block.rotate()  # Rotate block
            if event.key == pygame.K_r:
                game_over = False  # Restart game
                grid = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
                score = 0
                new_block()

    if not game_over:
        block.move(0, 1)  # Auto move block down

    pygame.display.update()  # Update display
    clock.tick(4)  # Set game speed

pygame.quit()  # Quit game
