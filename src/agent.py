# Takes a card datatype as input and outputs a card datatype
import random
from card import Card
import nltk

import re
from decks import RedCards  # Demo purposes ONLY
# nltk.download()  # uncomment then run to manage nltk packages

from nltk.tokenize import RegexpTokenizer
import gensim

from datasets import load_dataset   # Load WikiText corpus
from gensim.utils import simple_preprocess  # Tokenizes text
from gensim.models import Word2Vec  # Word2Vec model
from gensim.models import KeyedVectors  # To save and use model after training
import os.path  # To check if word vector file is available
import numpy as np


# To use corpus as training data without using too much memory
class SentenceIterator: 
    def __init__(self, data): 
        self.data = data 

    def __iter__(self):
        for text in self.data["train"]:
            yield simple_preprocess(text["text"])


# Represents the game agent
class Agent:
    def __init__(self, agent_type="random", is_dealer=False):
        self.hand = []

        self.agent_type = agent_type
        self.score = 0

        self.is_dealer = is_dealer
        self.green_card = None

        self.wordvector = None
        if agent_type == "model_training":
            if os.path.isfile("a2a.wordvectors"):
                self.wordvector = KeyedVectors.load("a2a.wordvectors", mmap='r')
            else:
                self.wordvector = self.train_model()
        

    def judge(self, cards):
        """
        Judges the cards of the other players
        :param cards: list of tuples (player number, card)
        :return: int (index of the winning player)
        """
        # Judge based on agent type

        if (self.agent_type == "random"):
            # Picks random card from the play area
            return random.randint(0, len(cards) - 1)
        
        elif (self.agent_type == "alit"):
            # Pick the first card that has the same letter
            # as our green card. Return its index
            first_letter = self.green_card[0]

            for i in range(len(cards)):
                if (self.hand[i][0] == first_letter):
                    return i
                
            # Return the first card index since no other cards have the
            # same letter as the green card
            return 0
        
        elif (self.agent_type == "assoc"):
            # Returns the lowest Levenshtein distance card index
            best_card = cards[0][0]
            temp = nltk.edit_distance(self.green_card.name, cards[0][1].name)
            for i in range(1, len(cards)):
                if (temp > nltk.edit_distance(self.green_card.name, cards[i][1].name)):
                    best_card = cards[i][0]
                    temp = nltk.edit_distance(self.green_card.name, cards[i][1].name)

            return best_card
        
        elif (self.agent_type == "pos"):
            # Return index of same parts of speech
            tags = self.get_pos_tags()
            
            if (self.green_card is not None):
                target = nltk.pos_tag([self.green_card])
                            
                for tag in tags:
                    if (target == tag[0][1]):
                        return (tags.index(tag))
                    
            # Return index of first card
            return 0
        
        elif (self.agent_type == "model_training"):
            red_cards = [card[1] for card in cards]
            green_card = self.green_card
            
            red_cards_with_vectors = self.modify_hand_red(red_cards, self.wordvector)
            green_card_with_vector = self.modify_hand_green(green_card, self.wordvector)

            best_sim = -5
            best_card = 0
            for i, card in enumerate(red_cards_with_vectors):
                similarity = (np.dot(green_card_with_vector[1], card[1]) /
                            (np.linalg.norm(green_card_with_vector[1]) * 
                            np.linalg.norm(card[1]))
                                )
                if similarity > best_sim:
                    best_sim = similarity
                    best_card = i
            return best_card

        return 0
    
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
        elif (self.agent_type == "model_training"):
            return self.play_with_model()

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
            card_scores.append(nltk.edit_distance(self.green_card.name, self.hand[i].name))
        
        return self.hand.pop(card_scores.index(max(card_scores)))
    
    def draw_hand(self, deck, num_cards=7):
        """
        Draws a hand from the deck
        :param deck: list of card datatype
        :return: Added cards
        """
        cards = []
        for i in range(num_cards):
            card = deck.pop(0)
            self.add_card(card)
            cards.append(card)

        return cards

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


    def train_model(self):
        """
        Trains a model to be used by our agent
        :return: dict (vector representation of words)
        """
        
        # Load data for model
        data_files = {"train": ["wikitext-train-00000-of-00002.arrow",
                                "wikitext-train-00001-of-00002.arrow"]}
        directory = (
                    "src/corpora/wikitext/wikitext-103-v1/"
                    "0.0.0/b08601e04326c79dfdd32d625aee71d232d685c3/"
                    )
                    
        data = load_dataset("arrow", data_dir=directory,
                            data_files=data_files)
        
        train_sentences = SentenceIterator(data)
        model = Word2Vec(
            sentences=train_sentences,
            vector_size=300,
            window=5,
            min_count=5,
            workers=8,
            epochs=5
            )
        wv = model.wv
        print("Done training! trying to save.")

        # Save and return model wordvector
        wv.save("a2a.wordvectors")
        print("Done saving!")

        del model
        return wv

 
    def modify_hand_red(self, hand, wv):
        size_vec = 300
        card_to_vec = []

        for card in hand:
            # Set average vector to 0
            # Set count to 0, will be used to get average vector
            average_vector = np.zeros(shape=size_vec)
            count = 0

            # For each word in card name + description:
            # removed description since i think it introduces a lot of noise
            # -> + simple_preprocess(card.description)
            for word in (simple_preprocess(card.name)):
                # To prevent errors, only check if it exists in the word vector dictionary
                if word in wv.key_to_index:
                    count += 1
                    average_vector += wv[word]
            
            card_to_vec.append((card, average_vector/count if count > 0 else average_vector))

        return card_to_vec


    def modify_hand_green(self, card, wv):
        size_vec = 300

        average_vector = np.zeros(shape=size_vec)
        count = 0

        for word in (simple_preprocess(card.name) + simple_preprocess(card.description)):
            if word in wv.key_to_index:
                count += 1
                average_vector += wv[word]

        return (card, average_vector/count if count > 0 else average_vector)


    def play_with_model(self):
        red_cards = self.hand
        green_card = self.green_card
        
        red_cards_with_vectors = self.modify_hand_red(red_cards, self.wordvector)
        green_card_with_vector = self.modify_hand_green(green_card, self.wordvector)

        best_sim = -5
        best_card = 0
        # print("\nModel choices:")
        for i, card in enumerate(red_cards_with_vectors):
            if (np.any(green_card_with_vector[1]) and np.any(card[1])):
                similarity = (np.dot(green_card_with_vector[1], card[1]) /
                            (np.linalg.norm(green_card_with_vector[1]) * 
                            np.linalg.norm(card[1]))
                                )
            else:
                similarity = -1
            # print(f"{card[0].name} similarity to {green_card.name} is: {similarity}")
            if similarity > best_sim:
                best_sim = similarity
                best_card = i
        
        # print(f"\nModel thinks {red_cards[best_card].name} is best with {green_card.name} with a score of {best_sim}\n")
        return self.hand.pop(best_card)


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

