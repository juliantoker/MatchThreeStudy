import MatchThreeModel as model, view, pygame
from pygame.locals import *

class controller():

    def __init__(self):

        self.model = model.model()
        self.view = view.view(self.model.game_state)
        self.view_output = self.view.update(([],None,[],self.model.MAX_TIME,self.model.GAME_TIME_LENGTH,0))

    def update(self):

       self.model_output = self.model.update(self.view_output)
       self.view_output = self.view.update(self.model_output)

k = controller()

while True:
    
    k.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            pygame.quit()
    
