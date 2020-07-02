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
    name_in_url = 'centipede_SN'
    players_per_group = 2

    num_nodes = 4
    num_games = 3
    num_rounds = num_nodes * num_games

    large_pile = c(0.40)
    small_pile = c(0.10)
    base = 2

class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:

            #self.session.vars['game_off_num'] = 0
            self.session.vars['large_piles'] = []
            self.session.vars['small_piles'] = []

            for node in range(Constants.num_nodes + 1):
                self.session.vars['large_piles'].append(c(Constants.large_pile * Constants.base ** node))
                self.session.vars['small_piles'].append(c(Constants.small_pile * Constants.base ** node))

            for p in self.get_players():
                p.participant.vars['game'] = 1
                p.participant.vars['game_node'] = 1

    def advance_game(self):
        print(self.get_group_matrix())
        new_structure = [[4, 1], [2, 3]]
        self.set_group_matrix(new_structure)
        print(self.get_group_matrix())

        for p in self.get_players():
            if p.participant.vars['game'] < Constants.num_games:
                p.participant.vars['game'] += 1
                p.participant.vars['game_node'] = 1
        for g in self.get_groups():
            g.game_on = True

class Group(BaseGroup):

    game_on = models.BooleanField(initial=True)

    def stop_game_or_advance_node(self):
        for p in self.get_players():
            if p.take or p.participant.vars['game_node'] == Constants.num_nodes:
                self.game_on = False
                #self.session.vars['game_off_num'] += 1
            else:
                p.participant.vars['game_node'] += 1

    def set_payoffs(self):
        for p in self.get_players():
            if p.participant.vars['game_node'] == Constants.num_nodes:
                if p.id_in_group == 1:
                    p.payoff = p.session.vars['large_piles'][-1]
                else:
                    p.payoff = p.session.vars['small_piles'][-1]
            elif not self.game_on:
                if p.take:
                    p.payoff = self.session.vars['large_piles'][p.participant.vars['game_node'] - 1]
                else:
                    p.payoff = self.session.vars['small_piles'][p.participant.vars['game_node'] - 1]

class Player(BasePlayer):

    take = models.BooleanField(
        label='',
        widget=widgets.RadioSelectHorizontal,
    )
