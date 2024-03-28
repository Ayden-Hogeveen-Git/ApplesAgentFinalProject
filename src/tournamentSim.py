from decks import GreenCards, RedCards
from agent import Agent
from game import Game


def tournament(num_games=100):
    agents = []

    agents.append(Agent("random"))
    agents.append(Agent("alit"))
    agents.append(Agent("pos"))
    agents.append(Agent("assoc"))

    # Initialize counters for wins
    wins = {0: 0, 1: 0, 2: 0, 3: 0}

    for i in range(num_games):
        # Play a game and get the result
        result = play_game(agents)

        # Update the win counters based on the result
        wins[result] += 1
        print(i+1)

    # Print or return the results
    print(f"Random Agent wins: {wins[0]}, Alit Agent wins: {wins[1]}, Pos Agent wins: {wins[2]}, Levenshtein Agent wins: {wins[3]}")

def play_game(agents):
    # Create a game instance
    game = Game(len(agents), 1, "Basic_Green_Cards.txt", "Basic_RED_cards.txt")

    # Run Game
    return game.run(agents)


if __name__ == "__main__":
    tournament()