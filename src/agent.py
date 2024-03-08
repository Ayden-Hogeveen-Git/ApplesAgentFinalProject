# Takes a card datatype as input and outputs a card datatype
from card import Card
import nltk
import re


database = "Apple,Banana,Table,Chair,Sun,Moon,Cat,Dog,River,Mountain,Computer,Phone,Book,Car,Music,Art,Water,Fire,Earth,Air,Pizza,Coffee,Tea,Shoe,Hat,Guitar,Soccer,Basketball,Football,Swimming,Running,Dancing,Singing,Painting,Drawing,Writing,Reading,Eating,Sleeping,Dreaming,Laughing,Crying,Happiness,Sadness,Anger,Love,Friendship,Family,Work,School,Holiday,Vacation,Beach,Forest,Park,City,Country,Bridge,House,Building,Skyscraper,Tower,Train,Plane,Boat,Bike,Helmet,Glasses,Camera,Microphone,Clock,Watch,Mirror,Window,Door,Key,Lock,Pen,Pencil,Paper,Notebook,Marker,Highlighter,Scissors,Tape,Glue,Ruler,Calculator,Money,Wallet,Bag,Backpack,Suitcase,Jacket,Sweater,Scarf,Gloves,Hat,Boots,Socks,Jeans,Dress,Shirt,T-shirt,Skirt"


# Represents the game agent
class Agent:
    def __init__(self):
        self.database = self.tokenize(database)
        self.hand = []

    def play_card(self):
        """
        Plays a card from the agent's hand
        :return: card datatype
        """
        return self.hand.pop(0)
    
    def draw_hand(self, deck):
        """
        Draws a hand from the deck
        :param deck: list of card datatype
        :return: None
        """
        for i in range(5):
            self.add_card(deck.pop(0))

    def add_card(self, card):
        """
        Adds a card to the agent's hand
        :param card: card datatype
        :return: None
        """
        self.hand.append(card)

    def tokenize(self, text):
        """
        Splits the inputted string into the individual words, this function will be used to split a training set into tokens
        :param text: string
        :return: list of strings
        """
        return re.findall(r'\b\w+\b', text)  # Uses a regular expression to split the string into words
    
    def get_pos_tags(self):
        """
        Returns the part of speech tags for the agent's hand
        :return: list of strings
        """
        pos_tags = []
        for card in self.hand:
            pos_tags.append(nltk.pos_tag([card]))
        return pos_tags

    def get_database(self):
        """
        Returns the database of words
        :return: list of strings
        """
        return self.database

    def __str__(self):
        """
        Overloads the str method to return the agents hand when printed
        :return: string
        """
        string = "Hand: "
        for card in self.hand:
            string += "\n" + str(card)
        return string
