import pygame,random,Utilities,math,pdb,mtgeneralutilities as gu
from threading import Timer
from pygame.locals import *
pygame.init()

SCORE = 0 #M
GAME_TIME_LENGTH = 0 #M
MAX_TIME = 120.0 #M
CLOCK = pygame.time.Clock() #M
TIME_BUFFER = 0 #M
Kill_List = [] #M
spawn_report = []
BLOCK_VALUE = 20 #M
SECONDS_GAINED = 0.60 #M
TICK_INTERVAL = 1000 #M
BONUS_OFFSET = 2 #M
progress_decrement = 1
Game_State = ((gu.EMPTY,) * gu.VERTICAL_TILES * gu.BUFFER_MULT,) * gu.HORIZONTAL_TILES #M
number_of_sprites_requested = [ gu.EMPTY for i in range(gu.HORIZONTAL_TILES) ]

BLACK_QUOTA = 0
BLUE_QUOTA = 0
GREEN_QUOTA = 0
RED_QUOTA = 0
MAGENTA_QUOTA = 0
YELLOW_QUOTA = 0
quota_array = [0,BLACK_QUOTA,BLUE_QUOTA,GREEN_QUOTA,RED_QUOTA,MAGENTA_QUOTA,YELLOW_QUOTA]

tick = lambda: CLOCK.tick() #M
random_color = lambda: random.choice(range(1,gu.TILE_VARIETY)) #M
not_on_the_far_right = lambda x_selection,Game_State: x_selection != gu.HORIZONTAL_TILES - 1 #M
one_to_the_left = lambda Block_Selection: (Block_Selection[0] - 1, Block_Selection[1]) #M
not_clicking_white = lambda Game_State,Block_Selection: Game_State[Block_Selection[0]][Block_Selection[1]] != gu.EMPTY #M
calculate_score = lambda BLOCKS_CLEARED: BLOCK_VALUE * BLOCKS_CLEARED #M
calculate_multiplier = lambda BLOCKS_CLEARED: BLOCKS_CLEARED - BONUS_OFFSET #M
tally_score = lambda BLOCKS_CLEARED: calculate_score(len(BLOCKS_CLEARED)) * calculate_multiplier(len(BLOCKS_CLEARED)) #M
update_time = lambda TIME_BUFFER: TIME_BUFFER + tick() #M
report_spawn = lambda spawn_info: spawn_report.append(spawn_info)
pick_entries = lambda column_index,kill_list: [x for x in kill_list if x[0] == column_index]

def decrement_progress(swap_request,current_progress):

    """IN:Array swap_request and int current_progress. OUT:
    int new current progress. Decrements current progress
    every time the player makes a successful swap."""

    if swap_request != []:

        current_progress -= progress_decrement
        if current_progress < 0:
            current_progress = 0

    return current_progress
        
def fill_buffer(Game_State): #M

    """IN: Nested tuple game state.
    OUT: Nested tuple game state with
    its buffer filled with random
    tiles."""

    Game_State = gu.Tuple_To_Array(Game_State)

    for CORD in gu.Two_D_Nested_Iter(Game_State):

        color = random_color()
        Game_State[CORD[0]][CORD[1]] = color
        report_spawn([(CORD[0],CORD[1]),color])

    else:

        Game_State = gu.Array_To_Tuple(Game_State)
        return Game_State

def drop_column(column): #M #Antiquated

    """IN: Column Tuple. Drops the given column's blocks. """

    BOTTOM_ENTRY = len(column) - 1
    column = list(column)
    
    for i in reversed(gu.Array_Index(column)):

        if i != BOTTOM_ENTRY:
            
            entry = column[i]
            next_entry = column[i + 1]

            if entry != gu.EMPTY and next_entry == gu.EMPTY:

                column[i+1] = entry
                column[i] = gu.EMPTY

    return tuple(column)

def newest_drop_blocks(Game_State): #M #Anitquated

    game_state = gu.Tuple_To_Array(Game_State)
    for i in gu.Array_Index(Game_State):

        if locks[i] == 0:
            
            game_state[i] = drop_column(game_state[i])

    return tuple(game_state)

