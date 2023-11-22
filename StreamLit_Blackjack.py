#%%
import streamlit as st
import random

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
    # Take a bet as input
    bet = st.number_input(f"How much of your ${cash} do you want to bet on this round (minimum $0.01)?",
                          min_value=0.01, value=cash // 10)
    
    # Make sure that the player is entering a valid number
    if not isinstance(bet, (int, float)):
        st.warning("That's not a valid bet! We will be using 10% of your money instead")
        bet = round(cash / 10, 2)

    # Ensure they don't bet more than they have
    if bet < 0.01:
        st.warning("Too low of a bet, we are rounding up your bet to the minimum")
        bet = 0.01
    if bet > cash:
        st.warning("Woah there! You don't have that much cash right now. Looks like you're going all in")
        bet = cash

    # Rounding down the bet to 2 decimals
    bet = round(bet, 2)
    st.info(f"Bet= ${bet}")

    # Subtracting bet on the table from cash
    cash = round(cash - bet, 2)
    st.info(f"Remaining Money: ${cash}")

    # Returns both the adjusted cash and new bet
    return cash, bet
#===================== NEED TO FINISH THE INSTRUCTIONS FUNCTION===========================VVVVV
def show_instructions():
    """
    Display game instructions.
    """
    
    st.text("Get ready to play Blackjack! The goal of the game is to have a hand with a total score as close to 21 as possible without exceeding it.")

    st.text("Gameplay:")
    st.text("1. At the beginning of each round, youll be prompted to place a bet using a portion of your available cash.")
    st.text("2. The dealer will then shuffle the deck and deal two cards to you.")
    st.text("3. Your hands score is calculated based on the values of the cards. Number cards contribute their face value, face cards (J, Q, K) contribute 10, and Aces can be either 1 or 11.")
    st.text("4. You can choose to hit (receive an additional card) or stand (keep your current hand).")
    st.text("5. Be strategic in your decisions. If your total score exceeds 21, you bust, and the round is lost.")
    st.text("6. After you decide to stand, the dealer reveals their hand and follows a set of rules. The dealer will keep hitting until their hand is 17 or higher.")
    st.text("7. The winner of the round is the one with a hand closest to 21 without busting.")

    st.text("Scoring:")
    st.text("If you have an Ace and a 10-value card (10, J, Q, K) in your initial two cards, you have a blackjack and win the round instantly.")
 

def choose_difficulty(level):
    cash = 0
    level = level.lower()
    if level == 'hard':
        cash = 100
    elif level == 'medium':
        cash = 300
    elif level == 'easy':
        cash = 500
    
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
    
    choice = input("Do you want to split? Enter 'y' or 'n': ")
    if choice.lower() == 'y':
        cash = cash - bet
        for idx, new_hand in enumerate(new_hands):
            deck, h = shuffle_deal(deck,1)
            new_hand = [new_hand, h[0]]
            if can_split(new_hand, cash, bet):
                cash=split_pairs(new_hand, deck, cash, bet)
            else:
                print(f"\nPlaying Hand {idx + 1}: {new_hand}")
                print(f"Dealer Cards: [Face Down Card, {dealer_hand_before[1]}]")

                HS=score(new_hand)
                TS=score(dealer_hand_after)
                if HS == 21 and TS==21:
                    cash = cash + bet
                    I = 's'
                    print('It\'s a tie, you get your money back.')
                elif HS==21:
                    #Instant Win
                    I = 's'
                    jackpot_bet = (bet * 1.5) + bet
                    cash = cash + jackpot_bet
                    print(f"Black Jack! You Win ${jackpot_bet:.2f}!")
                else:
                    while True:
                        I = input("Decision time: enter s to stand or h to hit. Enter i for instructions or q to quit")
                        if type(I)!= str:
                            print("Invalid Input, please try again!.")
                            continue
                        if I=='i':
                            show_instructions()
                            continue

                        if I == 'h':
                            new_hand = player_hit(deck, new_hand)
                            print(f"Your Hand: {new_hand}")
                            HS=score(new_hand)
                            print(f"Your Score: {HS}")

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
                        cash = "Q"
                    
                    if busted==True:
                        print("Better luck next round!")
                        print(f"Remaining money: ${cash}")
                        cash = cash
                    else:
                        #Dealer play:
                        print(f"Dealer's Face Down Card was:{dealer_hand_before[0]}")

                        print("Table:", dealer_hand_before)
                        print("The Dealer Draws:")
                        print(f"Table Cards: {dealer_hand_after}")
                        cash = determine_winner(new_hand, dealer_hand_after, bet, cash)
        return cash
    else:
        return game(cash, deck, bet, hand)

def game(cash, deck, bet, hand):
    busted=False

    #FDC is the dealers facedown card, table is the dealer's face up card
    FDC=[]
    table=['Face Down Card']

    
    deck,f=shuffle_deal(deck,1)
    deck,t=shuffle_deal(deck,1)

    for i in f:
        FDC.append(i)
    for i in t:
        table.append(i)

    print(f"Your Hand: {hand}")
    print(f"Dealer Cards: {table}")


    
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
                show_instructions()
                continue

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

def start_game():
    st.title("Welcome to Pyjack!")

    round_number = 1

    while True:
        C = st.sidebar.radio("Select an option:", ["Start Game", "Instructions", "Quit"])
        
        if C == "Instructions":
            show_instructions()
        
        if C == "Quit":
            break

        if C == "Start Game":
            difficulty_level = st.sidebar.radio("Choose difficulty:", ["Easy", "Medium", "Hard"])

            cash = choose_difficulty(difficulty_level.lower())

            # Arbitrary Win limit, so the player can have a final victory
            limit = cash * 20

            while cash > 0:
                st.header(f"------------ Round {round_number} --------------------")
                Hearts = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
                Clubs = Hearts.copy()
                Spades = Hearts.copy()
                Diamonds = Hearts.copy()
                deck = Hearts + Clubs + Spades + Diamonds
                cash, bet = set_bet(cash)

                # Player's hand
                hand = []

                # Dealing cards
                deck, h = shuffle_deal(deck, 2)

                for i in h:
                    hand.append(i)

                if can_split(hand, cash, bet):
                    cash = split_pairs(hand, deck, cash, bet)
                else:
                    cash = game(cash, deck, bet, hand)

                # To ask players if they want another game
                A = st.sidebar.radio("Another Round?", ["Yes", "No"])
                if A == "No":
                    break

                if cash > limit:
                    st.success(f"You beat the house! Enjoy your (virtual) ${cash}")
                    break

                # This condition will hit if the player has just gone below 0
                if cash == 0:
                    st.warning(f"Money: ${cash}")
                    st.error("Tough Luck. You are out of cash. See you later!")
                    break

                # For those who quit in the middle of the game

            # This will catch players who just won/lost and those who quit
            st.info("Thanks for Playing! See you soon!")

start_game()


