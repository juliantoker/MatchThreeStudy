import pygame, viewutilities as vu, mtgeneralutilities as gu

class view():

    def __init__(self,game_state):

        vu.init_view_spawn(game_state,vu.spriteList)

    def update(self,model_input_tuple):

        vu.spritesAtYDest = []
        vu.spritesAtXDest = []
        
        self.kill_list = model_input_tuple[0]
        self.swap_verdict = model_input_tuple[1]
        self.spawn_list = model_input_tuple[2]
        self.max_time = model_input_tuple[3]
        self.game_time = model_input_tuple[4]
        self.score = model_input_tuple[5]
        self.quota_array = model_input_tuple[6]
        
        vu.engage_locks(self.kill_list)
        
        vu.add_sprites(self.spawn_list,vu.spriteList)
        vu.remove_tiles(self.kill_list,vu.spriteList)
        vu.assign_destinations(vu.spriteList)
        vu.assign_xdest(self.swap_verdict,vu.spriteList)
        
        vu.render(vu.spriteList,self.score,self.max_time,self.game_time,self.quota_array)
        
        vu.spriteList = gu.drop_lowest_to_bottom(vu.spriteList,vu.spritesAtYDest)
        vu.rectify_sprite_array(vu.spriteList)

        
        self.inputs = vu.check_for_input(vu.spriteList)
        self.swap_request = vu.lock_check(self.inputs[0],vu.locks)        
        self.other_input = self.inputs[1]
        
        return (self.other_input,vu.spritesAtYDest,vu.spritesAtXDest,self.swap_request)
