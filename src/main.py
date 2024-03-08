from agent import Agent
from decks import GreenCards, RedCards


if __name__ == "__main__":
    greenCards = GreenCards()
    redCards = RedCards()
    redCards.shuffle()

    agent = Agent()
    agent.draw_hand(redCards.get_cards())
    print(agent.get_pos_tags())

    
