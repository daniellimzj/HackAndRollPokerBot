CARDS_LEFT_PRE_FLOP = 5
CARDS_LEFT_POST_FLOP = 2
CARDS_LEFT_POST_TURN = 1
PERCENT = 100

numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = {
    "C": "♣️",
    "D": "♦️",
    "H": "♥️",
    "S": "♠️",
}

def findPairOdds(knownCards, stage):

    cardValues = [card[0] for card in knownCards]
    result = {}

    for value in cardValues:
        if value in result:
            result[value] += 1
        else:
            result[value] = 1
    
    for key in result:
        if result[key] > 2:
            return 0
        elif result[key] == 2:
            return 100

    if (stage == "preflop"):
        return round(PERCENT * CARDS_LEFT_PRE_FLOP * (6 * 44 * 43 * 42 * 41) / (50 * 49 * 48 * 47 * 46), 2)
    
    elif (stage == "postflop"):
        return round(PERCENT * CARDS_LEFT_POST_FLOP * (15 * 32) / (47 * 46), 2)
    
    else:
        return round(PERCENT * CARDS_LEFT_POST_TURN * 18 / 46, 2)


def findTripsOdds(knownCards, stage):

    cardValues = [card[0] for card in knownCards]

    result = {}

    for value in cardValues:
        if value in result:
            result[value] += 1
        else:
            result[value] = 1
    
    for key in result:
        if result[key] > 3:
            return 0
        elif result[key] == 3:
            return 100
    
    if (findPairOdds(knownCards, stage) != 100):
        return 0

    if (stage == "preflop"):
        return 18.37

    elif (stage == "postflop"):
        return round(PERCENT * CARDS_LEFT_POST_FLOP * (2 * 45 ) / (47 * 46), 2)
    
    else:
        return round(PERCENT * CARDS_LEFT_POST_TURN * 2 / 46, 2)

def findFlushOdds(knownCards, stage):

    cardSuits = [card[1] for card in knownCards]
    result = {}

    for suit in cardSuits:
        if suit in result:
            result[suit] += 1
        else:
            result[suit] = 1
    
    largestNumberOfSuitedCards = max(list(result.values()))

    if (stage == "preflop" and largestNumberOfSuitedCards == 2):
        return 6.4

    if (stage == "postflop" and largestNumberOfSuitedCards == 4):
        return 34.97

    if (stage == "turn" and largestNumberOfSuitedCards == 4):
        return 19.5

    return 0
    
