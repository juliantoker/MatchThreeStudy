### Model Imports ###

import pygame,random,Utilities,math,mtgeneralutilities as gu,pdb
from threading import Timer
from pygame.locals import *
from viewconfig import *

### Pygame Initialization ###

pygame.init()

### Lambda Function Declarations ###

Color_Interpreter = lambda x: COLOR_LOOKUP[x] #V
One_To_The_Right = lambda Block_Selection: (Block_Selection[0] + 1, Block_Selection[1]) #V
report_at_dest = lambda cord_array: sprites_at_dest.append(cord_array) #V
report_at_xdest = lambda cord_array: sprites_at_xdest.append(cord_array) #V

### Game Function Declarations ###

def Location_Selector(Row_Index,Column_Index): #V
    
    """Determines each block's appropriate screen location
    given its row and column indicies as well as its side length"""
    
    X_Coordinate =  BOARD_OFFSET_X + (Row_Index * Side_Length) 
    Y_Coordinate =  BOARD_OFFSET_Y + Side_Length * (Column_Index - gu.VERTICAL_TILES * (gu.BUFFER_MULT - 1))

    return (X_Coordinate,Y_Coordinate)

BAR_X = Location_Selector(0,gu.VERTICAL_TILES)[0] - BAR_OFFSET_X #V
BAR_Y = Location_Selector(0,gu.VERTICAL_TILES)[1] - BAR_OFFSET_Y #V

def Draw_Location_Selector(Row_Index,Column_Index): #V
    
    """Determines each block's appropriate screen location
    given its row and column indicies as well as its side length"""
    
    X_Coordinate =  (Row_Index * Side_Length) 
    Y_Coordinate =  (Column_Index * Side_Length) 

    return (X_Coordinate,Y_Coordinate)

def unlock(lock): #V

    locks[lock] = 0

def engage_locks(kill_list): #V

    COLUMN = 0
    for kill in kill_list:
        
        locked_column = kill[COLUMN]
        locks[locked_column] = 1
        timer = Timer(BLOCK_CLEAR_TIME,unlock,(locked_column,))
        timer.start()

class Block(pygame.sprite.Sprite): #V

    velocity = BLOCK_VELOCITY

    def __init__(self,location,color):

        """IN: Screen location tuple, RGB tuple."""

        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.surface = pygame.Surface(BLOCK_SIZE)
        self.surface.fill(self.color)
        self.position = location
        Block_Group.add(self)
        background.blit(self.surface,self.position)

class NBlock(pygame.sprite.Sprite): #V
    
    def __init__(self,cord,color):

        """IN: Cord array that specifies the starting
        model location of the sprite and the sprite's
        color RGB tuple."""
        
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.cord = cord
        self.location_tuple = Draw_Location_Selector(self.cord[0],self.cord[1])
        self.x = self.location_tuple[0] 
        self.y = self.location_tuple[1]
        self.surface = pygame.Surface(BLOCK_SIZE)
        self.surface.fill(self.color)
        self.surface = block_sprite_dict[self.color]
        self.dest = self.y
        self.xdest = self.x
        self.at_dest = False
        self.yinit_flag = True
        self.init_flag = True
        
    def update(self):

        """IN: Integer dest that specifies the desired
        screen location of the sprite."""

    
        distance_from_destination = abs(self.y - self.dest)
        xdistance_from_destination = abs(self.x - self.xdest)
        if locks[self.cord[0]] == 0:
            if distance_from_destination > FALL_THRESHOLD:
                self.yinit_flag = False
                self.y += BLOCK_VELOCITY
                
            elif xdistance_from_destination > FALL_THRESHOLD:
                self.init_flag = False
                if self.x > self.xdest: #I.e block is being shifted left.

                    self.x -= BLOCK_VELOCITY
                    
                elif self.x < self.xdest: #I.e block is being shifted right.

                    self.x += BLOCK_VELOCITY

            elif xdistance_from_destination <= FALL_THRESHOLD and not self.init_flag:

                self.x = self.xdest
                self.init_flag = True
                report_at_xdest(self.cord)

            elif distance_from_destination <= FALL_THRESHOLD and not self.yinit_flag:

                self.y = self.dest
                report_at_dest(self.cord)
                
            else:
                pass

        background.blit(self.surface,(self.x,self.y))

