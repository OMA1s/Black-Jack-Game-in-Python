# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
dealer_value = "???"
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    
outcome = ""
# initialize some useful global variables
in_play = False
Value_message = ""
outcome = ""
win = 0
loss = 0
score = 0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    def hide(self,canvas,pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0]*0, 
                    CARD_CENTER[1] + CARD_SIZE[1]*0)
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        

# define hand class
class Hand:
    def __init__(self):
        self.hand = []
        pass	# create Hand object

    def __str__(self):
        my_string = "Hand contains "
        for cards in self.hand:
            my_string += cards.get_rank()+cards.get_suit() + " "
        return my_string
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value = 0
        hand_rank = []
        for card in self.hand:
            value += VALUES[card.get_rank()]
            hand_rank.append(card.get_rank())
        if 'A' not in hand_rank:
            return value
        else:
            if value + 10 <= 21:
                return (value + 10)
            else:
                return value
            
   
    def draw(self, canvas, pos):
        for cards in self.hand:
            cards.draw(canvas,pos)
            pos[0] += 70
    def hide(self,canvas,pos):
        for cards in self.hand:
            cards.hide(canvas,pos)
            
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                mycard = Card(suit,rank)
                self.deck.append(mycard)
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        string = "Deck contains: "
        for cards in self.deck:
            string += (cards.get_suit()+cards.get_rank() + " ")
        return string


#define event handlers for buttons
def deal():
    global outcome, in_play, mydeck, player_hand, dealer_hand, score, win, loss, dealer_value
    if in_play:
        Outcome = "Player lost the game!"
        loss += 1
    dealer_value = "???"
    outcome = ""
    mydeck = Deck()
    mydeck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(mydeck.deal_card())
    player_hand.add_card(mydeck.deal_card())
    dealer_hand.add_card(mydeck.deal_card())
    dealer_hand.add_card(mydeck.deal_card())
    in_play = True
    print "The Player " +str(player_hand) + "of VALUE: " + str(player_hand.get_value())
    print "The dealer " +str(dealer_hand) + "of VALUE: " + str(dealer_hand.get_value())

def hit():
    global outcome, loss, win, score, in_play, dealer_value
    if in_play == False:
        return None
    if player_hand.get_value()<21:
        player_hand.add_card(mydeck.deal_card())
    if player_hand.get_value()>21:    
        outcome = "YOU ARE BUSTED! The Dealer wins"
        dealer_value = str(dealer_hand.get_value())
        loss += 1
        in_play = False
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, win, loss, score, in_play, dealer_value
    dealer_value = str(dealer_hand.get_value())
    if in_play == False:
        return None
    if player_hand.get_value()>21:
        print "You are already busted!"
    else:
        while dealer_hand.get_value() <17:
            dealer_hand.add_card(mydeck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = ("The Dealer has BUSTED! Player wins!")
            win += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = ("The Dealer has won!")
            loss += 1
        else:
            outcome = ("The Player has won!")
            win += 1
    in_play = False
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    global in_play, score, win, loss, outcome, dealer_value
    # test to make sure that card.draw works, replace with your code below
    score = win - loss
    player_hand.draw(canvas, [0,0])
    dealer_hand.draw(canvas, [0, 100])
    if in_play == True:
        dealer_hand.hide(canvas, [0,100])
    Value_message = "The Player hand's value is "+str(player_hand.get_value())+" and The Dealer hand's value is "+dealer_value
                                                 
    canvas.draw_text(Value_message, [0,300], 20,'Black')
    canvas.draw_text("Hit or Stand? Or new Deal?", [0,350], 20,'Black')
    canvas.draw_text(outcome, [0,400], 20,'Black')
    canvas.draw_text("WELCOME TO BLACKJACK!!!", [300,50], 20,'Red')
    canvas.draw_text("Current score: " + str(score), [300,100], 20,'Red') 

        

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# remember to review the gradic rubric

# Test code
###################################################
# Test code
