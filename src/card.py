# Represents the game cards

class Card:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        """
        Overloads the str method to return the value of the card when printed
        """
        return f"Card name: {self.name}\nCard Description: {self.description}"