def add_sprites(spawn_tuple,sprite_array): #V

    """IN:Nested spawn tuple from the model specifying where the new sprites should be instantiated
    within the sprite array and the nested sprite array. spawn_tuple[0] = cord spawn_tuple[1] = RGB
    Instantiates sprites in the sprite_array where the spawn_tuple specifies."""
    
    for entry in spawn_tuple:
        
        cord = entry[0]
        color = Color_Interpreter(entry[1])
        sprite_array[cord[0]][cord[1]] = NBlock(cord,color)
        
	    		
def Draw_Blocks(Game_State): #V #OBSOLETE: DOES NOT DRAW THE BLOCKS!!!

    """IN:Nested tuple. OUT:Void. Iterates through all spaces
    and blits the appropriately colored sprites to the correct
    coordinates. Updates the screen when iteration is finished."""

    background.fill(Utilities.white)

    for CORD in gu.Two_D_Nested_Iter(Game_State):

        CURRENT_ENTRY = Game_State[CORD[0]][CORD[1]]
        if CURRENT_ENTRY == gu.EMPTY:
            continue
        CURRENT_COLOR = Color_Interpreter(CURRENT_ENTRY)
        CURRENT_LOCATION = Draw_Location_Selector(CORD[0],CORD[1])
        block = Block(CURRENT_LOCATION,CURRENT_COLOR)
        
    else:
        screen.blit(background,BG_LOC)
        pygame.display.flip()

def Center_Position(Position,Side_Length = 80): #V

    """Transforms the upper-left corner block positions
    into center positions used for mouse collision
    detection."""

    Half_Length = Side_Length/2
    New_X = Position[0] + Half_Length
    New_Y = Position[1] + Half_Length
    
    return((New_X,New_Y))


def Mouse_Select(Game_State,x,y): #V

    """IN:Nested Game_State tuple and the screen coordinates
    x,y of the mouse click. OUT: The model coordinates of the
    clicked block. Determines which block the player has clicked."""
    
    for CORD in gu.Two_D_Nested_Iter(Game_State):
        
        if CORD[1] >= gu.TOP_PLAY_ROW: #Makes sure the buffer tiles can't be selected.
            
            BASE_POINT = Location_Selector(CORD[0],CORD[1])
            CENTER_POINT = Center_Position(BASE_POINT)
            delta_x = CENTER_POINT[0] - x
            delta_y = CENTER_POINT[1] - y
            if math.hypot(delta_x, delta_y) <= BLOCK_HALF_LENGTH:
                  
                
                SELECTED_BLOCK = [CORD[0],CORD[1]]
                return SELECTED_BLOCK  

def Load_Border(): #V

    ROUGH_LOCATION = Location_Selector(0,gu.VERTICAL_TILES * (gu.BUFFER_MULT - 1))
    X = ROUGH_LOCATION[0] - BORDER_OFFSET_X 
    Y = ROUGH_LOCATION[1] - BORDER_OFFSET_Y 
    NEW_LOCATION = (X,Y)
    screen.blit(Border,NEW_LOCATION)

def Draw_Progress_Bar(SURFACE,COLOR,MAX_WIDTH,MAX_QUANTITY,LOAD_QUANTITY,LOCATION,HEIGHT,BORDER_COLOR = (0,0,0)): #V

    PROGRESS = LOAD_QUANTITY/MAX_QUANTITY
    CURRENT_WIDTH = MAX_WIDTH * PROGRESS

    BAR_RECT = pygame.Rect(LOCATION[0],LOCATION[1],CURRENT_WIDTH,HEIGHT)
    BORDER_RECT = pygame.Rect(LOCATION[0],LOCATION[1],MAX_WIDTH,HEIGHT)

    pygame.draw.rect(SURFACE,Utilities.white,BORDER_RECT)
    pygame.draw.rect(SURFACE,COLOR,BAR_RECT)
    pygame.draw.rect(SURFACE,BORDER_COLOR,BORDER_RECT,BAR_BORDER_THICKNESS)
    
def init_view_spawn(game_state,sprite_array): #V

    """IN: G.S. OUT: Sprite tuple. Spawns NBlock objects in the buffer area
    of a a sprite tuple to match the passed in g.s."""

    for CORD in gu.Two_D_Nested_Iter(game_state):
    
        color = Color_Interpreter(game_state[CORD[0]][CORD[1]])
        sprite_array[CORD[0]][CORD[1]] = NBlock((CORD[0],CORD[1]),color)

    else:
        
        return sprite_array