def spawn_blocks(Game_State): #M

    """IN:Nested tuple. OUT:Nested tuple. Spawns new blocks in the top-most column entry
    if it is gu.EMPTY."""

    TOP_ROW = 0
    
    Game_State = gu.Tuple_To_Array(Game_State)

    for column_index in gu.Array_Index(Game_State):

        top_entry = Game_State[column_index][TOP_ROW]
        
        if top_entry == gu.EMPTY: 
            
            NEW_ENTRY = random_color()
            Game_State[column_index][TOP_ROW] = NEW_ENTRY
            
            report_spawn([(column_index,TOP_ROW),NEW_ENTRY])
       
    Game_State = gu.Array_To_Tuple(Game_State)
    
    return(Game_State)

def find_row_matches(Game_State,MATCH_STATE = 3): #M

    """IN:Nested tuple, int(optional). OUT:Nested array containing
    tuple elements. Finds matches of at least MATCH_STATE in
    length along the rows of a given matrix. MATCH_STATE = 3 by default""" 

    Game_State = gu.Tuple_To_Array(Game_State)
    PREVIOUS_ENTRY = gu.EMPTY
    Output_Array = []
    Holder_Array = []
    MATCH_NUMBER = 1

    for row_index in gu.Array_Index(Game_State[0]): #Notice the inversion of column and row indicies here.

        if row_index >= gu.TOP_PLAY_ROW:

            for column_index in gu.Array_Index(Game_State):

                CURRENT_ENTRY = Game_State[column_index][row_index]
                CURRENT_COORDINATE = (column_index,row_index)
                if gu.Column_Clear(Game_State,CURRENT_COORDINATE): 

                    if PREVIOUS_ENTRY == CURRENT_ENTRY and gu.Column_Clear(Game_State,one_to_the_left(CURRENT_COORDINATE)):

                        Holder_Array.append(CURRENT_COORDINATE)
                        PREVIOUS_ENTRY = CURRENT_ENTRY
                        MATCH_NUMBER += 1

                    elif PREVIOUS_ENTRY != CURRENT_ENTRY:

                        if MATCH_NUMBER >= MATCH_STATE:

                            Output_Array += Holder_Array
                            
                            Holder_Array = []
                            MATCH_NUMBER = 1
                            PREVIOUS_ENTRY = CURRENT_ENTRY

                        else:
                            
                            Holder_Array = []
                            Holder_Array.append(CURRENT_COORDINATE)
                            MATCH_NUMBER = 1
                            PREVIOUS_ENTRY = CURRENT_ENTRY
                            
                else:

                    Holder_Array = []
                    MATCH_NUMBER = 1
                    PREVIOUS_ENTRY = CURRENT_ENTRY                        
            else:

                if MATCH_NUMBER >= MATCH_STATE:

                    Output_Array += Holder_Array
                    Holder_Array = []
                    MATCH_NUMBER = 1
                    PREVIOUS_ENTRY = gu.EMPTY
                    

                else:
                    
                    Holder_Array = []
                    PREVIOUS_ENTRY = gu.EMPTY
                    MATCH_NUMBER = 1
        else:

            continue

    else:

        return(Output_Array)

                
