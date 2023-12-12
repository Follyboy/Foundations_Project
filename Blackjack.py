#%%
import random

#This function deals n cards and from the deck and removes them
#It returns a tuple of (the deck with the dealt cards removed, the n dealt cards)
def shuffle_deal(deck, n):
    """
    Shuffle the deck and deal n cards.
    Returns a tuple of (the deck with the dealt cards removed, the n dealt cards).
    """
    pile=[]
    random.shuffle(deck)
    for i in range(0,n):
        pile.append(deck[0])
        deck.remove(deck[0])
    return (deck,pile)


#This function calculates the current score of the hand; since A can be 1 or 11 the function will change depending on the current situation
def score(cards_input): #input expected should be a a list of numbers and/or strings with a length of 2 or more? depends on how we format other functions I guess 
    """
    Calculate the current score of the hand.
    """
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
    """
    Set the bet for the round.
    Returns the adjusted cash and the new bet.
    """
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
    """
    Display game instructions.
    """
    instructions = """
        Get ready to play Blackjack!

        Objective:
        - The goal of the game is to have a hand with a total score as close to 21 as possible without exceeding it.

        Gameplay:
        1. At the beginning of each round, you'll be prompted to place a bet using a portion of your available cash.
        2. The dealer will then shuffle the deck and deal two cards to you.
        3. Your hand's score is calculated based on the values of the cards. Number cards contribute their face value, face cards (J, Q, K) contribute 10, and Aces can be either 1 or 11.
        4. You can choose to "hit" (receive an additional card) or "stand" (keep your current hand).
        5. Be strategic in your decisions. If your total score exceeds 21, you "bust," and the round is lost.
        6. After you decide to stand, the dealer reveals their hand and follows a set of rules. The dealer will keep hitting until their hand is 17 or higher.
        7. The winner of the round is the one with a hand closest to 21 without busting.

        Scoring:
        - If you have an Ace and a 10-value card (10, J, Q, K) in your initial two cards, you have a "blackjack" and win the round instantly.

        Betting:
        - You start with a certain amount of cash. Adjust your bets wisely to maximize your winnings.

        Commands:
        - Type "hit" to receive another card.
        - Type "stand" to keep your current hand.

    Enjoy the game and good luck!
    """
    print(instructions)

def choose_difficulty(level):
    # Initializes cash variable to zero
    cash = 0

    # Converts the 'level' variable to lowercase
    level = level.lower()

    # Checks the level and assigns cash accordingly
    if level == 'hard':
        cash = 100
    elif level == 'medium':
        cash = 300
    elif level == 'easy':
        cash = 500

    # Returns the assigned cash value based on the chosen level
    return cash


def player_hit(deck, hand):
    deck,h=shuffle_deal(deck,1)
    for card in h:
        hand.append(card)
    return hand

def dealer_play(deck, dealer_hand):
    while score(dealer_hand) < 17:
        dealer_hand = player_hit(deck, dealer_hand)
    return dealer_hand

def determine_winner(player_hand, dealer_hand, bet, cash):
    player_score = score(player_hand)
    dealer_score = score(dealer_hand)

    if player_score > 21:
        print("Player busts! Dealer wins.")
        return cash

    if dealer_score > 21:
        print(f"Dealer is busted. You win ${bet}")
        return cash + 2 * bet

    if player_score == dealer_score:
        print("It's a tie. You got your bet back")
        return cash + bet

    if player_score > dealer_score:
        print(f"You Win! You won ${bet}")
        return cash + 2 * bet

    print("The Dealer won! Better luck next time...")
    print(f"Remaining Cash: ${cash}")
    return cash

def double_down(deck, hand, bet, cash):
    dd_choice = input("Do you want to double your bet? (y/n)").lower()

    if dd_choice =='y':
        if bet < cash:
            bet *= 2 #doubling bet
            cash-=bet
            print(f"Your bet is now ${bet}")
        else:
            print("You don't have the money to double your bet")


    # Deal one additional card after doubling down
    deck, additional_card = shuffle_deal(deck, 1)
    hand.append(additional_card[0])
    print(f"Your Hand after double down: {hand}")

def can_split(hand, remaining_cash, bet):
    return len(hand) == 2 and hand[0] == hand[1] and remaining_cash >= bet
    
