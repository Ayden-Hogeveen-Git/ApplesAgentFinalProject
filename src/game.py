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
    
    def run(self, players=None):
        # No players are given make it into a list of
        # containing num_players amount of Agent("assoc")
        if players is None:
            players = []
            
            for _ in range(self.num_players):
                players.append(Agent("assoc"))

        # Shuffle green & red cards
        self.redCards.shuffle()
        self.greenCards.shuffle()

        # Invisible dealer entity draws 7 red cards for each player
        for player in players:
            player.draw_hand(self.redCards.get_cards(), 7)

        # Determine first judge
        judge = randint(0, self.num_players-1)

        # Game loop
        game_round = 1
        while (self.running):
            print(f"\nRound {game_round}")

            # Dealer puts green card on the table
            green_card = self.greenCards.get_cards().pop()

            # Set up area to put the players red cards in
            player_card_picks = []

            # Players make their choices
            for player in range(self.num_players):
                # Set each players green_card to the drawn green card
                players[player].green_card = green_card

                # Skip the judge picking a red card
                if player == judge:
                    continue
                
                # Make each player choose a card by putting it on the table
                # Drawing card here does the same thing as drawing it
                # after the judge makes a decision.

                # player_card_picks contains tuples of cards played by a player
                # -> (player number, card)
                player_card_picks.append((player, players[player].play_card()))
                players[player].draw_hand(self.redCards.get_cards(), 1)

            # Judge makes a decision then resets the player card area
            winner = players[judge].judge(player_card_picks)
            players[winner].score += 1
            player_card_picks = []

            # Print the scores
            for i in range(self.num_players):
                print(f"Player {i+1}'s score: {players[i].score}")

            # Check if a player has reached the max score
            for i in range(self.num_players):
                if (players[i].score == self.max_score):
                    print(f"\nPlayer {i+1} wins!")
                    self.running = False

            # Judge will be next player
            judge = (judge+1) % self.num_players
            
            game_round += 1 
            
        return None
