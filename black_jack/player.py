
import pygame

class Player():

    def __init__(self):
        

        self.user_hands = []
        self.user_count = 0
        self.user_balance = 2500
        self.user_bet = 0
        self.player_index = -1
        self.done = False


    def arrange_card(self, player_index, stock_pos): #hand_lenght = 0
        
        stock_pos = stock_pos[0] + (17 * player_index), stock_pos[1] - (17 * player_index)
        return stock_pos

    def display_player(self, player_index, player, spritesheet, card, screen, font, user_count, user_bet, user_balance):
        player_index += 1
        #Displays all the indicators concerning the player on the screen: Cards, count, bet, balance
        pos = player.arrange_card(player_index,[230,400])      
        spritesheet.blit_card(card, screen, pos[0], pos[1], False)
        count = font.render(f"{user_count}", True, (0,0,0))
        bet = font.render(f"Bet: {user_bet}", True, (0,0,0))
        balance = font.render(f"Money: {user_balance}", True, (0,0,0))
        screen.blit(count,(180,493)), screen.blit(bet,(460,490)), screen.blit(balance ,(460,525))
        return player_index


    def limit_decisions(self, decisions, hand, count, rects, done):  
        #Limit the decisions of the player base on the hand charateristics
        if len(hand) >= 3:
            if "Double" in decisions:
                    decisions.remove("Double")
                    del rects[2]
        if count >= 21:
            rects = []
            decisions = [] 
            done = True  
        #If the user has done its moves, appends the New hand button to the list of active rects
        if done == True:
            if "New hand" not in decisions:
                decisions.append("New hand")
                rects.append(["/", False])
        return decisions, rects, done
          
    def double(self, user_bet, user_balance):
        #Basically the same as hitting except the user doubles his bet and can't make any moves anymore
        rects =[]
        decisions = []
        done = True
        user_bet *= 2
        user_balance -= user_bet / 2
        user_balance = int(user_balance)  #Truncate decimals to the user balance
        return rects, decisions, done, user_bet, user_balance
     
        
    def stand(self):
        rects =[]
        decisions = []
        done = True
        return rects, decisions, done

        
        

