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

    # --------------------------------------------------------------------------------
    # Experiment settings
    # --------------------------------------------------------------------------------

    # Is it a Laboratory experiment?
    # If "False", instructions pertaining to a laboratory setting will be omitted
    # (e.g., "...raise your hand, and an experimenter will come and assist you.")
    # --------------------------------------------------------------------------------
    lab = True

    # Random paying games
    # If True, one or more games will be randomly selected to determine player's payoff in the experiment
    # TODO: implement payoff mechanism
    random_paying_games = False

    # --------------------------------------------------------------------------------
    # Number of nodes, games, and rounds
    # --------------------------------------------------------------------------------

    # Number of game nodes
    num_nodes = 4

    # Number of games
    #num_games = np.random.geometric(0.5, size=100)
    #num_games = np.random.randint(2, 4)
    num_games = 3

    # Number of rounds
    # Total number of rounds has to be a multiple of number of nodes
    # --------------------------------------------------------------------------------
    num_rounds = num_nodes * num_games
    # --------------------------------------------------------------------------------

    # Number of games to be randomly selected for payment (from 1 to num_games)
    # This setting works only if random_paying_games is True
    # --------------------------------------------------------------------------------
    num_paying_games = 1
    # --------------------------------------------------------------------------------

    # Check that num_paying_games <= num_games
    # --------------------------------------------------------------------------------
    if num_paying_games > num_games:
        print('Error in App "centipede": Number of paying games exceeds the total number of games. '
              'Please, make sure that num_paying_games <= num_games in Constants.'
              )
        exit()

    # --------------------------------------------------------------------------------
    # Piles and related variables
    # --------------------------------------------------------------------------------

    # Initial Piles
    # --------------------------------------------------------------------------------
    large_pile = c(0.40)
    small_pile = c(0.10)

    # Base of payoff multiplier
    # --------------------------------------------------------------------------------
    base = 2

    # Vars for Instructions
    # --------------------------------------------------------------------------------
    columns_range = range(4 + num_nodes)
    rounds_range = range(1, num_nodes + 1)


class Subsession(BaseSubsession):

    def creating_session(self):

        # --------------------------------------------------------------------------------
        # Operations to be performed at round 1
        # --------------------------------------------------------------------------------
        if self.round_number == 1:

            # Assigning variables from Constants
            # --------------------------------------------------------------------------------
            nodes = Constants.num_nodes
            games = Constants.num_games
            rounds = Constants.num_rounds

            large_pile = Constants.large_pile
            small_pile = Constants.small_pile

            print(f"This session has {rounds} rounds.")
            print(f"This session has {games} games.")

            # Set session paying round(s) randomly at round 1
            # ----------------------------------------------------
            if Constants.random_paying_games:

                paying_games = [i for i in range(1, Constants.num_games + 1)]
                for j in range(0, Constants.num_games + 1 - (Constants.num_paying_games + 1)):
                    random_item_from_list = np.random.choice(paying_games)
                    paying_games.remove(random_item_from_list)
                print(f"Rounds selected for payment: {paying_games}")

                # assign list of paying rounds and create list of payoffs to sum at the end
                for p in self.get_players():
                    p.participant.vars['paying_games'] = paying_games
                    p.participant.vars['payoffs_list'] = []

                print(f"This session's paying game(s) are {paying_games}.")

            # --------------------------------------------------------------------------------
            # Create list of Large and Small Piles
            # --------------------------------------------------------------------------------

            # Compute Large and Small Piles
            # --------------------------------------------------------------------------------
            self.session.vars['large_piles'] = []
            self.session.vars['small_piles'] = []

            base = Constants.base

            for node in range(nodes + 1):
                self.session.vars['large_piles'].append(c(large_pile * base ** node))
                self.session.vars['small_piles'].append(c(small_pile * base ** node))

                # print(f"Multiplier is {base ** node}. \n"
                #       f"Large Piles: {self.session.vars['large_piles']}, \n"
                #       f"Small Piles: {self.session.vars['small_piles']}."
                #       )

            # Assign vars to session attributes
            large_piles = self.session.vars['large_piles']
            small_piles = self.session.vars['small_piles']

            # --------------------------------------------------------------------------------
            # Vars for Instructions/Practice
            # --------------------------------------------------------------------------------

            # Create list of payoffs for Practice
            # --------------------------------------------------------------------------------
            large_piles_practice = large_piles.copy()
            small_piles_practice = small_piles.copy()

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
            movesList = ['P' for p in range(nodes)]
            movesMatrix = [movesList.copy()]

            for i in range(nodes):
                mc = movesList.copy()
                for j in range(nodes):
                    if j <= i:
                        mc[i - j] = ''
                        mc[i] = 'T'
                mc.reverse()
                movesMatrix.append(mc)

            movesMatrix.reverse()

            # Zip variables needed for Instructions
            instructionsMatrix = list(zip(movesMatrix, large_piles_practice, small_piles_practice,
                                          payoff_red_practice, payoff_blue_practice))
            self.session.vars['instructionsMatrix'] = instructionsMatrix

            # Assign initial Large and Small Pile to player's fields
            # --------------------------------------------------------------------------------
            for p in self.get_players():
                p.large_pile = large_piles[0]
                p.small_pile = small_piles[0]

                # Assign Game and Game Node variables
                # ----------------------------------------------------------------------------
                p.participant.vars['game'] = 1
                p.participant.vars['game_node'] = 1

    # --------------------------------------------------------------------------------
    # Other functions
    # --------------------------------------------------------------------------------

    # Shuffle players before each game
    # --------------------------------------------------------------------------------
    def shuffle_players(self):

        for p in self.get_players():

            if p.participant.vars['game'] == 2:
                new_structure = [[1, 3], [2, 4]]
                self.set_group_matrix(new_structure)

            elif p.participant.vars['game'] == 3:
                new_structure = [[3, 2], [4, 1]]
                self.set_group_matrix(new_structure)

        print(self.get_group_matrix())


        # Get players list
        # group_matrix_start = self.get_group_matrix()
        # print(group_matrix_start)
        #
        # players = self.get_players()
        # players_indices = set(j for j in range(1, len(players) + 1))
        #
        # # Match players randomly
        # matches = []
        #
        # while players_indices:
        #     pairs = random.sample(players_indices, 2)
        #     matches.append(pairs.copy())
        #     players_indices -= set(pairs)
        #
        # # Set groups for following game
        # group_matrix = []
        # for A, B in matches:
        #     group_matrix.append([players[A - 1], players[B - 1]])
        #
        # self.set_group_matrix(matches)
        # print(group_matrix)
        # print("Regrouping performed.")


