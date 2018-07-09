"""
 Sample Breakout Game
 
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Modified Version using Fuzzy Controller (With acceleration)
"""
 
# --- Import libraries used for this program
 
import math
import pygame
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
 
# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
 
# Size of break-out blocks
block_width = 23
block_height = 15
 
 
class Block(pygame.sprite.Sprite):
  """This class represents each block that will get knocked out by the ball
  It derives from the "Sprite" class in Pygame """

  def __init__(self, color, x, y):
    """ Constructor. Pass in the color of the block,
        and its x and y position. """

    # Call the parent class (Sprite) constructor
    super(Block, self).__init__()

    # Create the image of the block of appropriate size
    # The width and height are sent as a list for the first parameter.
    self.image = pygame.Surface([block_width, block_height])

    # Fill the image with the appropriate color
    self.image.fill(color)

    # Fetch the rectangle object that has the dimensions of the image
    self.rect = self.image.get_rect()

    # Move the top left of the rectangle to x,y.
    # This is where our block will appear..
    self.rect.x = x
    self.rect.y = y
 
 
class Ball(pygame.sprite.Sprite):
  """ This class represents the ball
      It derives from the "Sprite" class in Pygame """

  # Speed in pixels per cycle
  speed = 10.0
  acceleration = 0.005

  # Floating point representation of where the ball is
  x = 0.0
  y = 180.0

  # Direction of ball (in degrees)
  direction = 200

  width = 10
  height = 10

  # Constructor. Pass in the color of the block, and its x and y position
  def __init__(self):
    # Call the parent class (Sprite) constructor
    super(Ball, self).__init__()

    # Create the image of the ball
    self.image = pygame.Surface([self.width, self.height])

    # Color the ball
    self.image.fill(white)

    # Get a rectangle object that shows where our image is
    self.rect = self.image.get_rect()

    # Get attributes for the height/width of the screen
    self.screenheight = pygame.display.get_surface().get_height()
    self.screenwidth = pygame.display.get_surface().get_width()

  def bounce(self, diff):
    """ This function will bounce the ball
        off a horizontal surface (not a vertical one) """

    self.direction = (180 - self.direction) % 360
    self.direction -= diff

  def update(self):
    """ Update the position of the ball. """
    # Sine and Cosine work in degrees, so we have to convert them
    self.speed = min(25.0, self.speed + self.acceleration)
    direction_radians = math.radians(self.direction)

    # Change the position (x and y) according to the speed and direction
    self.x += self.speed * math.sin(direction_radians)
    self.y -= self.speed * math.cos(direction_radians)

    # Move the image to where our x and y are
    self.rect.x = self.x
    self.rect.y = self.y

    # Do we bounce off the top of the screen?
    if self.y <= 0:
      self.bounce(0)
      self.y = 1

    # Do we bounce off the left of the screen?
    if self.x <= 0:
      self.direction = (360 - self.direction) % 360
      self.x = 1

    # Do we bounce of the right side of the screen?
    if self.x > self.screenwidth - self.width:
      self.direction = (360 - self.direction) % 360
      self.x = self.screenwidth - self.width - 1

    # Did we fall off the bottom edge of the screen?
    if self.y > 600:
      return True
    else:
      return False
 
 
class Player(pygame.sprite.Sprite):
  """ This class represents the bar at the bottom that the
  player controls. """

  def __init__(self):
    """ Constructor for Player. """
    # Call the parent's constructor
    super(Player, self).__init__()

    self.width = 75
    self.height = 15
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill((white))

    # Make our top-left corner the passed-in location.
    self.rect = self.image.get_rect()
    self.screenheight = pygame.display.get_surface().get_height()
    self.screenwidth = pygame.display.get_surface().get_width()

    self.rect.x = 0
    self.rect.y = self.screenheight-self.height

  def update(self, vel):
    """ Update the player position. """
    # Set the left side of the player bar to the ball position
    #self.rect.x = pos - self.width / 2
    self.rect.x = self.rect.x + vel
    # Make sure we don't push the player paddle
    # off the right side of the screen
    if self.rect.x > self.screenwidth - self.width:
      self.rect.x = self.screenwidth - self.width

    if self.rect.x < 0:
      self.rect.x = 0


