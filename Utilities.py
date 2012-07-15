import pygame,sys,os
from pygame.locals import *

white = (255,255,255)
black = (0,0,0)
red = (255,102,73)
green = (107,255,113)
blue = (58,167,255)
magenta = (147,112,219) # 243,145,187
yellow = (255,244,80)

colors = (white,black,blue,green,red,magenta,yellow)
quota_colors = (black,blue,green,red,magenta,yellow)

def all_indices(value, qlist):

    """IN:Value,Iterable. OUT:The indicies of all occurences
    of value in qlist."""
    
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices

def Screen_Init(width,height,background_color):

    """Initializes a screen of the given dimensions with the specified background color."""

    background_color = background_color
    (width,height) = (width,height)

    screen = pygame.display.set_mode((width,height))
    screen.fill(background_color)

    pygame.display.flip()

def test_shell():
        
    for event in pygame.event.get():
            
        if event.type == pygame.QUIT:

            print False
            return False
        
        else:
            return True
    
def Load_Image(Name, Color_Key = None):

    """Loads an image file of the passed
    in Name value from the 'data' sub-
    directory. If the Color_Key argument
    is -1, the top left pixel will be
    used for transparency purposes."""

    Full_Name = os.path.join('data',Name)

    try:

        Image = pygame.image.load(Full_Name)

    except pygame.error, message:

        print 'Cannot load image:',Name
        raise SystemExit,message

    Image = Image.convert()

    if Color_Key == -1:

        Color_Key = Image.get_at((0,0))

    Image.set_colorkey(Color_Key, RLEACCEL)

    return Image


def Load_Sound(Name):

    Full_Name = os.path.join('data',Name)

    try:

        Sound = pygame.mixer.Sound(Full_Name)

    except pygame.error, message:

        print 'Cannot load sound:', Name
        raise SystemExit, message

    return Sound










    
