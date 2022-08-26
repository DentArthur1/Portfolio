
import pygame 
class Chips():

    def __init__(self):
        self.chips = [1,5,20,50,100,500]
        self.chips_img = [pygame.image.load(chip) for chip in ["data/chips/white.png","data/chips/blue.png","data/chips/pink.png","data/chips/purple.png","data/chips/yellow.png","data/chips/red.png",]]
        self.chips_scaled = [pygame.transform.scale(chip,(60,60)) for chip in self.chips_img]
        self.chips_rect = [["/", False],["/", False],["/", False],["/", False],["/", False],["/", False]]
        self.bet_bg = pygame.image.load("data/backgrounds/betting.png")
        self.chip_op_bool = True
        self.init_bet = True
        pygame.font.init()
        self.balance_font = pygame.font.Font("data/fonts/LCALLIG.ttf", 30)
        self.ready = self.balance_font.render("Ready?", True, (0,0,0))
        self.ready_rect = self.ready.get_rect()
        self.ready_rect.center = 400 + self.ready.get_width() - 15 ,400 + self.ready.get_height() / 2



    def display_chips(self, buttons , chip_imgs, screen, chip_rects):
        for chip in chip_imgs:
            pos = buttons.arrange_chips(chip, chip_imgs)
            screen.blit(chip, (pos[0], pos[1]))
            chip_rect = chip.get_rect()
            chip_rect.center = pos[0] + chip.get_width() / 2 , pos[1] + chip.get_height() / 2
            self.chips_rect = buttons.update_collisions(chip_rect, chip, chip_rects, chip_imgs)




    def bet_sequence(self, screen, user_balance, buttons, mouse_bool, mouse, running):
        betting = True
        user_bet = 0
        while betting:
            screen.blit(self.bet_bg,(0,0))
         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    betting = False
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    for rect in self.chips_rect:
                        #adds the correct amount of money to user bet correspondly to the chip selected
                        if rect[0].collidepoint(pygame.mouse.get_pos()):
                            value = int(self.chips[self.chips_rect.index(rect)])
                            if user_balance - int(value) >= 0:
                                user_bet += int(value)
                                user_balance -= int(value)
                    #Checks if ready has been clicked on    
                    if self.ready_rect.collidepoint(pygame.mouse.get_pos()):
                        if user_bet > 0:
                             betting = False
                            
    
            #displays balance and bet of the user
            balance = self.balance_font.render(f"{user_balance}", True, (0,0,0))
            bet = self.balance_font.render(f"{user_bet}", True, (0,0,0))

            #blit chips
            self.display_chips(buttons,self.chips_scaled, screen, self.chips_rect)
            #blit balance, bet and ready button   
            screen.blit(balance, (500, 542)), screen.blit(bet, (500,478)), screen.blit(self.ready,(450,400))

            #mouse movement and hovering handling
            mouse_bool = buttons.detect_collision(self.chips_rect)
            if self.ready_rect.collidepoint(pygame.mouse.get_pos()): 
                mouse_bool = True
            mouse.blit_cursor(screen, mouse_bool)
            pygame.display.update()

        chip_bool = True     
        return user_bet, user_balance, chip_bool, running

    def money_operator(self, user_bet, user_balance, chip_bool, case):
        #divides each ending case and handles user bet correspondly
        if chip_bool:
            if case == 0: # loss
               pass
            elif case == 1: #regular victory
                user_balance += user_bet * 2
            elif case == 2: #bj
                user_balance += user_bet * 2.5
            else:
                user_balance += user_bet #draw
            chip_bool = False
        #replenishes user balance if he/she runs out of cash
        if user_balance == 0: 
            user_balance = 2500
       
        user_balance = int(user_balance)
        return user_bet, user_balance, chip_bool

            