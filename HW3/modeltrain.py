from asyncio.windows_events import NULL
import csv

from pokerhands import evaluate_hand
from poker import Card

'''
We only care about actions

array of actions given information and why did they choose action

http://kevinwang.us/lets-analyze-pluribuss-hands/
https://www.youtube.com/watch?v=yJm2l2Mh7nQ
https://keras.io/api
https://www.tensorflow.org/api_docs/python/tf

'''

error = []

class TurnAction:

    decision = -1
    evaluated_hand = 0
    pot_amount = 0
    already_bet = 0
    call_diff = 0
    num_players = 0

    '''
    everytime pluribus makes a move in game

    we create new turnaction and pass it to array

    dont care about hands
    '''

    def __init__(self, decision, evaluated_hand, pot_amount, already_bet, call_diff, num_players):
        self.decision = decision
        self.evaluated_hand = evaluated_hand
        self.pot_amount = pot_amount
        self.already_bet = already_bet
        self.call_diff = call_diff
        self.num_players = num_players

    def print_turn(self):
        print(self.decision)
        print(self.evaluated_hand)
        print(self.pot_amount)
        print(self.already_bet)
        print(self.call_diff)
        print(self.num_players)

    def listify(self):
        return [self.decision, self.evaluated_hand, self.pot_amount, self.already_bet, self.call_diff, self.num_players]
        





def append_cards_flop(line,cards):
    new_cards = []
    for card in cards:
        new_cards.append(card)

    rank = line[14]
    suit = line[15]
    if(rank == 'T'):
        rank = '10'
    new_cards.append(Card(rank,suit))

    rank = line[17]
    suit = line[18]
    if(rank == 'T'):
        rank = '10'
    new_cards.append(Card(rank,suit))

    rank = line[20]
    suit = line[21]
    if(rank == 'T'):
        rank = '10'
    new_cards.append(Card(rank,suit))

    return new_cards

def append_cards_turn_1(line, cards):
    new_cards = []
    for card in cards:
        new_cards.append(card)
    
    rank = line[25]
    suit = line[26]
    if(rank == 'T'):
        rank = '10'
    new_cards.append(Card(rank,suit))

    return new_cards

def append_cards_river(line, cards):
    new_cards = []
    for card in cards:
        new_cards.append(card)
    
    rank = line[31]
    suit = line[32]
    if(rank == 'T'):
        rank = '10'    
    new_cards.append(Card(rank,suit))

    return new_cards





def convert_hole_cards_and_eval(card):

    hole_cards = []

    rank = card[1]
    suit = card[2]

    if(rank == 'T'):
        rank = '10'
    new_card = Card(rank,suit)
    hole_cards.append(new_card)

    rank = card[4]
    suit = card[5]

    if(rank == 'T'):
        rank = '10'
    new_card = Card(rank,suit)
    hole_cards.append(new_card)

    rep, hand_val, tie_break, raw_data = evaluate_hand(hole_cards)

    return hole_cards, hand_val

"""
 fold: 0
 raise: 1
 check: 2
 call: 3
"""
def get_actions(input):
    if(input.find("folds") != -1):
        return 0
    elif(input.find("raises") != -1):
        return 1
    elif(input.find("checks") != -1):
        return 2
    elif(input.find("calls") != -1):
        return 3
    elif(input.find("bets") != -1):
        return 4
    
    return -1

def get_initial_bet(input): 
    if(input.find("small blind") != -1):
        return -50
    elif(input.find("big blind") != -1):
        return -100


