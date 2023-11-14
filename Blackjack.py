import numpy as np
import random


#The base Deck Suits Dont matter for the game
Hearts=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
Clubs=Hearts.copy()
Spades=Hearts.copy()
Diamonds=Hearts.copy()
Deck=Hearts+Clubs+Spades+Diamonds


#This function deals n cards and from the deck and removes them
#It returns a tuple of (the deck with the dealt cards removed, the n dealt cards)
def shuffle_deal(deck, n):
    pile=[]
    random.shuffle(deck)
    for i in range(0,n):
        pile.append(deck[0])
        deck.remove(deck[0])
    return (deck,pile)

print(shuffle_deal(Deck,2)[1])

#This function calculates the current score of the hand; since A can be 1 or 11 the function will change depending on the current situation
def score(cards_input): #input expected should be a a list of numbers and/or strings with a length of 2 or more? depends on how we format other functions I guess 
    score = 0
    aces = 0

    for card in cards_input:
        if card == "A":
            aces+=1
            score+=11 #start out with ace == 11 but is adjusted if needed 
        elif card in ['J','Q','K']:
            score += 10
        else:
            score +=card

    while aces > 0 and score > 21: ##this makes sure that the ace value is changed from 11 to 1 when the score gets too high 
        score -= 10
        aces -=1

    return score