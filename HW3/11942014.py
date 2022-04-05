
from poker import Hand, Pot
import tensorflow as tf
import numpy as np
import random


class shperry(Strategy):
    
    model = tf.keras.models.load_model('11942014_2.h5')
    choices={0:'check, fold or bet', 1:'call, raise, fold', 2:'call all-in or fold'}

    def decide_play(self, player, pot):


        # hand_strength, pot, already_bet, call_difference, players
        attribute_list = []
        hand_strength, rep, x, y = player.get_value()
        attribute_list.append(hand_strength)
        
        potTot = pot.total
        attribute_list.append(potTot)


        call_difference = player.to_play
        attribute_list.append(call_difference)

        num_players = len(pot.active_players)
        attribute_list.append(num_players)

        #have model predict from situation

        index = self.model.predict([attribute_list])
        maxI = max(index[0])

        i_old = np.where(index[0] == maxI)
        i = i_old[0][0]

        print("PREDICTION = ")
        print(i)

        num = random.randint(0,9)
        # if num % 2 == 1:
        #     if(self.choices[op].find("check") != -1):
        #         i = 2
        #     elif (self.choices[op].find("call") != -1):
        #         i = 3
        #     elif((self.choices[op].find("bet") != -1)):
        #         i = 4
        #     elif(self.choices[op].find("raise") != -1):
        #         i = 1
        # fold
        if i == 0:
            player.fold(pot)
        elif i == 1:
            # only raise by 25
            if(player.stack < 25):
                #if cant raise 25 go all in
                player.bet(pot,player.stack)
            else:
                player.bet(pot, 25)
        # check
        elif i == 2:
            player.check_call(pot)
        # call
        elif i == 3:
            player.check_call(pot)
        # bet
        elif i == 4:
            if(player.stack < 25):
                #if cant bet 25 go all in
                player.bet(pot,player.stack)
            else:
                # bet 25 if you want to bet
                player.bet(pot, 25)




    