def create_array_for_csv(input_file):

    actions = []
    cards = []
    file = open(input_file, "r")
    pot = 0
    bet_already = 0
    highest_bet = 0
    need_call = 0
    players = 6
    card_score = 0
    flop = False
    turn_1 = False
    turn_2 = False

    '''
    parse through file and update all until turn happens
    '''

    lines = []
    lines = file.readlines()

    for line in lines:
        # ONLY FOR 1 TURN

        # END OF HAND RESET ALL 
        if(line.find("SUMMARY") != -1):
            pot = 0
            cards = []
            bet_already = 0
            highest_bet = 0
            need_call = 0
            players = 6
            card_score = 0
            flop = False
            turn_1 = False
            turn_2 = False
            


        if(line.find("FLOP") != -1):
            flop = True
            cards = append_cards_flop(line, cards)

        if(line.find("TURN") != -1):
            turn_1 = True
            cards = append_cards_turn_1(line, cards)

        if(line.find("RIVER") != -1):
            turn_2 = True
            cards = append_cards_river(line, cards)

        #ONLY PLURIBUS NOT OTHERS
        if(line.find("Pluribus") != -1):
            if(flop == turn_1 == turn_2 == False):
                # HANDLES DEAL
                if(line.find("Dealt") != -1):
                    cards, card_score = convert_hole_cards_and_eval(line[18:])
             # HANDLES BIG/SMALL BLIND
                elif(get_actions(line) == -1):
                    if(line.find("big blind") != -1):
                        pot += 100
                        bet_already += 100
                    else:
                        pot += 50
                        bet_already +=50
                # IF NOT BLIND, DEALt, ITS ACTION
                else:
                    need_call = highest_bet - bet_already
                    rep, card_score, tie_break, raw_data = evaluate_hand(cards)
                    act = TurnAction(get_actions(line), card_score, pot, bet_already,need_call,players)

                    if(get_actions(line) == 1):
                        nums = [int(i) for i in line.split() if i.isdigit()]
                        raised = nums[0]
                        bet_already += raised
                        pot += raised + highest_bet
                        highest_bet += raised
                    elif(get_actions(line) == 3):
                        for i in line.split():
                            if i.isdigit():
                                pot += int(i)
                                bet_already += int(i)
                    error.append(line)
                    actions.append(act)
            elif(flop == True and (turn_1 == turn_2 == False) and get_actions(line) != -1):
                    rep, card_score, tie_break, raw_data = evaluate_hand(cards)
                    need_call = highest_bet - bet_already
                    act = TurnAction(get_actions(line), card_score, pot, bet_already,need_call,players)
                    if(get_actions(line) == 1):
                        nums = [int(i) for i in line.split() if i.isdigit()]
                        raised = nums[0]
                        bet_already += raised
                        pot += raised + highest_bet
                        highest_bet += raised
                    elif(get_actions(line) == 3):
                        for i in line.split():
                            if i.isdigit():
                                pot += int(i)
                                bet_already += int(i)

                    error.append(line)
                    actions.append(act)
            elif(flop == turn_1 == True and (turn_2 == False) and get_actions(line) != -1):
                    rep, card_score, tie_break, raw_data = evaluate_hand(cards)
                    need_call = highest_bet - bet_already
                    act = TurnAction(get_actions(line), card_score, pot, bet_already,need_call,players)
                    if(get_actions(line) == 1):
                        nums = [int(i) for i in line.split() if i.isdigit()]
                        raised = nums[0]
                        bet_already += raised
                        pot += raised + highest_bet
                        highest_bet += raised
                    elif(get_actions(line) == 3):
                        for i in line.split():
                            if i.isdigit():
                                pot += int(i)
                                bet_already += int(i)

                    error.append(line)
                    actions.append(act)
            elif(flop == turn_1 == turn_2 == True and get_actions(line) != -1):
                    rep, card_score, tie_break, raw_data = evaluate_hand(cards)
                    need_call = highest_bet - bet_already
                    act = TurnAction(get_actions(line), card_score, pot, bet_already,need_call,players)
                    if(get_actions(line) == 1):
                        nums = [int(i) for i in line.split() if i.isdigit()]
                        raised = nums[0]
                        bet_already += raised
                        pot += raised + highest_bet
                        highest_bet += raised
                    elif(get_actions(line) == 3):
                        for i in line.split():
                            if i.isdigit():
                                pot += int(i)
                                bet_already += int(i)

                    error.append(line)
                    actions.append(act)
        # OTHER PLAYERS ACTIONS
        # GET RID OF UNWANTED KNOWLEDGE
        # HANDLE BIG AND SMALL BLIND
        elif(line.find("big blind") != -1):
            pot += 100
            highest_bet = 100
        elif(line.find("small blind") != -1):
            pot += 50
        # if no actions on line we dont care
        elif(get_actions(line) == -1):
            print(line)
        elif(get_actions(line) == 0):
            players -= 1
        elif(get_actions(line) == 1):
            nums = [int(i) for i in line.split() if i.isdigit()]
            raised = nums[0]
            pot += raised + highest_bet
            highest_bet += raised
        elif(get_actions(line) == 3):
            # nums = [int(i) for i in line.split() if i.isdigit()]
            # calls = nums
            # pot += calls
            for i in line.split():
                if i.isdigit():
                    pot += int(i)
        elif(get_actions(line) == 4):
            nums = [int(i) for i in line.split() if i.isdigit()]
            bet = nums[0]
            if(bet > highest_bet):
                highest_bet = bet
            pot += bet
    return actions
        
            



                



    











'''
    parsing files and creating final files

'''    

def get_pluribus_moves(input):

    if(input.find("PokerStars") == -1 and input.find("Table") == -1 and input.find("Seat") == -1):
        return input
    
    return NULL
    

        
path = "pluribus_all.txt"

# f = open("pluribus_all.txt","a")

# AllFiles = os.listdir()
# StrTxt = "pluribus"
# for TxtFile in AllFiles:
#     if (TxtFile.__contains__(StrTxt) and TxtFile != "pluribus_all.txt"):
#         print(TxtFile)
#         fileObject = open(TxtFile,"r")
#         data = fileObject.read()
#         f.write(data)
#         fileObject.close()

# f.close()

actions = create_array_for_csv(path)

print(len(actions))

f = open("actions.csv", "w")

writer = csv.writer(f)

header = ["Decision", "Hand Strength", "Pot", "Already Bet", "Call Difference", "Players"]
writer.writerow(header)

for action in actions:
    l = action.listify()
    writer.writerow(l)

f.close()









    



