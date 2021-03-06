import pygame,random,Utilities,math,pdb,modelutilities as mu,  mtgeneralutilities as gu
from threading import Timer
from pygame.locals import *
pygame.init()

class model():

    def __init__(self):

        self.game_state = mu.Game_State
        self.game_state = mu.fill_buffer(self.game_state)
        self.MAX_TIME = mu.MAX_TIME
        self.GAME_TIME_LENGTH = mu.GAME_TIME_LENGTH
        self.TIME_BUFFER = mu.TIME_BUFFER
        self.score = 0
        self.combo_number = 0
        
    def update(self,view_input_tuple):

        """IN:Player input constant, nested drop_list array
        containing the cords of all sprites who reaches their
        destinations last view cycle. OUT:Game state,spawn_list,
        kill_list,swapped_blocks,time,score,paused or not. Supplies
        the view with the information it needs."""

        player_input = view_input_tuple[0]
        drop_list = view_input_tuple[1]
        swap_list = view_input_tuple[2]
        swap_request = view_input_tuple[3]
        
        mu.spawn_report = []
        self.game_state = gu.drop_lowest_to_bottom(self.game_state,drop_list)
              
        self.kill_list = mu.find_matches(self.game_state)
        self.game_state = mu.destroy_matches(self.game_state,self.kill_list)
        mu.lower_spawn_points(drop_list,mu.number_of_sprites_requested)
        self.game_state = mu.replenish_blocks(self.game_state,self.kill_list)
           
        self.game_state = mu.improved_swap_blocks(self.game_state,swap_list)
        self.combo_number = mu.determine_combo(self.kill_list,swap_request,self.combo_number,self.game_state)
        
        self.score += mu.tally_score(self.kill_list)
        #self.GAME_TIME_LENGTH = mu.handle_zone(self.GAME_TIME_LENGTH,swap_list,self.kill_list)
        self.TIME_BUFFER,self.GAME_TIME_LENGTH = mu.handle_time_attack(self.TIME_BUFFER,self.GAME_TIME_LENGTH,self.kill_list)
        self.swap_verdict = mu.generate_swap_verdict(self.game_state,swap_request)
        mu.quota_array,mu.level = mu.try_level_up(mu.quota_array,mu.level)
        return(self.kill_list,self.swap_verdict,mu.spawn_report,self.MAX_TIME,self.GAME_TIME_LENGTH,self.score,mu.quota_array)
        

































