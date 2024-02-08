import pygame, sys, random, math

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, color, name):
        super(Square, self).__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.name = name
        self.successful_pick = False

    def move(self, deltax, deltay):
        if self.rect.left < 0 or self.rect.right > 1200:
            deltax *= -1
        if self.rect.top < 0 or self.rect.bottom > 600:
            deltay *= -1

        self.rect.centerx += deltax
        self.rect.centery += deltay

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super(Goal, self).__init__()
        self.image = pygame.Surface((100, 50), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Agario")

# Set up font for displaying messages
font = pygame.font.Font(None, 36)

# Create clock to later control frame rate
clock = pygame.time.Clock()

# Function to shuffle and assign goals to squares
def shuffle_and_assign_goals(squares, goal_group):
    goals = list(goal_group)
    random.shuffle(goals)

    for i, square in enumerate(squares):
        square.correct_goal = goals[i]
        square.successful_pick = False

blue_square = Square(800, 300, "light blue", "Blue Square")
pink_square = Square(400, 300, "pink", "Pink Square")

squares = pygame.sprite.Group()
squares.add(blue_square)
squares.add(pink_square)

goal1 = Goal(100, 100, "light blue")
goal2 = Goal(100, 200, "light blue")
goal3 = Goal(100, 300, "light blue")
goal4 = Goal(100, 400, "light blue")
goal5 = Goal(100, 500, "light blue")
goal6 = Goal(1130, 100, "pink")
goal7 = Goal(1130, 200, "pink")
goal8 = Goal(1130, 300, "pink")
goal9 = Goal(1130, 400, "pink")
goal10 = Goal(1130, 500, "pink")

goal_group = pygame.sprite.Group()
goal_group.add(goal1, goal2, goal3, goal4, goal5, goal6, goal7, goal8, goal9, goal10)


first_pick_blue_square = None
first_pick_pink_square = None

# Shuffle and assign initial goals
shuffle_and_assign_goals(squares, goal_group)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        blue_square.move(-2, 0)
    if keys[pygame.K_RIGHT]:
        blue_square.move(2, 0)
    if keys[pygame.K_UP]:
        blue_square.move(0, -2)
    if keys[pygame.K_DOWN]:
        blue_square.move(0, 2)

    if keys[pygame.K_a]:
        pink_square.move(-2, 0)
    if keys[pygame.K_d]:
        pink_square.move(2, 0)
    if keys[pygame.K_w]:
        pink_square.move(0, -2)
    if keys[pygame.K_s]:
        pink_square.move(0, 2)

    #Collisons w goals
    for square in squares:
        if not square.successful_pick:
            collided_goals = pygame.sprite.spritecollide(square, goal_group, False)
            for goal in collided_goals:
                # Check if the square is colliding with the correct goal
                if square.color == goal.color and square.correct_goal == goal:
                    # Record the first successful pick for each square
                    if square.name == "Blue Square" and first_pick_blue_square is None:
                        first_pick_blue_square = square.name
                    elif square.name == "Pink Square" and first_pick_pink_square is None:
                        first_pick_pink_square = square.name

                    square.successful_pick = True
    # Display messages on the screen
    if first_pick_blue_square:
        message_blue = font.render(f"{first_pick_blue_square} picked the right goal first! Game over.", True, (255, 255, 255))
        screen.blit(message_blue, ((screen_width - message_blue.get_width()) // 2, (screen_height - message_blue.get_height()) // 2))

    if first_pick_pink_square:
        message_pink = font.render(f"{first_pick_pink_square} picked the right goal first! Game over.", True, (255, 255, 255))
        screen.blit(message_pink, ((screen_width - message_pink.get_width()) // 2, (screen_height - message_pink.get_height()) // 2))

    squares.draw(screen)
    goal_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()