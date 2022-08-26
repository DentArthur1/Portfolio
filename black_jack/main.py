

import pygame
from spritesheet import *
from player import Player
from cards import *
from dealer import *
from buttons import *
from mouse import *
from chips import *





class Main():

    def __init__(self):
        # init of all the values and classes from other files
        self.width = 600
        self.height = 600
        self.FPS = 75
        self.bg = pygame.image.load("data/backgrounds/bg.png")
        self.start = True
        self.clock = pygame.time.Clock()
        self.icon = pygame.image.load("data/backgrounds/card.png")
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.running = True
        self.player = Player()
        self.cards = Cards()
        self.dealer = Dealer()
        self.buttons = Buttons()
        self.chips = Chips()
        self.spritesheet = Spritesheet("data/spritesheet/spritesheet.png")
        self.mouse = Mouse()
        self.mouse_bool = False
        pygame.font.init()
        self.my_font = pygame.font.Font("data/fonts/LCALLIG.ttf", 25)
        self.count_font = pygame.font.Font("data/fonts/LCALLIG.ttf", 20)
        self.choices = ["Hit" , "Stand", "Double"]
        self.choice_rects = [["/", False],["/", False],["/", False]]
        self.messages = ["You busted!", "Blackjack!", "You lose!", "You win!", "You both busted!", "Draw"]
        self.messages_font = [self.my_font.render(message, True, (0,0,0)) for message in self.messages]
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("BlackJack")
        pygame.mixer.init()
    

    def get_new_hand(self):
        #Called everytime we want to make a new game
        user_hand, user_count, dealer_hand, dealer_count, choices, rects,start, done = [],0,[],0,["Hit" , "Stand", "Double"], [["/", False],["/", False],["/", False]], True, False
        return user_hand, user_count, dealer_hand, dealer_count, choices, start, rects, done

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                        #handles mouse input events by the user
                        for rect in self.choice_rects:
                                if  rect[0].collidepoint(pygame.mouse.get_pos()):
                                    if self.choices[self.choice_rects.index(rect)] == "Hit":
                                        self.player.user_hands, self.player.user_count = self.cards.hit(self.player.user_hands, self.player.user_count)
                                    elif self.choices[self.choice_rects.index(rect)] == "Stand":
                                        self.choices, self.choice_rects,self.player.done = self.player.stand()
                                    elif self.choices[self.choice_rects.index(rect)] == "Double":
                                        self.player.user_hands, self.player.user_count = self.cards.hit(self.player.user_hands, self.player.user_count)
                                        self.choices, self.choice_rects,self.player.done, self.player.user_bet, self.player.user_balance = self.player.double(self.player.user_bet, self.player.user_balance)
                                    else:
                                        #This is in case the user pressed the "New hand" button at the end of a game
                                         self.player.user_hands, self.player.user_count, self.dealer.dealer_hand, self.dealer.dealer_count, self.choices, self.start, self.choice_rects, self.player.done = self.get_new_hand()
                                         self.player.user_bet, self.player.user_balance, self.chips.chip_op_bool, self.running =  self.chips.bet_sequence(self.screen,self.player.user_balance,self.buttons, self.mouse_bool, self.mouse, self.running)
                                         
                                        

                        self.choices,self.choice_rects,self.player.done = self.player.limit_decisions(self.choices,self.player.user_hands, self.player.user_count,self.choice_rects, self.player.done)

       
                    
             
        self.player.player_index, self.dealer.dealer_index = -1, -1 # to prevent buggy blitting of same value and sign cards
        
    
    def check_victory(self, user_count, dealer_count):
        case = 0
        #divides each ending case and draws the corresponding message on the screen
        if user_count == 21:
                self.screen.blit(self.messages_font[1], (400,360))
                case = 2
        elif dealer_count <= 21 and user_count <= 21: 
            if dealer_count > user_count:
                self.screen.blit(self.messages_font[2], (400,360))
            elif dealer_count < user_count:
                self.screen.blit(self.messages_font[3], (400,360))
                case = 1
            else:
                self.screen.blit(self.messages_font[5], (400,360))
                case = 3
        elif user_count <= 21 and dealer_count > 21:
            self.screen.blit(self.messages_font[3], (400,360))
            case = 1
        else:
            self.screen.blit(self.messages_font[0], (400,360))
        return case


        
      
    def start_game(self, start_bool, shuffle_bool):
            if start_bool:
               #This is for the one time shuffle at the start of the game
               if shuffle_bool:
                        self.cards.decks = self.cards.shuffle_cards(self.cards.decks)
                        shuffle_bool = False
               #initializes each hand and displays the possible decisions
               self.player.user_hands, self.player.user_count = self.cards.begin(self.player.user_hands, self.player.user_count)
               self.dealer.dealer_hand, self.dealer.dealer_count = self.cards.begin(self.dealer.dealer_hand, self.dealer.dealer_count)
               self.choices,self.choice_rects,self.player.done = self.player.limit_decisions(self.choices, self.player.user_hands, self.player.user_count, self.choice_rects,self.player.done)
               start_bool = False
            return start_bool, shuffle_bool

            

        
    def main_loop(self):
        while self.running:

            self.screen.blit(self.bg,(0,0))
            self.handle_events()
            # Initialize betting sequence on first start of the game 
            if self.chips.init_bet:
                  self.player.user_bet, self.player.user_balance, self.chips.chip_op_bool,self.running =  self.chips.bet_sequence(self.screen,self.player.user_balance,self.buttons, self.mouse_bool, self.mouse, self.running)
                  self.chips.init_bet = False
            if self.running == False: #To brevent buggy closing
                break
            # GIVE PLAYER AND DEALER THE CARDS and SHUFFLES
            self.start, self.cards.shuffle_bool = self.start_game(self.start, self.cards.shuffle_bool)
        
            #Start dealer moves if player has finished
            if self.player.done:
                if self.dealer.dealer_count < 17:
                    self.dealer.dealer_hand, self.dealer.dealer_count = self.cards.hit(self.dealer.dealer_hand, self.dealer.dealer_count)
                case = self.check_victory(self.player.user_count, self.dealer.dealer_count)
                self.player.user_bet,self.player.user_balance, self.chips.chip_op_bool = self.chips.money_operator(self.player.user_bet,self.player.user_balance, self.chips.chip_op_bool, case)

            #UPDATE USER AND HAND and various indicators
            for card in self.player.user_hands:
                        self.player.player_index = self.player.display_player(self.player.player_index, self.player, self.spritesheet, card, self.screen, self.count_font, self.player.user_count, self.player.user_bet, self.player.user_balance)

            for card in self.dealer.dealer_hand:
                        self.dealer.dealer_index = self.dealer.display_dealer(self.dealer.dealer_index,self.dealer, self.spritesheet, card, self.screen,self.player.done,self.count_font, self.dealer.dealer_count)


            #render choices and draws them on the screen 
            for n in self.choices:
                self.buttons.display_choices(self.choices, self.choice_rects, n, self.my_font, self.screen,self.player.done)
         
     
            self.mouse_bool = self.buttons.detect_collision(self.choice_rects)
            self.mouse.blit_cursor(self.screen, self.mouse_bool)
            self.clock.tick(self.FPS)
        
            pygame.display.update()



game = Main()
game.main_loop()