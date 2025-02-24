import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Dimensions
WIDTH, HEIGHT = 400, 440  # Increased height for the smiley face
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE - 1, WIDTH // TILE_SIZE
MINE_COUNT = 10

# Font
FONT = pygame.font.SysFont("Arial", 18)
LARGE_FONT = pygame.font.SysFont("Arial", 24)

# Game state
game_over = False
score = 0
mines_left = MINE_COUNT  # New mine counter

# Create the grid and mines
def create_grid():
    grid = [['' for _ in range(COLS)] for _ in range(ROWS)]
    mines = set()
    
    while len(mines) < MINE_COUNT:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        mines.add((x, y))
    
    for y in range(ROWS):
        for x in range(COLS):
            if (x, y) in mines:
                grid[y][x] = 'M'
            else:
                # Count mines around the tile
                count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= x + i < COLS and 0 <= y + j < ROWS:
                            if grid[y + j][x + i] == 'M':
                                count += 1
                grid[y][x] = str(count) if count > 0 else ''
    
    return grid, mines

# Draw the smiley face
def draw_smiley(screen):
    pygame.draw.circle(screen, YELLOW, (WIDTH // 2, 30), 20)  # Smiley face circle
    pygame.draw.circle(screen, BLACK, (WIDTH // 2 - 7, 20), 3)  # Left eye
    pygame.draw.circle(screen, BLACK, (WIDTH // 2 + 7, 20), 3)  # Right eye
    pygame.draw.arc(screen, BLACK, (WIDTH // 2 - 12, 15, 24, 20), 3.14, 0, 2)  # Smile

# Draw the score and mines left counter
def draw_score_and_mines(screen, score, mines_left):
    score_text = LARGE_FONT.render(f"Score: {score}", True, WHITE)
    mines_text = LARGE_FONT.render(f"Mines Left: {mines_left}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(mines_text, (WIDTH - 150, 10))  # Positioned on the right

# Drawing the grid
def draw_grid(screen, grid, revealed, flagged, game_over):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * TILE_SIZE, (y + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Adjusted y position
            
            if game_over and grid[y][x] == 'M' and (x, y) not in revealed:  # Show mines in black when game is over
                pygame.draw.rect(screen, BLACK, rect)  # Mines are black
            elif (x, y) in flagged:
                pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.line(screen, WHITE, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, WHITE, rect.bottomleft, rect.topright, 2)
            elif (x, y) in revealed:
                pygame.draw.rect(screen, WHITE, rect)
                if grid[y][x] != '':
                    text = FONT.render(grid[y][x], True, BLACK)
                    screen.blit(text, (x * TILE_SIZE + TILE_SIZE // 3, (y + 1) * TILE_SIZE + TILE_SIZE // 4))
            else:
                pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

# Game loop
def main():
    global game_over, score, mines_left
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Minesweeper')

    grid, mines = create_grid()
    revealed = set()
    flagged = set()

    while True:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x - WIDTH // 2) ** 2 + (y - 30) ** 2 < 400:  # Check if clicked inside the smiley face
                    # Restart the game if clicked on smiley
                    if game_over:
                        game_over = False
                        score = 0  # Reset score when restarting
                        mines_left = MINE_COUNT  # Reset mine counter
                        grid, mines = create_grid()
                        revealed = set()
                        flagged = set()
                    break

                x, y = (x // TILE_SIZE), (y - 40) // TILE_SIZE  # Adjusted y position for grid
                if 0 <= x < COLS and 0 <= y < ROWS:  # Clicked within bounds
                    if event.button == 1:  # Left click
                        if grid[y][x] == 'M':
                            game_over = True  # Hit a mine
                        else:
                            revealed.add((x, y))
                            score += 1  # Increase score for a successful reveal
                    elif event.button == 3:  # Right click (Flagging)
                        if (x, y) in flagged:
                            flagged.remove((x, y))
                            mines_left += 1  # Increase mine count when unflagging
                        else:
                            flagged.add((x, y))
                            mines_left -= 1  # Decrease mine count when flagging

        draw_smiley(screen)  # Draw the smiley face at the top
        draw_score_and_mines(screen, score, mines_left)  # Draw score and mine counter
        draw_grid(screen, grid, revealed, flagged, game_over)

        if game_over:
            game_over_text = FONT.render('Game Over! Click the smiley to restart.', True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 120, HEIGHT // 2))
        
        pygame.display.flip()

# Run the game
if __name__ == '__main__':
    main()
