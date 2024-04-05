from pygame import font
font.init()

ROW, COL = 15, 5
SIDEBAR_SIZE = 3
GRID_SIZE = 64
WIDTH, HEIGHT = (ROW + SIDEBAR_SIZE) * GRID_SIZE, COL * GRID_SIZE
FPS = 60
TITLE = "Tower Defense"
TEXT_SIZE = 30
FONT = font.SysFont("",TEXT_SIZE)
SCROLL_SPEED = 10

#Buttons
BUTTON_OFFSET = 5
BUTTON_WIDTH, BUTTON_HEIGHT = (SIDEBAR_SIZE * GRID_SIZE) - 2 * BUTTON_OFFSET, 50
BUTTON_IMAGE_OFFSET = 3
BUTTON_IMAGE_SIZE = BUTTON_HEIGHT - BUTTON_IMAGE_OFFSET

BUTTON_COLOR = (70,70,70)
BUTTON_HOVER_COLOR = (150,150,150)

IMAGE_BUTTON_COMMAND = "set_image"

#Entry_box
ENTRY_BOX_OFFSET = 5
ENTRY_BOX_WIDTH, ENTRY_BOX_HEIGHT = (SIDEBAR_SIZE * GRID_SIZE) - 2 * ENTRY_BOX_OFFSET, 30
ENTRY_BOX_COLOR = (70,70,70)
SELECTED_ENTRY_BOX_COLOR = (150,150,150)
BLINK_SPEED = 30

#Sidebar Data
SIDEBAR_DATA = {"button_1":{"image_path":"dir_triangle.png","text":"Direction","type":"button"},
                "button_2":{"image_path":"assets/defence/canon_idol.png","text":"Canon","type":"button"},
                "entry_1":{"type":"entry"},
                "entry_2":{"type":"entry"},
                "button_3":{"type":"button"}
                }

#Sprite types
ENEMY = ["tank_0.png"]
DEFENCE = ["canon_idol.png"]
DIRECTION = ["dir_triangle.png"]
OTHER = "other"

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)