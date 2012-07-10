import pygame,random,Utilities,math,mtgeneralutilities as gu
from threading import Timer
from pygame.locals import *
from viewconfig import *
pygame.init()
### Screen Initialization ###

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
screen.fill(Utilities.white)

### Game Constants Initialization ###

black_block = Utilities.Load_Image('black_block.png',Utilities.white)
blue_block = Utilities.Load_Image('blue_block.png',Utilities.white)
green_block = Utilities.Load_Image('green_block.png',Utilities.white)
red_block = Utilities.Load_Image('red_block.png',Utilities.white)
magenta_block = Utilities.Load_Image('magenta_block.png',Utilities.white)
yellow_block = Utilities.Load_Image('yellow_block.png',Utilities.white)

small_black_block = Utilities.Load_Image('small_black_block.png',Utilities.white)
small_blue_block = Utilities.Load_Image('small_blue_block.png',Utilities.white)
small_green_block = Utilities.Load_Image('small_green_block.png',Utilities.white)
small_red_block = Utilities.Load_Image('small_red_block.png',Utilities.white)
small_magenta_block = Utilities.Load_Image('small_magenta_block.png',Utilities.white)
small_yellow_block = Utilities.Load_Image('small_yellow_block.png',Utilities.white)

block_sprite_dict = {Utilities.black:black_block,Utilities.blue:blue_block,Utilities.green:green_block,Utilities.red:red_block,Utilities.magenta:magenta_block,Utilities.yellow:yellow_block}

small_block_sprite_array = [small_black_block,small_blue_block,small_green_block,
                            small_red_block,small_magenta_block,small_yellow_block]

Block_Group = pygame.sprite.Group() #Delete this once the new graphics are coded.
BLOCK_SIZE = (74,) * 2 #V
BLOCK_VELOCITY = 8 #V
Side_Length = 80 #V
BLOCK_HALF_LENGTH = Side_Length/2 #V
COLOR_LOOKUP = dict(zip(range(gu.TILE_VARIETY), Utilities.colors)) #V
quota_color_lookup = dict(zip(range(gu.TILE_VARIETY),Utilities.quota_colors))
BAR_COLOR = Utilities.red #V
running = True #Main
Player_Selections = [] #V
BOARD_OFFSET_X,BOARD_OFFSET_Y = 450,180 #V
BOARDER_IMAGE_PATH = 'Border.gif' #V
BORDER_OFFSET_X,BORDER_OFFSET_Y = 51,46 #V
BAR_OFFSET_X,BAR_OFFSET_Y = 0,130 #V
BAR_WIDTH,BAR_HEIGHT = 480,70 #V
PAUSE_INTERVAL = 1000 #V
BLOCK_CLEAR_TIME = 0.2 #V
BAR_BORDER_THICKNESS = 2 #V
FALL_THRESHOLD = 1 #V
[COLUMN1_LOCK,COLUMN2_LOCK,COLUMN3_LOCK,COLUMN4_LOCK,COLUMN5_LOCK,COLUMN6_LOCK] = [0] * gu.HORIZONTAL_TILES #V
locks = [COLUMN1_LOCK,COLUMN2_LOCK,COLUMN3_LOCK,COLUMN4_LOCK,COLUMN5_LOCK,COLUMN6_LOCK] #V
QUOTA_BG_WIDTH,QUOTA_BG_HEIGHT = 200,480
QUOTA_BLOCK_OFFSET = 40
sprite_array = [ [gu.EMPTY] * (gu.VERTICAL_TILES * gu.BUFFER_MULT) for i in range(gu.HORIZONTAL_TILES)] #V

BG_WIDTH,BG_HEIGHT = gu.HORIZONTAL_TILES * Side_Length, gu.BUFFER_MULT * gu.VERTICAL_TILES * Side_Length

background = pygame.Surface((BG_WIDTH,BG_HEIGHT)) #V
BG_LOC = (BOARD_OFFSET_X,BOARD_OFFSET_Y - (gu.VERTICAL_TILES * Side_Length * (gu.BUFFER_MULT - 1)))

quota_bg = pygame.Surface((QUOTA_BG_WIDTH,QUOTA_BG_HEIGHT))
                          
curtain = pygame.Surface((BG_WIDTH,BOARD_OFFSET_Y - 0.9*BORDER_OFFSET_Y))

Border = Utilities.Load_Image(BOARDER_IMAGE_PATH,Utilities.white) #V
Border = Border.convert_alpha()

FONT_SIZE = 50
FONT_POSITION = screen.get_rect().topleft
FONT_COLOR = Utilities.black
font = pygame.font.Font(None,FONT_SIZE)

sprites_at_dest = [] #V
sprites_at_xdest = [] #V

pygame.event.set_allowed(None)
pygame.event.set_allowed(MOUSEBUTTONDOWN)