def split_pairs(hand, deck, cash, bet):
    deck,dealer_hand_before=shuffle_deal(deck,2) # Dealer hand (one face down and one face up)
    new_hands = [hand[0], hand[1]]  # Split the hand into two separate hands
    dealer_hand_after = dealer_play(deck, dealer_hand_before)
    busted = False

    # Asks the user if they want to split
    choice = input("Do you want to split? Enter 'y' or 'n': ")

    # Checks if the user's input (converted to lowercase) is 'y'
    if choice.lower() == 'y':
        # Deducts the bet amount from the cash
        cash = cash - bet
        
        # Loops through each new hand
        for idx, new_hand in enumerate(new_hands):
            # Deals a new card from the deck
            deck, h = shuffle_deal(deck, 1)
            # Appends a new card to the current hand
            new_hand = [new_hand, h[0]]
            
            # Checks if the hand can be split
            if can_split(new_hand, cash, bet):
                # Splits the pairs and updates cash if possible
                cash = split_pairs(new_hand, deck, cash, bet)
            else:
                # Prints the current player's hand and the dealer's visible card
                print(f"\nPlaying Hand {idx + 1}: {new_hand}")
                print(f"Dealer Cards: [Face Down Card, {dealer_hand_before[1]}]")
                
                # Calculates scores for the player's hand and the dealer's hand
                HS = score(new_hand)
                TS = score(dealer_hand_after)
                
                # Checks for different game outcomes (tie, blackjack, or ongoing game)
                if HS == 21 and TS == 21:
                    cash = cash + bet
                    I = 's'
                    print('It\'s a tie, you get your money back.')
                elif HS == 21:
                    # Instant Win - Blackjack
                    I = 's'
                    jackpot_bet = (bet * 1.5) + bet
                    cash = cash + jackpot_bet
                    print(f"Black Jack! You Win ${jackpot_bet:.2f}!")
                else:
                    # Asks the player to make a decision (hit, stand, instructions, or quit)
                    while True:
                        I = input("Decision time: enter s to stand or h to hit. Enter i for instructions or q to quit")
                        if type(I) != str:
                            print("Invalid Input, please try again!.")
                            continue
                        if I == 'i':
                            show_instructions()
                            continue
                        
                        if I == 'h':
                            # Player decides to hit, receives a new card and updates the hand
                            new_hand = player_hit(deck, new_hand)
                            print(f"Your Hand: {new_hand}")
                            HS = score(new_hand)
                            print(f"Your Score: {HS}")
                            
                            # Checks if the player is busted (hand value over 21)
                            if HS > 21:
                                print("You're busted")
                                busted = True
                                break
                            else:
                                continue
                        
                        if I == 's' or I == 'q':
                            break
                    
                    # Handles mid-game quitting
                    if I == 'q':
                        cash = "Q"
                        
                    if busted == True:
                        # Prints a message for a busted hand
                        print("Better luck next round!")
                        print(f"Remaining money: ${cash}")
                        cash = cash
                    else:
                        # Dealer plays their turn
                        print(f"Dealer's Face Down Card was:{dealer_hand_before[0]}")
                        print("Table:", dealer_hand_before)
                        if dealer_hand_before!=dealer_hand_after:
                            print("The Dealer Draws:")
                            print(f"Current Table Cards: {dealer_hand_after}")
                        print("The Dealer Draws:")
                        print(f"Table Cards: {dealer_hand_after}")
                        
                        # Determines the winner and updates cash based on the outcome
                        cash = determine_winner(new_hand, dealer_hand_after, bet, cash)
        
        # Returns the final cash amount after the game
        return cash
    else:
        return game(cash, deck, bet, hand)

