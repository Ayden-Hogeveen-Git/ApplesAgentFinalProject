# Represents the game cards

class Card:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        """
        Overloads the str method to return the value of the card when printed
        """
        return str(self.value)
