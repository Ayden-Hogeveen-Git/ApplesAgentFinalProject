# game.py
from agent import Agent
from decks import GreenCards, RedCards


class Game:
    def __init__(self):
        self.running = True

        self.max_score = 3
    
        self.greenCards = GreenCards()
        self.redCards = RedCards()

    def run(self):
        self.redCards.shuffle()

        players = []
        deal = 0

        agent1 = Agent("pos")
        agent2 = Agent()
        agent3 = Agent()
        
        players.append(agent1)
        players.append(agent2)
        players.append(agent3)

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

                # Arbitrary Score (dealer should pick the best and award a point)
                players[i].score += 1

                if (players[i].score == self.max_score):
                    self.running = False
                
            # End of round
            player.draw_hand(self.redCards.get_cards(), 1)
            deal = (deal+1) % len(players)

