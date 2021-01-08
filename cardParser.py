
NUMBER = 0
SUIT = 1

CARDS_IN_HAND = 2
CARDS_IN_FLOP = 3
CARDS_IN_TURN = 1

numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = {
    "C": "♣️",
    "D": "♦️",
    "H": "♥️",
    "S": "♠️",
}

def parseCardsInHand(userInput):
    cards = userInput.split()

    if (not isCorrectNumberOfCards(CARDS_IN_HAND, cards)):
        return "error"
    
    firstHandCard = parseCardValue(cards[0])
    secondHandCard = parseCardValue(cards[1])

    if (firstHandCard == "error" or secondHandCard == "error"):
        return "error"
    
    return firstHandCard, secondHandCard


def parseCardsInFlop(userInput):
    
    cards = userInput.split()

    if (not isCorrectNumberOfCards(CARDS_IN_FLOP, cards)):
        return "error"
    
    firstFlopCard = parseCardValue(cards[0])
    secondFlopCard = parseCardValue(cards[1])
    thirdFlopCard = parseCardValue(cards[2])

    if (firstFlopCard == "error" or secondFlopCard == "error" or thirdFlopCard == "error"):
        
        return "error"

    return firstFlopCard, secondFlopCard, thirdFlopCard

def parseCardsInTurn(userInput):

    cards = userInput.split()

    if (not isCorrectNumberOfCards(CARDS_IN_TURN, cards)):
        return "error"
    
    turnCard = parseCardValue(cards[0])

    if (turnCard == "error"):
        return "error"
    
    return turnCard

def parseCardValue(card):

    if (len(card) != 2):
        return "error"
    
    if (card[NUMBER] not in numbers or card[SUIT].upper() not in suits):
        return "error"

    return card[NUMBER] + suits[card[SUIT].upper()]


def isCorrectNumberOfCards(correctNumber, cards):
    return len(cards) == correctNumber