def find_column_matches(Game_State,MATCH_STATE = 3): #M

    """IN:Nested tuple, int(optional). OUT: Nested
    array containing tuple elements.Finds matches
    of at least MATCH_STATE in length along the rows
    of a given matrix. MATCH_STATE = 3 by default"""

    Game_State = gu.Tuple_To_Array(Game_State)
    PREVIOUS_ENTRY = gu.EMPTY
    Output_Array = []
    Holder_Array = []
    MATCH_NUMBER = 1

    for column_index in gu.Array_Index(Game_State):

        for row_index in gu.Array_Index(Game_State[column_index]):

            if row_index >= gu.TOP_PLAY_ROW:

                CURRENT_ENTRY = Game_State[column_index][row_index]
                CURRENT_COORDINATE = (column_index,row_index)

                if gu.Column_Clear(Game_State,CURRENT_COORDINATE):

                    if PREVIOUS_ENTRY == CURRENT_ENTRY:

                        Holder_Array.append(CURRENT_COORDINATE)
                        PREVIOUS_ENTRY = CURRENT_ENTRY
                        MATCH_NUMBER += 1
                        
                    elif PREVIOUS_ENTRY != CURRENT_ENTRY:

                        if MATCH_NUMBER >= MATCH_STATE:
                            
                            Output_Array += Holder_Array
                            
                            Holder_Array = []
                            MATCH_NUMBER = 1
                            PREVIOUS_ENTRY = CURRENT_ENTRY

                        else:
                            
                            Holder_Array = []
                            Holder_Array.append(CURRENT_COORDINATE)
                            MATCH_NUMBER = 1
                            PREVIOUS_ENTRY = CURRENT_ENTRY

                else:

                    continue
            
        else:

            if MATCH_NUMBER >= MATCH_STATE:

                Output_Array += Holder_Array
                Holder_Array = []
                MATCH_NUMBER = 1
                PREVIOUS_ENTRY = gu.EMPTY

            else:
                
                Holder_Array = []
                PREVIOUS_ENTRY = gu.EMPTY
                MATCH_NUMBER = 1
            
    else:

        return(Output_Array)
            

def find_matches(Game_State): #M

    """Determines which blocks are making matches with thier neighbors."""
    
    return find_row_matches(Game_State) + find_column_matches(Game_State)

def decrement_quota(killed_color):

    """IN: The color of a matched block. OUT:Void.
    Decrements the appropriate entry of the quota array."""

    quota_array[killed_color] -= 1
    if quota_array[killed_color] < 0:
        quota_array[killed_color] = 0
    
def destroy_matches(Game_State,Kill_List): #M

    """IN:Nested Game_State tuple,Kill_List. OUT: Game_State.
    This function replaces all tiles at coordinates specified
    by the Kill_List with white ones."""

    Game_State = gu.Tuple_To_Array(Game_State)

    for kill_index in Kill_List:
        killed_color = Game_State[kill_index[0]][kill_index[1]]
        decrement_quota(killed_color)
        Game_State[kill_index[0]][kill_index[1]] = gu.EMPTY

    Game_State = gu.Array_To_Tuple(Game_State)
    
    return Game_State

def swap_check(selected_row,column): #M
    lowest_empty = gu.lowest_empty(column)
    if lowest_empty == None:
        lowest_empty = -100
    
    if selected_row > lowest_empty:

        return True
    else:
        return False

def real_swap_check(selected_row,column,next_column): #M
    
    if swap_check(selected_row,column) and swap_check(selected_row,next_column):

        return True

    else:

        return False

def improved_swap_blocks(Game_State,Block_Selection):#M

    """IN:Nested Game_State tuple,Block_Selection tuple. OUT:Nested tuple.
    Takes player tile selections and swaps them."""

    if Block_Selection != []:
        try:
            selection = Block_Selection[0]
            Game_State = gu.Tuple_To_Array(Game_State)
            FIRST_COLUMN = selection[0]
            FIRST_ROW = selection[1]
            SECOND_COLUMN = FIRST_COLUMN + 1
            SECOND_ROW = FIRST_ROW 
            A = Game_State[FIRST_COLUMN][FIRST_ROW]        
            B = Game_State[SECOND_COLUMN][SECOND_ROW]
            Game_State[FIRST_COLUMN][FIRST_ROW] = B
            Game_State[SECOND_COLUMN][SECOND_ROW] = A
            Game_State = gu.Array_To_Tuple(Game_State)
        except IndexError:
            print 'Right Block i: %d Right Block j: %d' % (SECOND_COLUMN,SECOND_ROW)
        return(Game_State)
    
    else:

        return Game_State

       

def check_time(TIME_BUFFER,GAME_TIME): #M

    """Takes the current time buffer and game time. Decrements
    the game time if one second has passed. Returns an updated
    game time."""

    if TIME_BUFFER >= TICK_INTERVAL:
       
       GAME_TIME -= 1
       TIME_BUFFER = 0

    return GAME_TIME,TIME_BUFFER


