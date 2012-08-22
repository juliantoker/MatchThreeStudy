import pygame,os
from pygame.locals import *

# constants
white = (255,255,255)
black = (0,0,0)
red = (255,102,73)
green = (107,255,113)
blue = (58,167,255)
magenta = (147,112,219) # 243,145,187
yellow = (255,244,80)

color_list = [white,black,blue,green,red,magenta,yellow]
color_tuple = (white,black,blue,green,red,magenta,yellow)
color_dict = {'white':white,'black':black,'blue':blue,'green':green,
              'red':red,'magenta':magenta,'yellow':yellow}

EXTENSION_DELIMETER = '.'

def name_ext(f):
    if not EXTENSION_DELIMETER in f:
        return (None, None)
    else:
        si = f.find(EXTENSION_DELIMETER)
        return (f[:si], f[si+1:])
    
def _list_paths(root_dir, extensions):
    file_paths = []
    directory_paths = []
    for i in [os.path.join(root_dir, x) for x in os.listdir(root_dir)]:
        if os.path.isfile(i):
            (name, ext) = name_ext(i)
            if name and ((not extensions) or (ext in extensions)):
                #p rint 'adding %s to files' % i
                file_paths.append(os.path.join(root_dir, i))
        elif os.path.isdir(i):
            #print 'adding %s to dirs' % i
            directory_paths.append(os.path.join(root_dir, i))
    subdir_files = filter(lambda x: x, map(lambda y: _list_paths(y, extensions), directory_paths))
    # print subdir_files
    for fls in subdir_files:
        for f in fls:
            file_paths.append(f)
    return file_paths
    
def getFilenames(rootDirectory, fileExtensions=None, returnRelativePaths=True):
    """IN: Str rootDirectory, optional list of strings containing the desired file extensions,
    optional boolean. Returns a list containing the absolute paths of all files of the passed
    in extensions from the passed in directory."""
    root_path = os.path.abspath(rootDirectory)
    exts = fileExtensions if fileExtensions else None
    return _list_paths(root_path, exts)
       
def findIndices(value, qlist):
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

def initializeScreen(resolution,backgroundColor):
    """In: (width,height) resolution tuple, RGB tuple. OUT: Pygame surface. Creates a screen
    object of the specified resolution filled with the specified backgroundColor."""
    screen = pygame.display.set_mode(resolution)
    screen.fill(background_color)
    return screen

def testShell():
    """IN: Nothing. OUT: Void. Polls pygame's event loop and ends the program if a QUIT event
    is triggered. Place a call to testShell() in your game/update loop."""        
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            # exits pygame
            pygame.quit()
            # terminates all active threads
            os._exit(1)
            
@memoize            
def loadImage(name, colorKey = None):
    """IN: String, optional Int. OUT: Pygame surface.
    Loads an image file of the passed
    in name value from the 'data' sub-
    directory. If the colorKey argument
    is -1, the top left pixel will be
    used for transparency purposes."""
        
    fullName = os.path.join('data',name)
    try:
        image = pygame.image.load(fullName)
    except pygame.error, message:
        print 'Cannot load image:',name
        raise SystemExit,message
    image = image.convert()
    if colorKey == -1:
        colorKey = image.get_at((0,0))
    image.set_colorkey(colorKey, RLEACCEL)
    return image

def loadSound(name):
    """IN: String. OUT: Pygame sound object.
    Creates a Pygame sound from a .OGG or an
    uncompressed .WAV file. """
    
    fullName = os.path.join('data',name)
    try:
        sound = pygame.mixer.Sound(fullName)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound


#def main():
#    root_directory = '/Users/michaelsobczak54/Documents/workspace/CTAT_STUFF/Examples/flash/FractionAddition/CognitiveTutorProblems'
#    my_ext = ['wme', 'pr']
#    print '\n'.join([str(x) for x in getFilenames(root_directory, my_ext)])
#    
#main()







    
