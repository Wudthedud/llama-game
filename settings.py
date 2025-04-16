# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83) # Color matching Chrome Dino game text

# Player settings
GRAVITY = 0.8
JUMP_POWER = -15
PLAYER_START_X = 50
PLAYER_GROUND_Y = SCREEN_HEIGHT - 70 # Adjust based on ground/llama sprite height
PLAYER_DUCK_Y = SCREEN_HEIGHT - 40  # Adjust for ducking sprite height

# Game speed settings
INITIAL_SPEED = 6
SPEED_INCREASE_RATE = 0.001 # How much speed increases per frame/tick
MAX_SPEED = 20

# Ground settings
GROUND_Y = SCREEN_HEIGHT - 50 # Top of the ground image

# Obstacle settings
OBSTACLE_MIN_GAP = 250  # Minimum pixels between obstacles
OBSTACLE_MAX_GAP = 600  # Maximum pixels between obstacles
BIRD_ALTITUDE_LOW = PLAYER_GROUND_Y - 30  # Y pos for low bird
BIRD_ALTITUDE_HIGH = PLAYER_GROUND_Y - 70 # Y pos for high bird (needs ducking)

# File Paths
FONT_NAME = 'assets/fonts/pixel_font.ttf' # Example path
HIGH_SCORE_FILE = 'high_score.txt'
# ... add paths for all image assets ...
LLAMA_RUN_IMGS = ['assets/images/llama/run1.png', 'assets/images/llama/run2.png']
LLAMA_JUMP_IMG = 'assets/images/llama/jump.png'
LLAMA_DUCK_IMGS = ['assets/images/llama/duck1.png', 'assets/images/llama/duck2.png']
LLAMA_CRASH_IMG = 'assets/images/llama/crash.png'
CACTUS_SMALL_IMGS = ['assets/images/obstacles/cactus_small1.png', ...]
CACTUS_LARGE_IMGS = ['assets/images/obstacles/cactus_large1.png', ...]
BIRD_IMGS = ['assets/images/obstacles/bird1.png', 'assets/images/obstacles/bird2.png']
GROUND_IMG = 'assets/images/environment/ground.png'
CLOUD_IMG = 'assets/images/environment/cloud.png'

# Sound Paths (Optional)
JUMP_SOUND = 'assets/sounds/jump.wav'
SCORE_SOUND = 'assets/sounds/score_tick.wav'
GAMEOVER_SOUND = 'assets/sounds/game_over.wav'

# Custom Events (Optional, for timed actions like cloud spawning)
ADD_CLOUD_EVENT = pygame.USEREVENT + 1