def update_sprites(sprite_array): #V

    """IN:Sprite tuple. OUT:Void. Each element's
    update() called ."""
       
    for cord in gu.Two_D_Nested_Iter(sprite_array):
        entry = sprite_array[cord[0]][cord[1]]
        if entry != gu.EMPTY:
            
            entry.update() 

def draw_blocks(sprite_array): #V

    """IN:Sprite tuple. Updates and renders the sprites
    within the passed in sprite tuple."""
    
    background.fill(Utilities.white)

    update_sprites(sprite_array)

    screen.blit(background,BG_LOC)

def not_moving_check(block_selection,sprite_array): #V

    """IN:[i,j] sprite array coordinate list and sprite array.
    OUT: Boolean. Returns True of the sprite in the [i,j]
    position's init_flag flag is True and False otherwise."""
    
    if block_selection[0] < gu.HORIZONTAL_TILES:
        checked_entry = sprite_array[block_selection[0]][block_selection[1]]
        if  type(checked_entry) is not int and checked_entry.init_flag:
            return True
        else:
            return False
    else:
        return False
    
def generate_swap_request(event,sprite_array): #V

    """IN:Sprite array. OUT:Nested array swap request."""
    for ev in event:
        if ev.type == pygame.MOUSEBUTTONDOWN:
            (mouse_x,mouse_y) = pygame.mouse.get_pos()
            selection = Mouse_Select(sprite_array,mouse_x,mouse_y)
            if selection != None:
                right_neighbor = [selection[0] + 1,selection[1]]
                if  right_neighbor != None and not_moving_check(selection,sprite_array) and not_moving_check(right_neighbor,sprite_array):
                    #print selection,sprite_array[selection[0]][selection[1]].color
                    return selection
        else:
            
            return None
    
def process_other_input(event):

    return None #Have a dict lookup for each event type.

def check_for_input(sprite_array): #V

    """IN:game state tuple. OUT:Tuple of Swap request and other input(A,B)."""

    event = pygame.event.get()
    return (generate_swap_request(event,sprite_array),process_other_input(event))

def hide_buffer(): #V

    """IN:Void. OUT:Void. Covers up the buffer."""

    curtain.fill(Utilities.white)
    screen.blit(curtain,(BOARD_OFFSET_X,0))

