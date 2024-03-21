# game.py
from agent import Agent
from decks import Deck, GreenCards, RedCards


#TODO: Fix pop from empty list error

class Game:
    def __init__(self, num_players=3, max_score=3, green_cards=None, red_cards=None):
        self.running = True

        self.num_players = int(num_players)
        self.max_score = int(max_score)
        self.greenCards = Deck(green_cards)
        self.redCards = Deck(red_cards)
    
    def run(self):
        self.redCards.shuffle()

        players = []
        deal = 0

        for i in range(self.num_players):
            players.append(Agent())
        
        # All players draw 5 cards
        for player in players:
            player.draw_hand(self.redCards.get_cards())

        # Main game loop
        while (self.running):
            # Dealer draws a green card
            players[deal].draw_green_card(self.greenCards.get_cards())

            # Dealer Card
            print(f"Dealer's Card: {players[deal].get_green_card()}")
            
            # Each player plays a card
            for i in range(len(players)):
                if (i != deal):
                    players[i].green_card = players[deal].get_green_card()
                    print(f"{i+1}: {players[i].play_card()}")
                    players[i].draw_hand(self.redCards.get_cards(), 1)

                # Arbitrary Score (dealer should pick the best and award a point)
                players[i].score += 1

                if (players[i].score == self.max_score):
                    self.running = False
                
            # End of round
            deal = (deal+1) % len(players)