def calculate_membership(position_x=0, position_y=200, plot=False):
  # We need the activation of our fuzzy membership functions at these values;
  # position_x and position_y
  distance_level_near = fuzz.interp_membership(distance, distance_near, position_y)
  distance_level_mid  = fuzz.interp_membership(distance, distance_mid, position_y)
  distance_level_far  = fuzz.interp_membership(distance, distance_far, position_y)

  position_level_left   = fuzz.interp_membership(position, position_left, position_x)
  position_level_center = fuzz.interp_membership(position, position_center, position_x)
  position_level_right  = fuzz.interp_membership(position, position_right, position_x)

  # Now we take our rules and apply them. Rule 1 concerns middle way AND on the left.
  # The AND operator means we take the minimum of these two.
  active_rule1 = np.fmin(distance_level_mid, position_level_left)

  # As a result of Rule #1: move FAST to LEFT
  moving_s_activation_left_fast = np.fmin(active_rule1, moving_s_left_fast)

  # Now we take our rules and apply them. Rule 2 concerns near AND on the left.
  # The AND operator means we take the minimum of these two.
  active_rule2 = np.fmin(distance_level_near, position_level_left)

  # As a result of Rule #2: move SLOW to LEFT
  moving_s_activation_left_slow = np.fmin(active_rule2, moving_s_left_slow)

  # Now we take our rules and apply them. Rule 3 concerns far OR on the center.
  # The OR operator means we take the maximum of these two.
  active_rule3 = np.fmax(distance_level_far, position_level_center)

  # As a result of Rule #3: no move
  moving_s_activation_no_move = np.fmin(active_rule3, moving_s_no_move)

  # Now we take our rules and apply them. Rule 4 concerns near AND on the right.
  # The AND operator means we take the minimum of these two.
  active_rule4 = np.fmin(distance_level_near, position_level_right)

  # As a result of Rule #4: move SLOW to RIGHT
  moving_s_activation_right_slow = np.fmin(active_rule4, moving_s_right_slow)

  # Now we take our rules and apply them. Rule 5 concerns middle way AND on the right.
  # The AND operator means we take the minimum of these two.
  active_rule5 = np.fmin(distance_level_mid, position_level_right)

  # As a result of Rule #5: move FAST to RIGHT
  moving_s_activation_right_fast = np.fmin(active_rule5, moving_s_right_fast)

  union_left = np.fmax(moving_s_activation_left_fast, moving_s_activation_left_slow)
  union_right = np.fmax(moving_s_activation_right_fast, moving_s_activation_right_slow)
  union_sides = np.fmax(union_left, union_right)
  union = np.fmax(moving_s_no_move, union_sides)

  # Calculate defuzzified result
  velocity = fuzz.defuzz(moving_s, union, 'centroid')
  moving_s_activation = fuzz.interp_membership(moving_s, union, velocity)

  if plot:
    moving_s0 = np.zeros_like(moving_s)

    # Visualize this
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.fill_between(moving_s, moving_s0, moving_s_activation_left_fast, facecolor='b', alpha=0.7)
    ax0.plot(moving_s, moving_s_left_fast, 'b', linewidth=0.5, linestyle='--', label='Fast to left')
    ax0.fill_between(moving_s, moving_s0, moving_s_activation_left_slow, facecolor='g', alpha=0.7)
    ax0.plot(moving_s, moving_s_left_slow, 'g', linewidth=0.5, linestyle='--', label='Slow to left')
    ax0.fill_between(moving_s, moving_s0, moving_s_activation_no_move, facecolor='r', alpha=0.7)
    ax0.plot(moving_s, moving_s_no_move, 'r', linewidth=0.5, linestyle='--', label='No move')
    ax0.fill_between(moving_s, moving_s0, moving_s_activation_right_slow, facecolor='y', alpha=0.7)
    ax0.plot(moving_s, moving_s_right_slow, 'y', linewidth=0.5, linestyle='--', label='Slow to right')
    ax0.fill_between(moving_s, moving_s0, moving_s_activation_right_fast, facecolor='m', alpha=0.7)
    ax0.plot(moving_s, moving_s_right_fast, 'm', linewidth=0.5, linestyle='--', label='Fast to right')
    ax0.set_title('Output membership activity')
    ax0.legend()

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    # Visualize this
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.plot(moving_s, moving_s_left_fast, 'b', linewidth=0.5, linestyle='--')
    ax0.plot(moving_s, moving_s_left_slow, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(moving_s, moving_s_no_move, 'r', linewidth=0.5, linestyle='--')
    ax0.plot(moving_s, moving_s_right_slow, 'y', linewidth=0.5, linestyle='--')
    ax0.plot(moving_s, moving_s_right_fast, 'm', linewidth=0.5, linestyle='--')
    ax0.fill_between(moving_s, moving_s0, union, facecolor='Orange', alpha=0.7)
    ax0.plot([velocity, velocity], [0, moving_s_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Aggregated membership and defuzzifying (line)')

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.show()

  return velocity

 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])
 
# Set the title of the window
pygame.display.set_caption('Breakout')
 
# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)
 
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
 
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
 
# Create sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
 
# Create the player paddle object
player = Player()
allsprites.add(player)
 
# Create the ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)
 
# The top of the block (y position)
top = 80
 
# Number of blocks to create
blockcount = 32
 
# --- Create blocks
 
# Five rows of blocks
for row in range(5):
  # 32 columns of blocks
  for column in range(0, blockcount):
    # Create a block (color,x,y)
    block = Block(blue, column * (block_width + 2) + 1, top)
    blocks.add(block)
    allsprites.add(block)
  # Move the top of the next row down
  top += block_height + 2
 
# Clock to limit speed
clock = pygame.time.Clock()
 
# Is the game over?
game_over = False
 
# Exit the program?
exit_program = False


# Generate universe variables
#   * Distance and position on ranges [0, 600] and [-800, 800]
#   * Player velocity has a range of [-120, 120]
distance = np.arange(0, 601, 1)
position = np.arange(-800, 801, 1)
moving_s = np.arange(-120, 121, 1)

# Generate fuzzy membership functions
distance_near = fuzz.trimf(distance, [0, 0, 50])
distance_mid  = fuzz.trimf(distance, [0, 200, 400])
distance_far  = fuzz.trimf(distance, [300, 600, 600])
position_left   = fuzz.trimf(position, [-800, -800, 0])
position_center = fuzz.trimf(position, [-50, 0, 50])
position_right  = fuzz.trimf(position, [0, 800, 800])
moving_s_left_fast  = fuzz.trimf(moving_s, [-120, -120, -40])
moving_s_left_slow  = fuzz.trimf(moving_s, [-80, -40, 0])
moving_s_no_move    = fuzz.trimf(moving_s, [-20, 0 , 20])
moving_s_right_slow = fuzz.trimf(moving_s, [0, 40, 80])
moving_s_right_fast = fuzz.trimf(moving_s, [40, 120, 120])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(distance, distance_near, 'b', linewidth=1.5, label='Near')
ax0.plot(distance, distance_mid, 'g', linewidth=1.5, label='Mid')
ax0.plot(distance, distance_far, 'r', linewidth=1.5, label='Far')
ax0.set_title('Y-Position of the ball compared to the player')
ax0.legend()

ax1.plot(position, position_left, 'b', linewidth=1.5, label='Left')
ax1.plot(position, position_center, 'g', linewidth=1.5, label='Center')
ax1.plot(position, position_right, 'r', linewidth=1.5, label='Right')
ax1.set_title('X-Position of the ball compared to the player')
ax1.legend()

ax2.plot(moving_s, moving_s_left_fast, 'b', linewidth=1.5, label='Fast to left')
ax2.plot(moving_s, moving_s_left_slow, 'g', linewidth=1.5, label='Slow to left')
ax2.plot(moving_s, moving_s_no_move, 'r', linewidth=1.5, label='No move')
ax2.plot(moving_s, moving_s_right_slow, 'y', linewidth=1.5, label='Slow to right')
ax2.plot(moving_s, moving_s_right_fast, 'm', linewidth=1.5, label='Fast to right')
ax2.set_title('Player moving behaviour')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

plt.show()

# Main program loop
while not exit_program:
  # Limit to 30 fps
  clock.tick(30)

  # Clear the screen
  screen.fill(black)

  # Process the events in the game
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit_program = True

  # Update the ball and player position as long
  # as the game is not over.
  if not game_over:
    text = font.render("Speed = %.2f" % ball.speed, True, white)
    textpos = text.get_rect(centerx=background.get_width()-100)
    textpos.top = 20
    screen.blit(text, textpos)
    # Update the player and ball positions
    game_over = ball.update()
    
    vel = calculate_membership(ball.x - player.rect.x - player.width / 2, np.abs(player.rect.y - ball.y))
    player.update(vel)
    #player.update(ball.x)

  # If we are done, print game over
  if game_over:
    text = font.render("Game Over", True, white)
    textpos = text.get_rect(centerx=background.get_width()/2)
    textpos.top = 300
    screen.blit(text, textpos)

  # See if the ball hits the player paddle
  if pygame.sprite.spritecollide(player, balls, False):
    # The 'diff' lets you try to bounce the ball left or right
    # depending where on the paddle you hit it
    diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)

    # Set the ball's y position in case
    # we hit the ball on the edge of the paddle
    ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
    ball.bounce(0)

  # Check for collisions between the ball and the blocks
  deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

  # If we actually hit a block, bounce the ball
  if len(deadblocks) > 0:
    ball.bounce(0)

    # Game ends if all the blocks are gone
    if len(blocks) == 0:
      game_over = True

  # Draw Everything
  allsprites.draw(screen)

  # Flip the screen and show what we've drawn
  pygame.display.flip()
 
pygame.quit()










