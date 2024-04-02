# Takes a card datatype as input and outputs a card datatype
import random
from card import Card
import nltk
import re
from decks import RedCards  # Demo purposes ONLY
# nltk.download()  # uncomment then run to manage nltk packages

from nltk.tokenize import RegexpTokenizer
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

from nltk.corpus import brown
from nltk.corpus import reuters
import numpy as np


# Represents the game agent
class Agent:
    def __init__(self, agent_type="random", is_dealer=False):
        self.hand = []

        self.agent_type = agent_type
        self.score = 0

        self.is_dealer = is_dealer
        self.green_card = None

    def judge(self, cards):
        """
        Judges the cards of the other players
        :param cards: list of tubles including index and card datatype
        :return: int (index of the winning player)
        """
        best_card = cards[0][0]
        temp = nltk.edit_distance(self.green_card, cards[0][1])
        for i in range(1, len(cards)):
            if (temp > nltk.edit_distance(self.green_card, cards[i][1])):
                best_card = cards[i][0]
                temp = nltk.edit_distance(self.green_card, cards[i][1])
        return best_card           
            

    def play_card(self):
        """
        Plays a card from the agent's hand
        :return: card datatype
        """
        if (self.agent_type == "random"):
            return self.play_random_card()
        elif (self.agent_type == "alit"):
            return self.play_alit_card()
        elif (self.agent_type == "assoc"):
            return self.play_associated_card()
        elif (self.agent_type == "pos"):
            return self.play_card_pos()

    def play_random_card(self):
        """
        Plays a card from the agent's hand randomly
        :return: card datatype
        """
        return self.hand.pop(random.randint(0, len(self.hand) - 1))
    
    def play_alit_card(self):
        """
        Plays a card from the agent's had based on the first letter of the green 
        card, otherwise plays the first card
        :return: card datatype
        """
        first_letter = self.green_card[0]
        for i in range(len(self.hand)):
            if (self.hand[i][0] == first_letter):
                return self.hand.pop(i)
        
        return self.hand.pop(0)

    def play_card_pos(self):
        """
        Plays a card from the agent's hand based on similar parts of speech
        :return: card datatype
        """
        tags = self.get_pos_tags()
        
        if (self.green_card is not None):
            target = nltk.pos_tag([self.green_card])
                        
            for tag in tags:
                if (target == tag[0][1]):
                    return self.hand.pop(tags.index(tag))
                
        return self.hand.pop(0)
    
    def play_associated_card(self):
        """
        Plays a card from the agent's hand based on the Levenshtein distance
        between the green card and the red card. This distance is calculated from
        the number of single-character edits required to change one word into the other.
        :return: card datatype
        """
        card_scores = []
        for i in range(len(self.hand)):
            card_scores.append(nltk.edit_distance(self.green_card, self.hand[i]))
        
        return self.hand.pop(card_scores.index(max(card_scores)))
    
    def draw_hand(self, deck, num_cards=7):
        """
        Draws a hand from the deck
        :param deck: list of card datatype
        :return: None
        """
        for i in range(num_cards):
            self.add_card(deck.pop(0))

    def demo_red_card(self):
        all_red_cards = RedCards().cards
        first_letter = self.green_card[0]
        for i in range(len(all_red_cards)):
            if all_red_cards[i][0] == first_letter:
                return all_red_cards[i]

    def draw_green_card(self, deck):
        """
        Draws a green card from the deck
        :param deck: list of card datatype
        :return: None
        """
        self.green_card = deck.pop(0)
    
    def get_green_card(self):
        """
        Returns the green card
        :return: card datatype
        """
        return self.green_card

    def add_card(self, card):
        """
        Adds a card to the agent's hand
        :param card: card datatype
        :return: None
        """
        self.hand.append(card)

    def tokenize(self, text):
        """
        Splits the inputted string into the individual words, this function will be used to split a training set into tokens
        :param text: string
        :return: list of strings
        """
        return re.findall(r'\b\w+\b', text)  # Uses a regular expression to split the string into words
    
    def get_pos_tags(self):
        """
        Returns the part of speech tags for the agent's hand
        :return: list of strings
        """
        pos_tags = []
        for card in self.hand:
            pos_tags.append(nltk.pos_tag([card]))
        return pos_tags

    def get_hand_size(self):
        """
        Returns the size of the agent's hand
        :return: int
        """
        return len(self.hand)

    #
    # START ADD -J
    #

    def add_green_card_examples(self, corpus):
        """
        TODO
        Adds definitions of given green cards to the corpus
        :return: None
        """

        return None

    def add_red_card_examples(self, corpus):
        """
        TODO
        Adds definitions of given red cards to the corpus
        :return: None
        """

        return None

    def train_model(self):
        """
        Trains a model to be used by our agent
        :return: dict (vector representation of words)
        """
        size_vec = 300
        tokenizer = RegexpTokenizer(r'\w+')

        corpus = []
        for sentence in brown.sents():
            # convert all to lowercase and remove punctuation
            corpus.append(tokenizer.tokenize(' '.join(sentence)))
        
        for sentence in reuters.sents():
            corpus.append(tokenizer.tokenize(' '.join(sentence)))

        # Add definitions of green and red cards to the corpus
        self.add_green_card_examples(corpus)
        self.add_red_card_examples(corpus)

        # Note this will take 30-ish seconds every run. The model will train itself at the
        # beginning 
        model = Word2Vec(vector_size=size_vec, window=5, min_count=3, workers=10)
        model.build_vocab(corpus)
        model.train(corpus, total_examples=model.corpus_count, epochs=100)
        wv = model.wv

        return wv
    
    def get_red_cards(self):
        red_cards = {}
        tokenizer = RegexpTokenizer(r'\w+')
        with open("Basic_RED_cards.txt", "r") as file:
            for line in file.readlines():
                card = line.strip().split("&")

                name = card[0].lower()
                red_cards[name] = []

                for word in tokenizer.tokenize(card[1]):
                    red_cards[name].append(word)
                
        return red_cards

    def get_green_cards(self):
        green_cards = {}
        with open("Basic_Green_Cards.txt", "r") as file:
            for line in file.readlines():
                card = line.strip().split("&")

                name = card[0].lower()
                green_cards[name] = []
                
                for word in card[1].split(", "):
                    green_cards[name].append(word.lower())

        return green_cards


    def modify_hand_red(self, deck, hand, wv):
        size_vec = 300
        card_to_vec = {}

        for card in hand:
            # check each of these words and calculate its average vector
            words_to_check = card.split() + deck[card]

            average_vector = np.zeros(shape=size_vec)
            count = 0

            for word in words_to_check:
                if word in wv.key_to_index:
                    count += 1
                    average_vector += wv[word]
            
            card_to_vec[card] = average_vector/count if count > 0 else average_vector
        return card_to_vec


    def modify_hand_green(self, deck, hand, wv):
        size_vec = 300
        card_to_vec = {}

        for card in hand.split():
            words_to_check = card.split() + deck[card]

            average_vector = np.zeros(shape=size_vec)
            count = 0

            for word in words_to_check:
                if word in wv.key_to_index:
                    count += 1
                    average_vector += wv[word]
            
            card_to_vec[card] = average_vector/count if count > 0 else average_vector
        return card_to_vec


    def draw_red_cards(self, deck, num):
        hand = []
        for _ in range(num):
            hand.append(random.choice(list(deck.keys())))
        return hand


    def pick_using_model(self, wv):
        red_cards = self.get_red_cards()
        green_cards = self.get_green_cards()
        
        # get 5 cards from red cards
        red_card_hand = self.draw_red_cards(red_cards, 5)

        # pick a random green card
        green_card = random.choice(list(green_cards.keys()))
        
        # create red card hand with vector for each card
        # to do this, go through all words of the red card and get its average vector
        red_card_hand = self.modify_hand_red(red_cards, red_card_hand, wv)
        
        # now do the same to the green card
        green_card = self.modify_hand_green(green_cards, green_card, wv)
        
        # now go through each red card and check its cosine similarity to the green card. pick the
        # highest
        check_green = list(green_card.keys())[0]
        
        best_sim = -5
        best_card = ""
        
        for card in red_card_hand:
            similarity = np.dot(green_card[check_green], red_card_hand[card])/(np.linalg.norm(green_card[check_green])*np.linalg.norm(red_card_hand[card]))
            print(f"{card}'s similarity to '{check_green}' is {similarity}")
            if similarity > best_sim:
                best_sim = similarity
                best_card = card
        
        # either our green card did not have a score or our red cards did not have a score
        if best_card == "":
            best_card = random.choice(list(red_card_hand.keys()))

        print(f"\nCards: {list(red_card_hand.keys())}")
        print(f"The best card for '{check_green}' is '{best_card}' with a score of {best_sim}")
        pass
    
    #
    # END ADD -J
    #

    def __str__(self):
        """
        Overloads the str method to return the agents hand when printed
        :return: string
        """
        string = "Hand: "
        for card in self.hand:
            string += "\n" + str(card)
        return string


# p1 = Agent()  # arg1<agent_type>, arg2<is_dealer>
# print(p1.database)  # prints full list of all green cards (nouns)
""" This whole main is for demo purposes ONLY. """
if __name__ == "__main__":
    # print("Part 1) Let's select a green card from the database and let the agent choose the ""best"" red one:")
    # p1 = Agent()
    # random.shuffle(p1.database)
    # p1.draw_green_card(p1.database)
    # print("Here is our green card: {}".format(p1.get_green_card()))
    # print("Agent's Turn...")
    # print(p1.demo_red_card())
    # userInput = input("Part 2) Enter a green card (noun): ")  # assumes a valid input
    # p2 = Agent()
    # p2.green_card = userInput
    # print("Agent's Turn...")
    # print(p2.demo_red_card())

    p1 = Agent()
    wv = p1.train_model()
    p1.pick_using_model(wv)

