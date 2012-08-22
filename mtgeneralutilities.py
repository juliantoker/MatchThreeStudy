import Utilities

EMPTY = 0 

HORIZONTAL_TILES = 6 
VERTICAL_TILES = 8 
BUFFER_MULT = 2 
TOP_PLAY_ROW = VERTICAL_TILES * (BUFFER_MULT - 1) 

TILE_VARIETY = len(Utilities.color_tuple) 

Array_Index = lambda Array: xrange(len(Array)) 
Array_To_Tuple = lambda Array: tuple([tuple(Array[column_index]) for column_index in Array_Index(Array)]) 
Tuple_To_Array = lambda Tuple: [list(Tuple[column_index]) for column_index in Array_Index(Tuple)] 
game_buffer = [buffer_entry for buffer_entry in reversed(xrange(TOP_PLAY_ROW))]

def Two_D_Nested_Iter(Nested_Array): 

    """IN:2D Array. OUT:Nested tuple containing the coordinates of all simple entries in the 2D nested array."""

    return [[i,j] for i in Array_Index(Nested_Array) for j in Array_Index(Nested_Array[i])]

def lowest_empty(column): 

    """IN: Column aray. OUT: Int. Returns
    the location of the lowest white space in the
    passed in column."""

    for i in reversed(Array_Index(column)):

        entry = column[i]
        if entry == EMPTY:

            return i

    else:

        return None 

def strip_zeroes(column): 

    """IN:Column. OUT: A column with all zeroes stripped off."""

    while column.count(EMPTY) > 0:

        column.remove(EMPTY)

    else:

        return column

def drop_lowest_to_bottom(game_state,drop_list): 

    """IN:Nested tuple or array g.s and nested tuple drop list.
    OUT: New game state.Moves game state entries
    specified by the drop list to the bottom of the g.s."""

    tuple_flag = 0
    
    if type(game_state) is tuple:
        game_state = Tuple_To_Array(game_state)
        tuple_flag = 1
        
    for cord in reversed(drop_list): 
        
        empty = lowest_empty(game_state[cord[0]])
        if empty != None and empty > cord[1]:
            game_state[cord[0]][empty]= game_state[cord[0]][cord[1]]
            game_state[cord[0]][cord[1]] = EMPTY

    else:
        
        if tuple_flag == 1:
            
            return Array_To_Tuple(game_state)
        else:

            return game_state

def Nested_List_Reverse(Nested_Array): 

    """IN:Nested array. OUT:Nested array. Reverses the nested elements of each array element within a 2-dimensional array"""

    Inverted_Array = []

    for element in [Nested_Array[column_index] for column_index in Array_Index(Nested_Array)]:

        element.reverse()
        Inverted_Array.append(element)

    else:

        return Inverted_Array

def Column_Clear(Game_State,Coordinate): 

    """IN: 2D nested Game_State tuple and coordinate tuple. Returns True if there are
    no empty spaces in the passed in coordinate's column. Returns False if there
    are empty spaces. Used to restict swaps and matches with falling columns."""
    
    COLUMN = Game_State[Coordinate[0]]
    for entry in Array_Index(COLUMN):

        CURRENT_ENTRY = COLUMN[entry]

        if entry >= TOP_PLAY_ROW and CURRENT_ENTRY == EMPTY:

            return False
            
    else:

        return True

def compress_column(column): 

    """IN:Column array. OUT:Compressed column."""
    
    bottom_entry = len(column) - 1
    column = list(column)
    
    for i in reversed(Array_Index(column)):
        
        entry = column[i]
        lil_empty = lowest_empty(column)
        
        if entry != EMPTY and i != bottom_entry: 

            column[lil_empty] = column[i]
            column[i] = EMPTY
    else:

        return column

if __name__ == '__main__':
    import ConfigParser as cp
    parser = cp.ConfigParser()
    parser.read('config.ini')
    print parser.get('pygame','screenWidth')
    
    
    
    
    
    
    
    
    
    