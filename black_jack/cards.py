

from random import randint
import re, pygame
class Cards():

    def __init__(self):
        #Initialize all deck values and makes a full deck made of n number of decks
        self.deck_number = 6
        self.splitter = re.compile("([A-Z]+)([0-9A-Z]+)")
        self.deck =["D10","D2","D3","D4","D5","D6","D7","D8","D9","DA","DJ","DK","DQ",
                    "H10","H2","H3","H4","H5","H6","H7","H8","H9","HA","HJ","HK","HQ",
                    "C10","C2","C3","C4","C5","C6","C7","C8","C9","CA","CJ","CK","CQ",
                    "S10","S2","S3","S4","S5","S6","S7","S8","S9","SA","SJ","SK","SQ",]
        self.decks = [card for card in self.deck for deck in range(self.deck_number)]
        self.shuffle_bool = True
        self.used_cards = []
        pygame.mixer.init()
        self.card_sound = pygame.mixer.Sound("data/sounds/cardSlide3.wav")
        self.shuflle_sound = pygame.mixer.Sound("data/sounds/shuffling-cards-1.wav")
        pygame.mixer.Sound.set_volume(self.shuflle_sound, 0.2)
        pygame.mixer.Sound.set_volume(self.card_sound, 0.2)

    def check_aces(self, count, aces):
        #Changes the value of the aces correspondly to user and dealer advantage
        if aces <= 1:
            if count + (aces * 11) > 21:
                count += 1
            else:
                count += aces * 11 
        else:
            if count + 11 + ((aces - 1) * 1) > 21: 
                count += aces
            else:
                count += 11 + ((aces - 1) * 1)
        return count
       

    def update_count(self, hand):
        #Formatting of the user hand
        split = [self.splitter.match(card).groups() for card in hand]
        count = 0
        aces = 0
        #loops through the splitted user hand to determine its value
        for card in split:
            if card[1] =="Q" or card[1] == "K" or card[1] =="J":
                count += 10
            elif card[1] == "A":
                aces += 1
            else:
                count += int(card[1])
        #Adds the correct value to the aces
        count = self.check_aces(count, aces)
        return count
    

    def shuffle_cards(self, decks = list):
        pygame.mixer.Sound.play(self.shuflle_sound)
        #Changes the index of each card in the full deck to a random one, and repeats the same progress n times to ensure randomness
        for n in range(0, len(decks) -1):
            for card in decks:
                decks.insert((randint(0,len(decks))), decks.pop(randint(0,len(decks) - 1))) #inserts in random position de card popped from the for loop
        return decks
        
    def check_deck(self,decks, used_cards):
        #Checks the health of the deck, shuffling at half and replenishing at minus 20 cards left
        if len(decks) == 150:
            decks = self.shuffle_cards(decks)

        if len(decks) <= 20:
            decks += self.used_cards
            decks = self.shuffle_cards(self.decks)
            used_cards = []
        return decks, used_cards
    
    def hit(self, hand, count):
             #Adds a card to the user hand and updates the user count
             pygame.mixer.Sound.play(self.card_sound)

             self.decks, self.used_cards = self.check_deck(self.decks, self.used_cards)
             card = self.decks.pop(0)
             hand.append(card)
             self.used_cards.append(card)
             count = self.update_count(hand)
             return hand, count

    def begin(self, hand, count):
        
        for n in range(0,2,1):
             hand, count = self.hit(hand, count)

        return hand, count

    