class Group(BaseGroup):

    # Game on
    # Controls whether game has to continue (True) or to stop (False)
    # --------------------------------------------------------------------------------
    game_on = models.BooleanField(initial=True)

    game = models.IntegerField()

    # Stop game
    # If a player "takes" or all rounds are passed on
    # --------------------------------------------------------------------------------
    def stop_game(self):

        for p in self.get_players():
            if p.take or p.participant.vars['game_node'] == Constants.num_nodes:
                self.game_on = False
                print(f"Game node {p.participant.vars['game_node']}. \
                 Game terminated. Game on set to {self.game_on}")

    # Update game node as rounds pass
    # --------------------------------------------------------------------------------
    def set_game_node(self):

        for p in self.get_players():
            if self.game_on:
                p.participant.vars['game_node'] += 1

            print(f"Group game node is: {p.participant.vars['game_node']}")

    # Set game number
    # --------------------------------------------------------------------------------
    def set_game(self):

        for p in self.get_players():

            if p.participant.vars['game'] <= Constants.num_games:
                if not self.game_on:

                    # Update game number
                    p.participant.vars['game'] += 1
                    self.game = p.participant.vars['game']
                    print(f"Game number {self.game}, {p.participant.vars['game']} out of {Constants.num_games}")

    # Repeat game
    # --------------------------------------------------------------------------------
    def repeat_game(self):
        for p in self.get_players():

            # if p.take or p.participant.vars['game_node'] == Constants.num_nodes:

            # Reset game node to 1
            p.participant.vars['game_node'] = 1
            print(f"Game node reset to {p.participant.vars['game_node']}")

    # Players' payoffs
    # --------------------------------------------------------------------------------
    def set_payoffs(self):

        if not self.game_on:

            for p in self.get_players():

                # Payoff when a player "takes"
                if p.take:
                    p.payoff = self.session.vars['large_piles'][p.participant.vars['game_node'] - 1]
                else:
                    p.payoff = self.session.vars['small_piles'][p.participant.vars['game_node'] - 1]
                print(f"Player {p.id_in_group} Final payoff is take: {p.payoff}")

                # Payoff if all rounds are played and no player "takes"
                if p.participant.vars['game_node'] >= Constants.num_nodes:
                    if p.id_in_group == 1:
                        p.payoff = p.session.vars['large_piles'][-1]
                    else:
                        p.payoff = p.session.vars['small_piles'][-1]
                    print(f"Player {p.id_in_group}'s final payoff if pass: {p.payoff}")


class Player(BasePlayer):

    # Has player taken the Large Pile?
    # --------------------------------------------------------------------------------
    take = models.BooleanField(
        label='',
        widget=widgets.RadioSelectHorizontal,
    )

    take_practice = models.BooleanField(
        label='',
        widget=widgets.RadioSelectHorizontal,
    )

    # Player's fields
    # --------------------------------------------------------------------------------
    small_pile = models.CurrencyField()
    large_pile = models.CurrencyField()

    large_pile_pass = models.CurrencyField()
    small_pile_pass = models.CurrencyField()
