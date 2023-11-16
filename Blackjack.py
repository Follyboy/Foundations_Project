import numpy as np
import random

#This function deals n cards and from the deck and removes them
#It returns a tuple of (the deck with the dealt cards removed, the n dealt cards)
def shuffle_deal(deck, n):
    pile=[]
    random.shuffle(deck)
    for i in range(0,n):
        pile.append(deck[0])
        deck.remove(deck[0])
    return (deck,pile)


#This function calculates the current score of the hand; since A can be 1 or 11 the function will change depending on the current situation
def score(cards_input): #input expected should be a a list of numbers and/or strings with a length of 2 or more? depends on how we format other functions I guess 
    score = 0
    aces = 0

    for card in cards_input:
        if card == "A":
            aces+=1
            score+=11 #start out with ace == 11 but is adjusted if needed 
        elif card in ['J','Q','K']:
           score+=10
        else:
            score +=card

    while aces > 0 and score > 21: ##this makes sure that the ace value is changed from 11 to 1 when the score gets too high 
        score -= 10
        aces -=1
    return score

def set_bet(cash):
    #Take a bet as input
    bet=eval(input(f"How much of your ${cash} do you want to bet on this round (minimum $0.01)?") or cash//10)
    #Make sure that the player is entering a number. As to not quit the program, theres a default value
    if (type(bet) != int) and (type(bet) != float):
        print("That's not a valid bet! We will be using 10% of your money instead")
        bet=round(cash/10,2)
    #This is to ensure that they dont bet more than they have
    if bet<0.01:
        print("Too low of a bet, we are rounding up your bet to the minimum")
        bet=0.01
    if bet>cash:
        print("Woah there! You don't have that much Cash right now. Looks like your going all in")
        bet=cash

    #Rounding down the bet to 2 decimals
    bet=round(bet,2)
    print(f"Bet= ${bet}")
    #Subtracting bet on the table from cash
    cash=round(cash-bet,2)
    print(f"Remaining Money: ${cash}")
    #Returns both the adjusted cash and new bet
    return(cash,bet)
#===================== NEED TO FINISH THE INSTRUCTIONS FUNCTION===========================VVVVV
def show_instructions():
    instructions="uhh idk"
    print(instructions)

def game(cash, deck, bet):
    busted=False
    #Hand is the players hand, FDC is the dealers facedown card, table is the dealer's face up card
    hand=[]
    FDC=[]
    table=['Face Down Card']
    #Dealing cards
    #It is formatted like this bc: the shuffle_deal function outputs the new deck and the dealt cards
    deck,h=shuffle_deal(deck,2)
    deck,f=shuffle_deal(deck,1)
    deck,t=shuffle_deal(deck,1)
    for i in h:
        hand.append(i)
    for i in f:
        FDC.append(i)
    for i in t:
        table.append(i)
    print(f"Your Hand: {hand}")
    print(f"Dealer Cards: {table}")
    HS=score(hand)
    TS=score(table[1:])+score(FDC)
    if HS == 21 and TS==21:
        cash= cash+bet
        #Need an End Condition
    elif HS==21:
        #Instant Win
        cash=cash+2*bet
        #Need an End
    elif TS==21:
        print("eek")
        #End
    print(f"Your Score: {HS}")
    print(f"Your bet: {bet}")
   #This is where the player can choose to stand or hit (or get instructions/ quit)
    while True:
        I = input("Decision time: enter s to stand or h to hit. Enter i for instructions or q to quit")
        if type(I)!= str:
            print("Invalid Input, please try again!.")
            continue
        if I=='i':
            show_instructions()
            continue

        if I == 'h':
            deck, h = shuffle_deal(deck, 1)
            for i in h:
                hand.append(i)
            print(f"Your Hand: {hand}")
            HS=score(hand)
            if HS>21:
                print("You're busted")
                busted=True
                break
            else:
                continue
        if I == 's' or I=='q':
            break
    #Mid-game Quit:
    if I == 'q':
        return ("Q")
    #This condition triggers if the player is busted. Instantly loses the game
    if busted==True:
        print("Better luck next round!")
        print(f"Remaining money: ${cash}")
        return(cash)
    else:
        #Dealer play:
        print(f"Dealer's Face Down Card was:{FDC[0]}")
        table=table[1:]
        table.append(FDC[0])
        print("Table:", table)
        TS=score(table)
        #This is to force the dealer to draw
        if TS < 17:
            while True:
                    print("The Dealer Draws:")
                    deck,t=shuffle_deal(deck,1)
                    for i in t:
                        table.append(i)
                    print(f"Table Cards: {table}")
                    TS = score(table)
                    if TS <17:
                        continue
                    else:
                        break
        #Possible endings:

        #Dealer goes over 21
        if TS>21:
            print(f"Dealer is busted. You win ${bet}")
            cash+= (2*bet)
            return(cash)
        HS = score(hand)
        #Player beats dealer
        if HS > TS:
            print(f"You Win! You won ${bet}")
            cash += (2 * bet)
            return (cash)
        #Tie
        elif HS == TS:
            print("Its a tie. You got your bet back")
            cash+=bet
            return(cash)
        #Player loses to dealer
        else:
            print("The Dealer won! Better luck next time...")
            print(f"Remaining Cash: ${cash}")
            return(cash)
#============= This is the function that actually starts the game. Think of it as a main menu
def start():
    print("Welcome to Pyjack!")

    while True:
        C = input("Please Enter b to start the game, i to read the instructions, or q to quit")
        if type(C)!= str:
            print("Invalid Input. Please try again")
            continue
        if C=='i':
            show_instructions()
        if C=='q' or C=='b':
            break
    if C=='b':
    #NEED A DIFFICULTY SELECTION HERE
        print("You are starting out with $100, if run out, you are done!")
        cash = 100
    #Arbitrary Win limit, so the player can have a final victory
        limit=cash*20
        while cash > 0:
            Hearts = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
            Clubs = Hearts.copy()
            Spades = Hearts.copy()
            Diamonds = Hearts.copy()
            deck = Hearts + Clubs + Spades + Diamonds
            cash,bet=set_bet(cash)
            print(f"Remaining cash: ${cash}")
            cash=game(cash,deck,bet)
            #To ask players if they want another game
            while True:
                if cash=='Q':
                    break
                A=input("Another Round (y/n) ?")
                if A== 'n':
                    cash='Q'
                    break
                if A =='y':
                    break
                else:
                    print("Input not understood. Please try again.")
            if cash=='Q':
                break
            if cash>limit:
                print(f"You beat the house! Enjoy your (virtual) ${cash}")
                break
            #This condition will hit, if the player has just gone below 0
            if cash==0:
                print(f"Money: ${cash}")
                print("Tough Luck. You are out of cash. See you later!")
                break
            #For those who quit in the middle of the game

    #This will catch players who just won/lost and those who quit
    print("Thanks for Playing! See you soon!")
    return()

start()

#THINGS TO DO:
#We need somebody to type up the instructions (The function is above, but it doesnt print anything)
#We need to modify the game function to include special rules: Double Down, Insurance, Splitting pairs
#Here are the instructions I am working from: https://bicyclecards.com/how-to-play/blackjack
#We need to figure out how to implement the difficulty setting
#Still need to modualize it (idk how to do that I assume we will learn in class)
#Possibly card text art function ?



