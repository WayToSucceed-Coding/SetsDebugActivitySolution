import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Match Game")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW=(255,255,0)

# Define fonts
font = pygame.font.SysFont("Arial", 30)
win_font = pygame.font.SysFont("Arial", 40, bold=True)
title_font = pygame.font.SysFont("Arial", 50, bold=True)  # For the game title

# Create shuffled cards (numbers as placeholders)
cards = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
random.shuffle(cards)

# Set up card grid
card_width = 100
card_height = 100
num_rows = 3
num_cols = 4
attempts_limit = 12  # Limit the number of attempts

# Game state
flipped_cards = []
matched_pairs = set()#Debug 1
attempts = 0
game_won = False

# Function to draw the cards
def draw_cards():
    # Calculate starting position to center the grid
    padding = 5
    total_width = (card_width + padding) * num_cols - padding
    total_height = (card_height + padding) * num_rows - padding
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2 

    for i in range(num_rows):
        for j in range(num_cols):
            card_index = i * num_cols + j
            x = start_x + j * (card_width + padding)
            y = start_y + i * (card_height + padding)
            if card_index in flipped_cards or card_index in matched_pairs:
                # Show the card's number
                pygame.draw.rect(screen, BLUE, (x, y, card_width, card_height))
                draw_text(str(cards[card_index]), WHITE, x + 35, y + 35)
            else:
                # Hide the card (draw as a red rectangle)
                pygame.draw.rect(screen, YELLOW, (x, y, card_width, card_height))

# Draw text on the screen
def draw_text(text, color, x, y, font=font):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Draw the title at the top of the screen
def draw_title():
    title = "Memory Match Game"
    draw_text(title, BLUE, WIDTH // 2 - title_font.size(title)[0] // 2, 10, title_font)

   
# Main game loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw the game title
    draw_title()
    
    # Draw all cards (centered)
    draw_cards()

    # Check for win condition
    if len(matched_pairs) == len(cards):
        game_won = True
        draw_text("You Win!", GREEN, WIDTH // 2 - 60, HEIGHT // 2 - 30, win_font)
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_won:
            # Get the card clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate the position of the clicked card relative to the centered grid
            padding = 5
            total_width = (card_width + padding) * num_cols - padding
            total_height = (card_height + padding) * num_rows - padding
            start_x = (WIDTH - total_width) // 2
            start_y = (HEIGHT - total_height) // 2

            clicked_row = (mouse_y - start_y) // (card_height + padding)
            clicked_col = (mouse_x - start_x) // (card_width + padding)
            clicked_card_index = clicked_row * num_cols + clicked_col
            
            if clicked_card_index not in flipped_cards and clicked_card_index not in matched_pairs:
                flipped_cards.append(clicked_card_index)
                
                # Check if two cards are flipped, and if they match
                if len(flipped_cards) == 2:
                    attempts += 1  # Increase the attempts count
                    card1, card2 = flipped_cards
                    
                    if cards[card1] == cards[card2]:

                        # They match, add to matched pairs
                        matched_pairs.add(card1)#Debug 2
                        matched_pairs.add(card2)#Debug 2
                    # Whether matched or not, clear flipped cards immediately
                    flipped_cards.clear()
    
    # Display score and attempts left
    draw_text(f"Matched pairs: {len(matched_pairs) // 2}", BLACK, 20, HEIGHT - 70)
    draw_text(f"Attempts left: {attempts_limit - attempts}", BLACK, 20, HEIGHT - 40)
    
    # Check for losing condition
    if attempts >= attempts_limit and not game_won and len(matched_pairs) != len(cards):
        draw_text("Game Over! Out of attempts.", RED, WIDTH // 2 - 200, HEIGHT // 2 - 30, win_font)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False  # End the game
    
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()
