import pygame


class Buttons():

    def __init__(self):

         pass

    def draw_text(self, screen, x, y, text):
        # Draws the choice on the screen with his rect
        screen.blit(text, (x,y))
        text_rect = text.get_rect()
        text_rect.center = x + (text_rect[2] / 2), y + (text_rect[3] / 2)
        return text_rect
      
    def update_collisions(self, rect, n, choice_rects, choices):
        #Update the mouse hovering collisions on the buttons triggered by the user
        choice_rects[choices.index(n)][0], choice_rects[choices.index(n)][1] = rect, rect.collidepoint(pygame.mouse.get_pos())
        return choice_rects

    def detect_collision(self, choice_rects = list):
        #checks if there have been collisions with buttons
        if any(True in sl for sl in choice_rects):
               mouse_bool = True
        else:
               mouse_bool = False
        return mouse_bool


    def arrange_text(self, text_index, stock_pos, done):
        #Arranges the text on the screen
        if text_index >= 1:
            stock_pos[1] += 40 * text_index
        if done:
            stock_pos = [225, 565]
        return stock_pos

    def arrange_chips(self, chip, chips):
        #Arrange chip imgs on the screen
        stock_pos = [90,180]
        if 1 <= chips.index(chip) <= 3:
            stock_pos[0] += (130 * chips.index(chip))
        if 4 <= chips.index(chip) <= 6:
            stock_pos[1], stock_pos[0] = 335, stock_pos[0] + (130 * (chips.index(chip) - 3))
        return stock_pos




    def display_choices(self, choices,choice_rects, n, font, screen, done):
             
        
       text_pos = self.arrange_text(choices.index(n),[23,400], done)
       text = font.render(choices[choices.index(n)], True, (0,0,0))
       text_rect = self.draw_text(screen, text_pos[0],text_pos[1], text)
       choice_rects = self.update_collisions(text_rect, n, choice_rects, choices)
       return choice_rects

  