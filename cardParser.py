
NUMBER = 0
SUIT = 1

numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = {
    "C": "♣️",
    "D": "♦️",
    "H": "♥️",
    "S": "♠️",
}


def getCardValue(card):

    if (len(card) != 2):
        return "error"
    
    if (card[NUMBER] not in numbers or card[SUIT] not in suits):
        return "error"

    return card[NUMBER] + suits[card[SUIT]]
