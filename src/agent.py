# Takes a card datatype as input and outputs a card datatype
from card import Card


# Represents the game agent
class Agent:
    def __init__(self, hand):
        self.hand = hand

    def play_card(self):
        return self.hand.pop(0)

    def add_card(self, card):
        self.hand.append(card)

    def __str__(self):
        return str(self.hand)
