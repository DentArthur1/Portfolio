class Dealer():

    def __init__(self):

        self.dealer_hand = []
        self.dealer_count = 0
        self.dealer_index = -1
        self.dealer_done = False
        

    def arrange_card(self, card_index, stock_pos = [425,86]): #600, 100

        if card_index != 0:
            stock_pos = stock_pos[0] - (card_index * 90), stock_pos[1]
        return stock_pos

    def display_dealer(self,dealer_index, dealer, spritesheet, card, screen, user_done, font, dealer_count):
        dealer_index += 1
        #Arranges the dealer cards on the screen 
        pos = dealer.arrange_card(dealer_index)
        #Shows the correct dealer count only when user has done its moves
        if user_done:
            dealer = font.render(f"{dealer_count}", False, (0,0,0))
            screen.blit(dealer,(521,57))
        #Checks if the index of the card is 0 and, if so, instead of blitting a card, it blits the back of one
        if dealer_index == 0 and user_done == False:
            spritesheet.blit_card(card, screen, pos[0],pos[1], True)
        else:
            spritesheet.blit_card(card, screen, pos[0], pos[1], False)
        return dealer_index

    