def increase_time(KILL_LIST,GAME_TIME): #M

    TIME_PARAMETER = len(KILL_LIST)
    TIME_BONUS = (SECONDS_GAINED * TIME_PARAMETER) 
    GAME_TIME += TIME_BONUS

    if GAME_TIME > MAX_TIME:

        GAME_TIME = MAX_TIME
    
    return GAME_TIME


def check_game_over(GAME_TIME): #M

    if GAME_TIME <= 0:

        pass #Replace this with call to view for gameover anim.

def handle_time_attack(time_buffer,game_time,kill_list):

    """IN:Int time_buffer,int game_time,nested array kill_list of all sprites
    cleared this cycle. OUT:Void. Updates all time parameters for the game."""

    game_time = increase_time(kill_list,game_time)
    time_buffer = update_time(time_buffer)
    game_time,time_buffer = check_time(time_buffer,game_time)
    check_game_over(game_time)

    return time_buffer,game_time

def handle_zone(current_progress,swap_request,kill_list):

    """IN:Int current progress, array swap request/kl. OUT:New current time.
    Decreases the progress if a successful swap is made and increases
    progress if matches are made."""

    current_progress = increase_time(kill_list,current_progress)
    current_progress = decrement_progress(swap_request,current_progress)

    return current_progress

    
def interpret_input(game_state,player_input): #M

    """IN:Nested tule g.s. and player input variable. OUT:Void. Performs
    the correct action in response to player input."""
    
    game_state = gu.Tuple_To_Array(game_state)
    if type(player_input) is tuple:

        game_state = improved_swap_blocks(game_state,player_input)
        return gu.Array_To_Tuple(game_state)
    
    if player_input is True:

        pygame.display.quit()
        pygame.quit()
        pdb.set_trace()
        return gu.Array_To_Tuple(game_state)
        
def check_swap_request(game_state,swap_request): #M
    
    """IN:Game state and array swap request. OUT:Boolean.
    Returns True if the swap request is legal. False otherwise."""
    
    if swap_request != [] and not_on_the_far_right(swap_request[0],game_state):
        column = game_state[swap_request[0]]
        next_column = game_state[swap_request[0] + 1]
        
        if not_clicking_white(game_state,swap_request) and real_swap_check(swap_request[1],column,next_column):

            return True
        else:

            return False
        
def generate_swap_verdict(game_state,swap_request): #M

    """IN:Game state and array swap_request. OUT: The coordinates of sprites
    that should be swapped with thier right neighbor and the destination cord
    of the sprite's right neighbor."""
    if swap_request != None:
        
        check = check_swap_request(game_state,swap_request)

        if check:

            return swap_request

        else:

            return None
    else:

        return None

def populate_buffer(game_state):
    
    game_state = gu.Tuple_To_Array(game_state)
    for column_index in gu.Array_Index(game_state):

        for row_index in gu.game_buffer:

            entry = game_state[column_index][row_index]

            if entry == gu.EMPTY:

                game_state[column_index][row_index] = random_color()

    else:

        return gu.Array_To_Tuple(game_state)

def request_sprites(game_state,column,column_index,column_sprite_request):
    
    for i in reversed(xrange(gu.TOP_PLAY_ROW - number_of_sprites_requested[column_index])):

        while column_sprite_request > 0:

            column[i] = random_color()
            entry = column[i]
            report_spawn([(column_index,i),entry])
            number_of_sprites_requested[column_index] += 1
            column_sprite_request -= 1
            break
    else:

        return column

def replenish_blocks(game_state,kill_list):
    
    game_state = gu.Tuple_To_Array(game_state)
    
    for column_index in gu.Array_Index(game_state):

        column = game_state[column_index]
        number_of_sprites_needed = len(pick_entries(column_index,kill_list))
        
        game_state[column_index] = request_sprites(game_state,column,column_index,number_of_sprites_needed)

    else:
        
        return gu.Array_To_Tuple(game_state)
    
def lower_spawn_points(drop_list,number_of_sprites_requested):

    for cord in drop_list:
        
        number_of_sprites_requested[cord[0]] -= 1
        if number_of_sprites_requested[cord[0]] < 0:
            number_of_sprites_requested[cord[0]] = 0
            

    










