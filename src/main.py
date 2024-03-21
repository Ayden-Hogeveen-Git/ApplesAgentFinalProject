import sys
from game import Game


if __name__ == "__main__":
    if (len(sys.argv) != 5):
        print("Usage: python main.py <num_players> <max_score> <green_cards> <red_cards>")
        sys.exit(1)
    
    game = Game(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    game.run()
