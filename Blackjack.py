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
