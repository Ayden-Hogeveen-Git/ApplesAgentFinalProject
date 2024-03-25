# Takes a card datatype as input and outputs a card datatype
import random
from card import Card
import nltk
import re
from decks import RedCards  # Demo purposes ONLY
# nltk.download()  # uncomment then run to manage nltk packages



# Represents the game agent
class Agent:
    def __init__(self, agent_type="random", is_dealer=False):
        self.hand = []

        self.agent_type = agent_type
        self.score = 0

        self.is_dealer = is_dealer
        self.green_card = None

    def judge(self, cards):
        """
        Judges the cards of the other players
        :param cards: list of tubles including index and card datatype
        :return: int (index of the winning player)
        """
        best_card = cards[0][0]
        temp = nltk.edit_distance(self.green_card, cards[0][1])
        for i in range(1, len(cards)):
            if (temp > nltk.edit_distance(self.green_card, cards[i][1])):
                best_card = cards[i][0]
                temp = nltk.edit_distance(self.green_card, cards[i][1])
        return best_card           
            

    def play_card(self):
        """
        Plays a card from the agent's hand
        :return: card datatype
        """
        if (self.agent_type == "random"):
            return self.hand.pop(0)
        elif (self.agent_type == "assoc"):
            return self.play_associated_card()
        elif (self.agent_type == "pos"):
            return self.play_card_pos()

    def play_associated_card(self):
        """
        Plays a card from the agent's hand based on the word association
        :return: card datatype
        """
        card_scores = []
        for i in range(len(self.hand)):
            card_scores.append(nltk.edit_distance(self.green_card, self.hand[i]))
        
        return self.hand.pop(card_scores.index(max(card_scores)))


    def play_card_pos(self):
        """
        Plays a card from the agent's hand based on similar parts of speech
        :return: card datatype
        """
        tags = self.get_pos_tags()
        
        if (self.green_card is not None):
            target = nltk.pos_tag([self.green_card])
                        
            for tag in tags:
                if (target == tag[0][1]):
                    return self.hand.pop(tags.index(tag))
                
        return self.hand.pop(0)
    
    def draw_hand(self, deck, num_cards=7):
        """
        Draws a hand from the deck
        :param deck: list of card datatype
        :return: None
        """
        for i in range(num_cards):
            self.add_card(deck.pop(0))

    def demo_red_card(self):
        all_red_cards = RedCards().cards
        first_letter = self.green_card[0]
        for i in range(len(all_red_cards)):
            if all_red_cards[i][0] == first_letter:
                return all_red_cards[i]

    def draw_green_card(self, deck):
        """
        Draws a green card from the deck
        :param deck: list of card datatype
        :return: None
        """
        self.green_card = deck.pop(0)
    
    def get_green_card(self):
        """
        Returns the green card
        :return: card datatype
        """
        return self.green_card

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

    def get_hand_size(self):
        """
        Returns the size of the agent's hand
        :return: int
        """
        return len(self.hand)

    def __str__(self):
        """
        Overloads the str method to return the agents hand when printed
        :return: string
        """
        string = "Hand: "
        for card in self.hand:
            string += "\n" + str(card)
        return string


# p1 = Agent()  # arg1<agent_type>, arg2<is_dealer>
# print(p1.database)  # prints full list of all green cards (nouns)
""" This whole main is for demo purposes ONLY. """
if __name__ == "__main__":
    print("Part 1) Let's select a green card from the database and let the agent choose the ""best"" red one:")
    p1 = Agent()
    random.shuffle(p1.database)
    p1.draw_green_card(p1.database)
    print("Here is our green card: {}".format(p1.get_green_card()))
    print("Agent's Turn...")
    print(p1.demo_red_card())
    userInput = input("Part 2) Enter a green card (noun): ")  # assumes a valid input
    p2 = Agent()
    p2.green_card = userInput
    print("Agent's Turn...")
    print(p2.demo_red_card())