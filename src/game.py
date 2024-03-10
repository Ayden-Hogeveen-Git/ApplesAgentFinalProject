# game.py
from agent import Agent
from decks import GreenCards, RedCards


class Game:
    def __init__(self):
        self.running = True
    
        self.greenCards = GreenCards()
        self.redCards = RedCards()

    def run(self):
        self.redCards.shuffle()

        players = []
        i = 1

        agent = Agent()
        dealer = Agent()
        
        players.append(agent)
        players.append(dealer)

        while (self.running):
            # Dealer draws a green card
            dealer.draw_green_card(self.greenCards.get_cards())

            # Each player draws a hand
            for player in players:
                player.draw_hand(self.redCards.get_cards())

            # Dealer Card
            print(f"Dealer's Card: {dealer.get_green_card()}")
            
            # Each player plays a card
            for player in players:
                print(f"{i}: {player.play_card()}")

                player.score += 1

                if (player.score == 5):
                    self.running = False
                    print("Game over")
                
                i += 1
            # End of round
            player.draw_hand(self.redCards.get_cards(), 1)
            i = 1