def game(cash, deck, bet, hand):
    busted=False

    #FDC is the dealers facedown card, table is the dealer's face up card
    FDC=[]
    table=['Face Down Card']

    #Dealing cards
    #It is formatted like this bc: the shuffle_deal function outputs the new deck and the dealt cards
    deck,f=shuffle_deal(deck,1)
    deck,t=shuffle_deal(deck,1)

    for i in f:
        FDC.append(i)
    for i in t:
        table.append(i)

    print(f"Your Hand: {hand}")
    print(f"Dealer Cards: {table}")


    # DOUBLE DOWN OPTION
    initial_numeric_hand = score(hand)

    if initial_numeric_hand is not None and initial_numeric_hand in [9, 10, 11]:
        double_down(deck, hand, bet, cash)

    HS=score(hand)
    TS=score(table[1:])+score(FDC)
    if HS == 21 and TS==21:
        cash= cash+bet
        print('It\'s a tie, you get your money back.')
        return cash
    elif HS==21:
        #Instant Win
        I = 's'
        jackpot_bet = (bet * 1.5) + bet
        cash = cash + jackpot_bet
        print(f"Black Jack! You Win ${jackpot_bet:.2f}!")
        return cash
    else:
        print(f"Your Score: {HS}")
        print(f"Your bet: ${bet}")
        #This is where the player can choose to stand or hit (or get instructions/ quit)
        while True:
            I = input("Decision time: enter s to stand or h to hit. Enter i for instructions or q to quit")
            if type(I)!= str:
                print("Invalid Input, please try again!.")
                continue
            if I=='i':
                # Show the instructions when i is entered
                show_instructions()
                continue

            # When h is entered, the player hits and gets an additional card.
            if I == 'h':
                hand = player_hit(deck, hand)
                print(f"Your Hand: {hand}")
                HS=score(hand)
                print(f"Your Score: {HS}")

                if HS>21:
                    print("You're busted")
                    busted=True
                    break
                else:
                    continue
            
            # when s or q is entered, the loop is broken and other statements in the function is ran
            if I == 's' or I=='q':
                break

        #Mid-game Quit:
        if I == 'q':
            return ("Q")
        
        #This condition triggers if the player is busted. Instantly loses the game
        if busted==True:
            print("Better luck next round!")
            print(f"Remaining money: ${cash}")
            return cash
        else:
            #Dealer play:
            print(f"Dealer's Face Down Card was:{FDC[0]}")

            table=table[1:]
            table.append(FDC[0])

            print("Table:", table)
            # TS=score(table)

            #This is to force the dealer to draw
            table = dealer_play(deck, table)
            print("The Dealer Draws:")
            print(f"Table Cards: {table}")
            # TS = score(table)
            return determine_winner(hand, table, bet, cash)

    
#============= This is the function that actually starts the game. Think of it as a main menu
def start():
    """
    This function serves as the main menu to initiate the Blackjack game.

    Players are prompted to choose between starting the game (b), reading the instructions (i), or quitting (q).
    If the player chooses to start the game (b), they will also be prompted to select a difficulty level (easy, medium, or hard).

    Returns:
    None
    """
    print("Welcome to Pyjack!")

    round_number = 1

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
    # Difficulty level determines amount of cash the player is given
        difficulty_level = str(input('Choose difficulty (easy/medium/hard):')).lower()

        while difficulty_level not in ['easy', 'medium', 'hard']:
            difficulty_level = str(input('Must choose difficulty (easy/medium/hard):'))

        cash = choose_difficulty(difficulty_level)
        print(f"You are starting out with ${cash}, if run out, you are done!")
    #Arbitrary Win limit, so the player can have a final victory
        limit = cash * 20

        while cash > 0:
            print(f"\n------------ Round {round_number} --------------------")
            Hearts = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
            Clubs = Hearts.copy()
            Spades = Hearts.copy()
            Diamonds = Hearts.copy()
            deck = Hearts + Clubs + Spades + Diamonds
            cash,bet=set_bet(cash)

            #Player's hand
            hand=[]

            #Dealing cards
            deck,h=shuffle_deal(deck,2)

            for i in h:
                hand.append(i)

            # The comment hand below is for testing black jack win
            # hand = [10, 'A']

            # The comment hand below is for testing the split function
            # hand = [10, 10]

            if can_split(hand, cash, bet):
                cash = split_pairs(hand, deck, cash, bet)
            else:
                cash=game(cash, deck, bet, hand)
            
            #To ask players if they want another game
            while True:
                if cash=='Q':
                    break
                A=input("Another Round (y/n) ?")
                if A== 'n':
                    cash='Q'
                    break
                if A =='y':
                    round_number += 1
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


if __name__ == "__main__":
    start()



# %%
