
# %%
import streamlit as st
import random


def shuffle_deal(deck, n):
    pile = []
    random.shuffle(deck)
    for i in range(0, n):
        pile.append(deck[0])
        deck.remove(deck[0])
    return (deck, pile)

def score(cards_input):
    score = 0
    aces = 0

    for card in cards_input:
        if card == "A":
            aces += 1
            score += 11
        elif card in ['J', 'Q', 'K']:
            score += 10
        else:
            score += card

    while aces > 0 and score > 21:
        score -= 10
        aces -= 1
    return score

def set_bet(cash):
    # bet = st.number_input(f"""How much of your ${cash} do you want to bet on this round (minimum $0.01)?""",
    #                       min_value=0.01, value=float(cash)//10)
    st.markdown(f"How much do you want to bet on this round (minimum $0.01)? Remaining Cash: {cash}")
    bet = st.number_input("", min_value=0.01, value=float(cash) // 10)
    if bet > cash:
        st.warning("Woah there! You don't have that much Cash right now. Looks like you're going all in.")
        bet = cash

    bet = round(bet, 2)
    st.write(f"Bet = ${bet}")

    cash = round(cash - bet, 2)
    st.write(f"Remaining Money: ${cash}")

    return cash, bet


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
 

def choose_difficulty():
    difficulty_level = st.radio("Choose difficulty:", ["Easy", "Medium", "Hard"])
    cash = 0

    if difficulty_level == 'Hard':
        cash = 100
    elif difficulty_level == 'Medium':
        cash = 300
    elif difficulty_level == 'Easy':
        cash = 500

    return cash

def player_hit(deck, hand):
    deck, h = shuffle_deal(deck, 1)
    hand.append(h[0])
    return hand

def dealer_play(deck, dealer_hand):
    while score(dealer_hand) < 17:
        dealer_hand = player_hit(deck, dealer_hand)
    return dealer_hand


def determine_winner(player_hand, dealer_hand, bet, cash):
    player_score = score(player_hand)
    dealer_score = score(dealer_hand)

    if player_score > 21:
        st.write("Player busts! Dealer wins.")
        return cash

    if dealer_score > 21:
        st.write(f"Dealer is busted. You win ${bet}")
        return cash + 2 * bet

    if player_score == dealer_score:
        st.write("It's a tie. You got your bet back")
        return cash + bet

    if player_score > dealer_score:
        st.write(f"You Win! You won ${bet}")
        return cash + 2 * bet

    st.write("The Dealer won! Better luck next time...")
    st.write(f"Remaining Cash: ${cash}")
    return cash

def double_down(deck, hand, bet, cash):
    # Your existing code for doubling down remains the same
    pass

def can_split(hand, remaining_cash, bet):
    return len(hand) == 2 and hand[0] == hand[1] and remaining_cash >= bet

def split_pairs(hand, deck, cash, bet):
    deck,dealer_hand_before=shuffle_deal(deck,2) # Dealer hand (one face down and one face up)
    new_hands = [hand[0], hand[1]]  # Split the hand into two separate hands
    dealer_hand_after = dealer_play(deck, dealer_hand_before)
    busted = False
    
    choice = st.radio("Do you want to split?", ["Yes", "No"])
    if choice.lower() == 'y':
        cash = cash - bet
        for idx, new_hand in enumerate(new_hands):
            deck, h = shuffle_deal(deck,1)
            new_hand = [new_hand, h[0]]
            if can_split(new_hand, cash, bet):
                cash=split_pairs(new_hand, deck, cash, bet)
            else:
                st.write(f"\nPlaying Hand {idx + 1}: {new_hand}")
                st.write(f"Dealer Cards: [Face Down Card, {dealer_hand_before[1]}]")

                HS=score(new_hand)
                TS=score(dealer_hand_after)
                if HS == 21 and TS==21:
                    cash = cash + bet
                    I = 's'
                    st.write('It\'s a tie, you get your money back.')
                elif HS==21:
                    #Instant Win
                    I = 's'
                    jackpot_bet = (bet * 1.5) + bet
                    cash = cash + jackpot_bet
                    st.write(f"Black Jack! You Win ${jackpot_bet:.2f}!")
                else:
                    while True:
                        I = st.radio("Decision time:", ["Stand", "Hit", "Instructions", "Quit"])
                        if type(I)!= str:
                            st.write("Invalid Input, please try again!.")
                            continue
                        if I=='i':
                            show_instructions()
                            continue

                        if I == 'h':
                            new_hand = player_hit(deck, new_hand)
                            st.write(f"Your Hand: {new_hand}")
                            HS=score(new_hand)
                            st.write(f"Your Score: {HS}")

                            if HS>21:
                                st.write("You're busted")
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
                        st.write("Better luck next round!")
                        st.write(f"Remaining money: ${cash}")
                        cash = cash
                    else:
                        #Dealer play:
                        st.write(f"Dealer's Face Down Card was:{dealer_hand_before[0]}")

                        st.write("Table:", dealer_hand_before)
                        st.write("The Dealer Draws:")
                        st.write(f"Table Cards: {dealer_hand_after}")
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

    st.write(f"Your Hand: {hand}")
    st.write(f"Dealer Cards: {table}")


    
    initial_numeric_hand = score(hand)

    if initial_numeric_hand is not None and initial_numeric_hand in [9, 10, 11]:
        double_down(deck, hand, bet, cash)

    HS=score(hand)
    TS=score(table[1:])+score(FDC)
    if HS == 21 and TS==21:
        cash= cash+bet
        st.write('It\'s a tie, you get your money back.')
        return cash
    elif HS==21:
        #Instant Win
        I = 's'
        jackpot_bet = (bet * 1.5) + bet
        cash = cash + jackpot_bet
        st.write(f"Black Jack! You Win ${jackpot_bet:.2f}!")
        return cash
    else:
        st.write(f"Your Score: {HS}")
        st.write(f"Your bet: ${bet}")
        #This is where the player can choose to stand or hit (or get instructions/ quit)
        while True:
            I = input("Decision time: enter s to stand or h to hit. Enter i for instructions or q to quit")
            if type(I)!= str:
                st.write("Invalid Input, please try again!.")
                continue
            if I=='i':
                show_instructions()
                continue

            if I == 'h':
                hand = player_hit(deck, hand)
                st.write(f"Your Hand: {hand}")
                HS=score(hand)
                st.write(f"Your Score: {HS}")

                if HS>21:
                    st.write("You're busted")
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
            st.write("Better luck next round!")
            st.write(f"Remaining money: ${cash}")
            return cash
        else:
            #Dealer play:
            st.write(f"Dealer's Face Down Card was:{FDC[0]}")

            table=table[1:]
            table.append(FDC[0])

            st.write("Table:", table)
            # TS=score(table)

            #This is to force the dealer to draw
            table = dealer_play(deck, table)
            st.write("The Dealer Draws:")
            st.write(f"Table Cards: {table}")
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
            cash = choose_difficulty()

            limit = cash * 20

            while cash > 0:
                st.header(f" Round {round_number} ")
                Hearts = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
                Clubs = Hearts.copy()
                Spades = Hearts.copy()
                Diamonds = Hearts.copy()
                deck = Hearts + Clubs + Spades + Diamonds
                cash, bet = set_bet(cash)
                hand = []
                deck, h = shuffle_deal(deck, 2)

                for i in h:
                    hand.append(i)

                if can_split(hand, cash, bet):
                    cash = split_pairs(hand, deck, cash, bet)
                else:
                    cash = game(cash, deck, bet, hand)

                A = st.sidebar.radio("Another Round?", ["Yes", "No"])
                if A == "No":
                    break

                if cash > limit:
                    st.success(f"You beat the house! Enjoy your (virtual) ${cash}")
                    break

                if cash == 0:
                    st.warning(f"Money: ${cash}")
                    st.error("Tough Luck. You are out of cash. See you later!")
                    break

            st.info("Thanks for Playing! See you soon!")

start_game()

