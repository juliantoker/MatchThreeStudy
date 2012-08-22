import pygame
import random
import Utilities
import math
import mtgeneralutilities as gu
import os
import re
from threading import Timer
from pygame.locals import *
from viewconfig import *
pygame.init()

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
lastComboNumber = 0
BLOCK_SIZE = (74,) * 2 
BLOCK_VELOCITY = 10 
SWAP_VELOCITY = 10
SIDE_LENGTH = 80 
BLOCK_HALF_LENGTH = SIDE_LENGTH/2 
colorLookUp = dict(zip(range(gu.TILE_VARIETY), Utilities.color_tuple)) 
quotaLookUp = dict(zip(range(gu.TILE_VARIETY),Utilities.color_tuple[1:]))
barColor = Utilities.red 
running = True 
BOARD_OFFSET_X,BOARD_OFFSET_Y = 450,180 
BOARDER_IMAGE_PATH = 'Border.gif' 
BORDER_OFFSET_X,BORDER_OFFSET_Y = 51,46 
BAR_OFFSET_X,BAR_OFFSET_Y = -35,130 
BAR_WIDTH,BAR_HEIGHT = 480,70 
PAUSE_INTERVAL = 1000 
BLOCK_CLEAR_TIME = 0.2 
BAR_BORDER_THICKNESS = 2 
FALL_THRESHOLD = 1 
ALPHA_THRESHOLD = 0
[COLUMN1_LOCK,COLUMN2_LOCK,COLUMN3_LOCK,COLUMN4_LOCK,COLUMN5_LOCK,COLUMN6_LOCK] = [0] * gu.HORIZONTAL_TILES 
locks = [COLUMN1_LOCK,COLUMN2_LOCK,COLUMN3_LOCK,COLUMN4_LOCK,COLUMN5_LOCK,COLUMN6_LOCK] 
QUOTA_BG_WIDTH,QUOTA_BG_HEIGHT = 300,700
QUOTA_BLOCK_OFFSET = 120
BG_WIDTH,BG_HEIGHT = gu.HORIZONTAL_TILES * SIDE_LENGTH, gu.BUFFER_MULT * gu.VERTICAL_TILES * SIDE_LENGTH
BG_LOC = (BOARD_OFFSET_X,BOARD_OFFSET_Y - (gu.VERTICAL_TILES * SIDE_LENGTH * (gu.BUFFER_MULT - 1)))

# sprite storage
blockGroup = pygame.sprite.Group() 
playerSelections = [] 
deadSprites = []
spriteList = [ [gu.EMPTY] * (gu.VERTICAL_TILES * gu.BUFFER_MULT) for i in range(gu.HORIZONTAL_TILES)] 
spritesAtYDest = [] 
spritesAtXDest = [] 

# limit player input
pygame.event.set_allowed(None)
pygame.event.set_allowed(MOUSEBUTTONDOWN)
pygame.event.set_allowed(QUIT)

# define pygame surfaces
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),DOUBLEBUF)
screen.fill(Utilities.white)
background = pygame.Surface((BG_WIDTH,BG_HEIGHT)) 
background.set_colorkey(Utilities.white)
background = background.convert()

backgroundMask = pygame.Surface((500,660))
backgroundMask.fill(Utilities.black)
backgroundMask.set_alpha(100)
backgroundMask = backgroundMask.convert_alpha()

quota_bg = pygame.Surface((QUOTA_BG_WIDTH,QUOTA_BG_HEIGHT))
quota_bg.set_colorkey(Utilities.white)
quota_bg = quota_bg.convert()

curtain = pygame.Surface((BG_WIDTH,BOARD_OFFSET_Y - 0.9*BORDER_OFFSET_Y))
curtain.set_colorkey(Utilities.white)
curtain = curtain.convert()

Border = Utilities.loadImage(BOARDER_IMAGE_PATH,Utilities.white)
Border = Border.convert_alpha()

# load sprites
backgroundSprite = Utilities.loadImage('background.png',Utilities.white)
quotaOutline = Utilities.loadImage('quotaOutline.png',Utilities.white)
clock = Utilities.loadImage('clock.png',Utilities.white)

black_block = Utilities.loadImage('black_block.png')
blue_block = Utilities.loadImage('blue_block.png')
green_block = Utilities.loadImage('green_block.png')
red_block = Utilities.loadImage('red_block.png')
magenta_block = Utilities.loadImage('magenta_block.png')
yellow_block = Utilities.loadImage('yellow_block.png')

small_black_block = Utilities.loadImage('small_black_block.png')
small_blue_block = Utilities.loadImage('small_blue_block.png')
small_green_block = Utilities.loadImage('small_green_block.png')
small_red_block = Utilities.loadImage('small_red_block.png')
small_magenta_block = Utilities.loadImage('small_magenta_block.png')
small_yellow_block = Utilities.loadImage('small_yellow_block.png')

black_block_surprised = Utilities.loadImage('black_block_surprised.png')
blue_block_surprised = Utilities.loadImage('blue_block_surprised.png')
green_block_surprised = Utilities.loadImage('green_block_surprised.png')
red_block_surprised = Utilities.loadImage('red_block_surprised.png')
magenta_block_surprised = Utilities.loadImage('magenta_block_surprised.png')
yellow_block_surprised = Utilities.loadImage('yellow_block_surprised.png')

spriteDict = {Utilities.black:black_block,Utilities.blue:blue_block,Utilities.green:green_block,Utilities.red:red_block,Utilities.magenta:magenta_block,Utilities.yellow:yellow_block}

smallSpriteList = [small_black_block,small_blue_block,small_green_block,
                            small_red_block,small_magenta_block,small_yellow_block]

surprisedSpriteDict = {Utilities.black:black_block_surprised,Utilities.blue:blue_block_surprised,
                       Utilities.green:green_block_surprised,Utilities.red:red_block_surprised,
                       Utilities.magenta:magenta_block_surprised,Utilities.yellow:yellow_block_surprised}

### Fonts ###

FONT_SIZE = 50
FONT_POSITION = screen.get_rect().topleft
FONT_COLOR = Utilities.black
font = pygame.font.Font(None,FONT_SIZE)


