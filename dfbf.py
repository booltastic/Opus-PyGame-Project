import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Text with Black Border")

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load font
font = pygame.font.Font(None, 36)

# Text content
text_content = "Hello, World!"

# Render text with black border
border_text = font.render(text_content, True, BLACK)
border_rect = border_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# Render actual text
actual_text = font.render(text_content, True, WHITE)
actual_rect = actual_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Blit the text with black border
    screen.blit(border_text, border_rect)

    # Blit the actual text on top
    screen.blit(actual_text, actual_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