def draw_score(score): #V

    """IN:Integer score. OUT:Void. Draws the score to the screen."""

    score = str(score)

    text = font.render(score,True,FONT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = screen.get_rect().topleft
    screen.blit(text,text_rect)
    
def quota_point_assignment(quota_index):

    quota_x = QUOTA_BLOCK_OFFSET
    quota_y = QUOTA_BLOCK_OFFSET + (Side_Length * quota_index)

    return (quota_x,quota_y)

def make_quota_block(quota_index):

    color = quota_color_lookup[quota_index]
    block = pygame.Surface((BLOCK_HALF_LENGTH,BLOCK_HALF_LENGTH))
    block.fill(color)
    block = small_block_sprite_array[quota_index]
    return block

def render_quota(quota_array):
    
    quota_bg.fill(Utilities.white)
    
    for index,color_quota in enumerate(quota_array):

        base_point = quota_point_assignment(index)
        
        quota_text = ':' + str(color_quota)
        text = font.render(quota_text,True,FONT_COLOR)
        text_rect = text.get_rect()

        block = make_quota_block(index)
        block_rect = block.get_rect()

        block_rect.center = base_point
        text_rect.midleft = (base_point[0] + 20,base_point[1])

        quota_bg.blit(text,text_rect)
        quota_bg.blit(block,block_rect)

    quota_point = Draw_Location_Selector(0,3)
    quota_x = quota_point[0] + 200
    quota_y = quota_point[1]
    screen.blit(quota_bg,(quota_x,quota_y))
    
def render(sprite_array,score,max_time,game_time,quota_array): #V

    """IN:Sprite tuple. OUT:Void. Carries out all blitting."""
    
    screen.fill(Utilities.white)
    draw_score(score)
    draw_blocks(sprite_array)
    hide_buffer()
    Draw_Progress_Bar(screen,BAR_COLOR,BAR_WIDTH,max_time,game_time,(BAR_X,BAR_Y),BAR_HEIGHT) #Be mindful of which variables come from the model.
    Load_Border()
    render_quota(quota_array)
    pygame.display.flip()

def number_of_empties(cord,column): #V

    """IN:Integer cord and column array. OUT: The number of zeroes
    below the cord entry of the passed in column."""

    empty_number = 0
    for index in xrange(cord,len(column)):

        if column[index] == gu.EMPTY:

            empty_number += 1
    else:

        return empty_number

def assign_destinations(sprite_array): #V

    """IN:Nested sprite array. OUT:Void. Updates the dest parameter for each sprite(NBlocks)
    within the nested sprite tuple."""

    for column_index in gu.Array_Index(sprite_array):

        column = sprite_array[column_index]
        lowest_empty_cord = gu.lowest_empty(column)
        
        
        for row_index in gu.Array_Index(column): #Only iterates through sprites above the lowest empty space.

            sprite = column[row_index]
            if sprite != gu.EMPTY:
                if lowest_empty_cord != None:
                    empties = number_of_empties(row_index,column)
                    dest_increase = empties * Side_Length #How far the sprite must fall.
                    coordinate_location = Draw_Location_Selector(sprite.cord[0],sprite.cord[1])[1]
                    new_dest = coordinate_location + dest_increase
                    sprite.dest = new_dest
                else:
                    if row_index == 0:
                        sprite.dest = sprite.y - 1 # THIS IS CAUSING AN ERROR.
                    

def remove_tiles(kill_list,sprite_array): #V

    """IN:Kill list passed in by the model via the controller
    and the sprite array. Removes sprites in the cords specified
    in the kill_list from the sprite array."""

    for cord in kill_list:

        x = cord[0]
        y = cord[1]
        sprite_array[x][y] = gu.EMPTY #Make sure pygame's garbage collection removes the replaced sprite.

def assign_xdest(swap_verdict,sprite_array): #V

    """IN:Array what block should be swapped with its right neighbor, sprite array.
    OUT:Void. The specified coordinate and its right neighbor will have
    appropriate xdest params set."""
    if swap_verdict != None:
        
        sprite = sprite_array[swap_verdict[0]][swap_verdict[1]]
        next_sprite = sprite_array[swap_verdict[0] + 1][swap_verdict[1]]
        
        sprite_x = sprite.x
        next_x = next_sprite.x
        
        sprite.xdest = next_x
        next_sprite.xdest = sprite_x

        sprite_array[swap_verdict[0]][swap_verdict[1]] = next_sprite
        sprite_array[swap_verdict[0] + 1][swap_verdict[1]] = sprite
        
def rectify_sprite_array(sprite_array): #V
    
    """IN:Sprite array. Makes the sprites' cord attribute
    match their position within the passed in sprite array."""
    
    for cord in reversed(gu.Two_D_Nested_Iter(sprite_array)):

        sprite = sprite_array[cord[0]][cord[1]]
        if sprite != gu.EMPTY:
            sprite.cord = cord
                            

def lock_check(selection,lock_array):

    if selection != None:
        requested_column = selection[0]
        
        if lock_array[requested_column] == 0:

            return selection
        else:
            return []

def check_combo(combo_number):

    pass
    
        
        
if __name__ == '__main__':
    
    B = [[(0, 0), 2], [(0, 1), 4], [(0, 2), 1], [(0, 3), 5], [(0, 4), 1], [(0, 5), 6],[(0, 6), 5], [(0, 7), 5],
         [(1, 0), 6], [(1, 1), 3],[(1, 2), 1], [(1, 3), 6], [(1, 4), 1], [(1, 5), 2],[(1, 6), 1], [(1, 7), 3],
         [(2, 0), 2], [(2, 1), 5], [(2, 2), 5],[(2, 3), 6], [(2, 4), 4], [(2, 5), 5], [(2, 6), 4], [(2, 7), 3],
         [(3, 0), 2], [(3, 1), 5], [(3, 2), 1], [(3, 3), 5], [(3, 4), 5],[(3, 5), 6], [(3, 6), 3], [(3, 7), 2],
         [(4, 0), 1], [(4, 1), 2],[(4, 2), 6], [(4, 3), 3], [(4, 4), 2], [(4, 5), 2], [(4, 6), 1],[(4, 7), 1],
         [(5, 0), 2], [(5, 1), 2], [(5, 2), 4], [(5, 3), 2],[(5, 4), 4], [(5, 5), 1], [(5, 6), 1], [(5, 7), 3]]
    
    A = [100,39,55,3]
    render_quota(A)
    

    


