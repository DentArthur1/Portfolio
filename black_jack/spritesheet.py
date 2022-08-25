
import pygame

from xml.etree import ElementTree

class Spritesheet():

    def __init__(self, filename):
        
        self.filename = filename
        self.spritesheet = pygame.image.load(filename).convert()


    def load_xml(self):
       data = ElementTree.parse("spritesheet/sprite.xml")
       return data

    def search_card(self, card):
        #Loads the xml file 
        data = self.load_xml()
        #Searches all the attributes of the card with the string given
        card_x = int(data.find(card).attrib.get("x"))
        card_y = int(data.find(card).attrib.get("y"))
        card_width = int(data.find(card).attrib.get("w"))
        card_height = int(data.find(card).attrib.get("h"))
        return card_x, card_y, card_width, card_height

        #returns all the values of the card


    def blit_card(self, card, screen, loc_x, loc_y, bool):
        #In case the bool value is true, the function gives the values for the red back png of a card
        #x, y, width, height give all the coordinates necessary to crop the correct part of the spritesheet file and give exactly one card
        if bool:
            x, y, width, height = 848, 453, 75, 113
        else:
            x, y, width, height = self.search_card(card)
           
        image = pygame.Surface((width, height))
        image.set_colorkey((0,0,0))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        screen.blit(image, (loc_x, loc_y))
        return image

