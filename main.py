import random

SUITS = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
RANKS = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
VALUES = {rank: min(index + 2, 10) if rank != 'Ace' else 11 for index, rank in enumerate(RANKS)}
playing = True

# Card class to represent individual cards
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Deck class to create and manage the deck of cards
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Hand class to manage cards and calculate their value
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Chips class to manage betting chips
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# Function to take the player's bet
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                break
        except ValueError:
            print('Please enter a valid number.')

# Deal a card to the player or dealer
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Ask the player to hit or stand
def hit_or_stand(deck, hand):
    global playing
    while True:
        choice = input("Would you like to Hit or Stand? (h/s): ").lower()
        if choice == 'h':
            hit(deck, hand)
        elif choice == 's':
            print("Player stands. Dealer's turn.")
            playing = False
        else:
            print("Invalid input. Please enter 'h' or 's'.")
            continue
        break

# Show cards, hiding the dealer's first card
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

# Show all cards
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Total Value:", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Total Value:", player.value)

# Scenarios for winning and losing
def player_busts(chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("It's a tie!")

# Game loop
while True:
    print('Welcome to Reporanger 2005! Get as close to 21 as possible without going over.')
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()
    take_bet(player_chips)
    show_some(player_hand, dealer_hand)

    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        show_all(player_hand, dealer_hand)
        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    print(f"Player's total chips: {player_chips.total}")
    if input("Play again? (y/n): ").lower() != 'y':
        print("Thanks for playing!")
        break
