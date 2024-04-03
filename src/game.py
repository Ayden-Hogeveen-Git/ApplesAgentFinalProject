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
        model_player = randint(0, self.num_players-1)

        if players is None:
            players = []
            
            for i in range(self.num_players):
                if (i == model_player):
                    players.append(Agent("model_training"))
                    continue

                # players.append(Agent("assoc"))
                # Change players to model_training
                players.append(Agent("model_training"))

        # Shuffle green & red cards
        self.redCards.shuffle()
        self.greenCards.shuffle()

        # Invisible dealer entity draws 7 red cards for each player
        for player in players:
            player.draw_hand(self.redCards.get_cards(), 7)

        # Determine first judge
        judge = randint(0, self.num_players-1)
        
        # Game loop
        print(f"\nModel player: Player {model_player+1}")
        print(f"There are a total of {self.num_players} players in this game\n")

        while (self.running):
            print("---------------NEW ROUND------------------")
            player_type = "player" if judge != model_player else "judge"
            print(f"Model player (#{model_player+1}) is playing as a: {player_type}")

            print("\nModel player cards in hand:")
            for i, card in enumerate(players[model_player].hand):
                print(f"Card {i+1}: {card.name} - {card.description}")

            model_player_play = None
            model_player_new_card = None

            # Judge puts green card on the table
            green_card = self.greenCards.get_cards().pop()

            print(f"\nGreen card from judge: {green_card.name} - {green_card.description}")

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
                chosen_card = players[player].play_card()
                player_card_picks.append((player, chosen_card))

                new_card = players[player].draw_hand(self.redCards.get_cards(), 1)
                
                if players[player] is players[model_player]:
                    model_player_new_card = new_card[0]
                    print(f"\nModel player chose the card: {chosen_card.name} - {chosen_card.description}")

            # Judge makes a decision then resets the player card area
            winner = players[judge].judge(player_card_picks)
            
            # Suppose there are 5 players.
            # If judge is player 2, there will be 4 cards played
            # [p1card, p3card, p4card, p5card]
            # Since .judge() gets the index of the best card, if it picks
            # cards of index >1, it will give the score to the player
            # before them. To fix this, add 1 to the winner and % with # players
            # to shift everything to the right
            if winner >= judge:
                winner = (winner+1) % self.num_players

            print(f"\nWinner is Player {winner+1}!")
            players[winner].score += 1

            print("\nOther players cards:")
            for i, card in enumerate(player_card_picks):
                if (card[1] is model_player_play):
                    continue
                print(f"Card {i+1}: {card[1].name} - {card[1].description}")
            
            if judge != model_player:
                print(f"\nNew card added to hand: {model_player_new_card.name} - {model_player_new_card.description}")
            
            player_card_picks = []

            
            # Print the scores
            print("\nNew scores:")
            for i in range(self.num_players):
                print(f"Player {i+1}'s score - {players[i].score}")

            # Check if a player has reached the max score
            for i in range(self.num_players):
                if (players[i].score == self.max_score):
                    print(f"\nGame end! Player {i+1} wins!")
                    self.running = False

            # Judge will be next player
            judge = (judge+1) % self.num_players
            

        return None
