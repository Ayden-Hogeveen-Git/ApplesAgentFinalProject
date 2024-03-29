# game.py
from agent import Agent
from decks import Deck, GreenCards, RedCards
from random import randint


class Game:
    def __init__(self, num_players=3, max_score=3, green_cards=None, red_cards=None):
        self.running = True

        self.num_players = int(num_players)
        self.max_score = int(max_score)
        self.greenCards = Deck(green_cards)
        self.redCards = Deck(red_cards)
    
    def run(self, players=[]):
        self.redCards.shuffle()

        cards_on_table = []
        deal = randint(0, 3)
        x = 0

        if (players == []):
            for i in range(self.num_players):
                players.append(Agent("assoc"))
        
        # All players draw 7 cards
        for player in players:
            player.draw_hand(self.redCards.get_cards())

        # Main game loop
        while (self.running):
            # Dealer draws a green card
            players[deal].draw_green_card(self.greenCards.get_cards())

            # Dealer Card
            # print(f"Dealer's Card: {players[deal].get_green_card()}")
            
            # Each player plays a card
            for i in range(len(players)):
                if (i != deal):
                    players[i].green_card = players[deal].get_green_card()

                    card_played = players[i].play_card()
                    cards_on_table.append((i, card_played))

                    # print(f"{i+1}: {card_played}")
                    players[i].draw_hand(self.redCards.get_cards(), 1)

            # Judge the cards
            x = players[deal].judge(cards_on_table)
            players[x].score += 1
            cards_on_table = []


            # Check if a player has reached the max score
            for i in range(len(players)):
                if (players[i].score == self.max_score):
                    print(f"Player {i+1} wins!")
                    self.running = False

            # Print the scores
            # print("-"*32)
            # for i in range(len(players)):
            #     print(f"Player {i+1}: {players[i].score}")
                
            # End of round
            deal = (deal+1) % len(players)
        return i

