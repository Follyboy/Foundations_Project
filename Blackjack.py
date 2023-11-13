import numpy as np
import random



Hearts=[2,3,4,5,6,7,8,9,10,'J','Q','K','A']
Clubs=Hearts.copy()
Spades=Hearts.copy()
Diamonds=Hearts.copy()
Deck=Hearts+Clubs+Spades+Diamonds

def shuffle_deal(deck, n):
    d=[]
    pile=[]
    random.shuffle(deck)
    for i in range(0,n):
        pile.append(deck[i])
    return (pile)

print(shuffle_deal(Deck,2))
