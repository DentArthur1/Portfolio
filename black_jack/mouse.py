
import pygame
class Mouse():

    def __init__(self):

       
        self.cursor_img = pygame.image.load("data/backgrounds/cursor.png")
        self.pointer_img = pygame.image.load("data/backgrounds/pointer.png")
    

    def blit_cursor(self, screen, bool):
        pygame.mouse.set_visible(False)
        #Handles the mouse hovering and changes the pointer icon correspondly
        x,y = pygame.mouse.get_pos()
        if bool:
               screen.blit(self.pointer_img, (x,y))
        else:
            screen.blit(self.cursor_img, (x,y))
    
