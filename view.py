import pygame, viewutilities as vu, mtgeneralutilities as gu

class view():

    def __init__(self,game_state):

        vu.init_view_spawn(game_state,vu.sprite_array)

    def update(self,model_input_tuple):

        vu.sprites_at_dest = []
        vu.sprites_at_xdest = []
        
        self.kill_list = model_input_tuple[0]
        self.swap_verdict = model_input_tuple[1]
        self.spawn_list = model_input_tuple[2]
        self.max_time = model_input_tuple[3]
        self.game_time = model_input_tuple[4]
        self.score = model_input_tuple[5]
        
        vu.engage_locks(self.kill_list)
        
        vu.add_sprites(self.spawn_list,vu.sprite_array)
        vu.remove_tiles(self.kill_list,vu.sprite_array)
        vu.assign_destinations(vu.sprite_array)
        vu.assign_xdest(self.swap_verdict,vu.sprite_array)
        vu.render(vu.sprite_array)

        vu.sprite_array = gu.drop_lowest_to_bottom(vu.sprite_array,vu.sprites_at_dest)
        vu.rectify_sprite_array(vu.sprite_array)

        
        self.inputs = vu.check_for_input(vu.sprite_array)
        self.swap_request = vu.lock_check(self.inputs[0],vu.locks)        
        self.other_input = self.inputs[1]
        
        return (self.other_input,vu.sprites_at_dest,vu.sprites_at_xdest,self.swap_request)
