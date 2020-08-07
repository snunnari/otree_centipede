from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import numpy as np
import random

author = 'Salvatore Nunnari, Bocconi University, salvatore.nunnari@unibocconi.it' \
    'Luca Congiu, Bocconi University, luca.congiu@unibocconi.it'

doc = """
oTree App for the Centipede Game as in McKelvey and Palfrey (1992), An Experimental Study of the Centipede Game, 
Econometrica, 60(4): 803-836.
"""


class Constants(BaseConstants):
    name_in_url = 'centipede'
    players_per_group = 2

    num_nodes = 4
    num_games = 3
    num_rounds = num_nodes * num_games

    first_rounds = np.arange(1,num_rounds,num_nodes)
    last_rounds = np.arange(num_nodes,num_rounds+1,num_nodes)

    large_pile = 0.40
    small_pile = 0.10
    base = 2

    large_piles = []
    small_piles = []

    for node in range(num_nodes + 1):
        large_piles.append(large_pile * base ** node)
        small_piles.append(small_pile * base ** node)


        # Vars for Instructions/Practice
        large_piles_practice = large_piles.copy()
        small_piles_practice = small_piles.copy()

        columns_range = range(4 + num_nodes)
        rounds_range = range(1, num_nodes + 1)

        # Merge the two Piles alternating elements
        payoff_red_practice = large_piles_practice.copy()
        for i in range(len(large_piles_practice)):
            if i % 2 != 0:
                payoff_red_practice[i] = small_piles_practice[i]

        # Merge the two Piles alternating elements
        payoff_blue_practice = small_piles_practice.copy()
        for i in range(len(payoff_blue_practice)):
            if i % 2 != 0:
                payoff_blue_practice[i] = large_piles_practice[i]

        # Matrix of moves and payoffs
        # --------------------------------------------------------------------------------
        # Table of moves for each game node
        movesList = ['P' for n in range(num_nodes)]
        movesMatrix = [movesList.copy()]

        for i in range(num_nodes):
            mc = movesList.copy()
            for j in range(num_nodes):
                if j <= i:
                    mc[i - j] = ''
                    mc[i] = 'T'
            mc.reverse()
            movesMatrix.append(mc)

        movesMatrix.reverse()

        # Zip variables needed for Instructions
        instructionsMatrix = list(zip(movesMatrix, large_piles_practice, small_piles_practice,
                                      payoff_red_practice, payoff_blue_practice))

class Subsession(BaseSubsession):

    game = models.IntegerField(initial=1)
    game_node = models.IntegerField(initial=1)

    def creating_session(self):

        for x in range(1,Constants.num_rounds+1):
            self.in_round(x).game = np.ceil(x/Constants.num_nodes)
            self.in_round(x).game_node = x - (np.ceil(x/Constants.num_nodes)-1)*Constants.num_nodes

        # shuffles players in groups randomly
        if self.round_number in Constants.first_rounds:
            self.group_randomly()
        else:
            x = Constants.first_rounds[int(np.ceil(self.round_number / Constants.num_nodes)) - 1]
            self.group_like_round(x)

        # shuffles players in groups randomly but keep players in fixed roles
        #if self.round_number in Constants.first_rounds:
        #    self.group_randomly(fixed_id_in_group=True)
        #else:
        #    x = Constants.first_rounds[int(np.ceil(self.round_number / Constants.num_nodes)) - 1]
        #    self.group_like_round(x)

        # shuffles players in groups as specified in matrix
        #if self.round_number == Constants.first_rounds[0]:
        #    new_structure = [[1, 2], [3, 4]]
        #    self.set_group_matrix(new_structure)
        #elif self.round_number == Constants.first_rounds[1]:
        #    new_structure = [[1, 3], [2, 4]]
        #    self.set_group_matrix(new_structure)
        #elif self.round_number == Constants.first_rounds[2]:
        #    new_structure = [[1, 4], [3, 2]]
        #    self.set_group_matrix(new_structure)
        #else:
        #    x = Constants.first_rounds[int(np.ceil(self.round_number / Constants.num_nodes)) - 1]
        #    self.group_like_round(x)

    def advance_game(self):
        for g in self.get_groups():
            if g.subsession.game < Constants.num_games:
                g.in_round(g.round_number + 1).game_on = True

class Group(BaseGroup):

    game_on = models.BooleanField(initial=True)
    game_outcome = models.IntegerField(initial=0)
    last_node = models.IntegerField(initial=1)

    def stop_game(self):
        players = self.get_players()
        takes = [p.take for p in players]
        if takes[0]:
            self.game_on = False
            self.game_outcome = 1
            self.last_node = self.subsession.game_node
        elif takes[1]:
            self.game_on = False
            self.game_outcome = 2
            self.last_node = self.subsession.game_node
        elif self.subsession.game_node == Constants.num_nodes and not any(takes):
            self.game_on = False
            self.last_node= self.subsession.game_node

        for group in self.in_rounds(self.round_number + 1, Constants.last_rounds[self.subsession.game-1]):
            group.game_on = self.in_round(self.round_number).game_on
            group.game_outcome = self.in_round(self.round_number).game_outcome
            group.last_node = self.in_round(self.round_number).last_node

    def set_payoffs(self):
        players = self.get_players()
        takes = [p.take for p in players]
        for p in self.get_players():
            if self.subsession.game_node == Constants.num_nodes and not any(takes):
                if p.id_in_group == 1:
                    p.payoff = c(Constants.large_piles[-1])
                else:
                    p.payoff = Constants.small_piles[-1]
            elif self.subsession.game_node < Constants.num_nodes and any(takes):
                if p.take:
                    p.payoff = c(Constants.large_piles[self.last_node - 1])
                else:
                    p.payoff = c(Constants.small_piles[self.last_node - 1])

class Player(BasePlayer):

    take = models.BooleanField(
        label='',
        widget=widgets.RadioSelectHorizontal,
    )
