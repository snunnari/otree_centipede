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

author = 'Luca Congiu, Bocconi University, luca.congiu@unibocconi.it' \
         'Salvatore Nunnari, Bocconi University, salvatore.nunnari@unibocconi.it'

doc = """
oTree App for the Centipede Game as in McKelvey and Palfrey (1992), An Experimental Study of the Centipede Game, 
Econometrica, 60(4): 803-836.
"""


class Constants(BaseConstants):
    name_in_url = 'otree_centipede'
    players_per_group = 2

    # Laboratory experiment
    # If "False", instructions pertaining to a laboratory setting will be omitted
    # (e.g., "...raise your hand, and an experimenter will come and assist you.")
    # --------------------------------------------------------------------------------
    lab = True

    # Number of rounds (or game nodes)
    # --------------------------------------------------------------------------------
    num_rounds = 6

    # Initial Piles
    # --------------------------------------------------------------------------------
    large_pile = c(0.40)
    small_pile = c(0.10)

    # Base of payoff multiplier
    # --------------------------------------------------------------------------------
    base = 2

    # Vars for Instructions
    # --------------------------------------------------------------------------------
    columns_range = range(4 + num_rounds)
    rounds_range = range(1, num_rounds + 1)


class Subsession(BaseSubsession):

    def creating_session(self):

        rounds = Constants.num_rounds
        #self.get_players()
        #print(self.get_players())
        #print(type(self.get_players()[0]))

        # Group players randomly
        # --------------------------------------------------------------------------------
        #self.group_randomly(fixed_id_in_group=True)
        #print(self.get_group_matrix())

        # Deprecated?
        # --------------------------------------------------------------------------------
        # from otree import matching
        #
        # def before_session_starts(self):
        #     self.set_group_matrix(matching.round_robin(self))

        # Compute Large and Small Piles based on game node
        # --------------------------------------------------------------------------------
        base = Constants.base
        large_pile = Constants.large_pile * base ** (self.round_number - 1)
        small_pile = Constants.small_pile * base ** (self.round_number - 1)

        print(f"In round {self.round_number}, Large Pile is {large_pile}, Low prize is {small_pile}, "
              f"Multiplier is {base ** (self.round_number - 1)}.")

        # Compute Large and Small Piles if last round is reached and no player "takes"
        # --------------------------------------------------------------------------------
        large_pile_pass = Constants.large_pile * base ** rounds
        small_pile_pass = Constants.small_pile * base ** rounds

        if self.round_number == rounds:
            print(f"If nobody takes in round {self.round_number}, "
                  f"Player 1 gets {large_pile_pass} and Player 2 gets {small_pile_pass}.")

        # Assign Large and Small Piles variables to player's fields
        # --------------------------------------------------------------------------------
        for p in self.get_players():
            p.large_pile = large_pile
            p.small_pile = small_pile
            p.large_pile_pass = large_pile_pass
            p.small_pile_pass = small_pile_pass

        # Create list of Large and Small Piles for Practice
        # --------------------------------------------------------------------------------
        if self.round_number == 1:
            self.session.vars['large_pile_practice'] = [c(large_pile)]
            self.session.vars['small_pile_practice'] = [c(small_pile)]
        else:
            self.session.vars['large_pile_practice'].append(c(large_pile))
            self.session.vars['small_pile_practice'].append(c(small_pile))

        # Adding payoff in case players pass in all rounds
        if self.round_number == Constants.num_rounds:
            self.session.vars['large_pile_practice'].append(c(large_pile_pass))
            self.session.vars['small_pile_practice'].append(c(small_pile_pass))

            print(f"For Practice, list of Large Pile is: {self.session.vars['large_pile_practice']}")
            print(f"For Practice, list of Small Pile is: {self.session.vars['small_pile_practice']}")

        large_pile_practice = self.session.vars['large_pile_practice']
        small_pile_practice = self.session.vars['small_pile_practice']

        # Create list of payoffs based on moves for Practice
        # --------------------------------------------------------------------------------
        payoff_red_practice = large_pile_practice.copy()
        for i in range(len(large_pile_practice)):
            if i % 2 != 0:
                payoff_red_practice[i] = small_pile_practice[i]
        print(payoff_red_practice)

        payoff_blue_practice = small_pile_practice.copy()
        for i in range(len(payoff_blue_practice)):
            if i % 2 != 0:
                payoff_blue_practice[i] = large_pile_practice[i]
        print(payoff_blue_practice)

        # Matrix of moves and payoffs for Instructions
        # --------------------------------------------------------------------------------
        # Table of moves for each round
        movesList = ['P' for p in range(rounds)]
        movesMatrix = [movesList.copy()]
        for i in range(rounds):
            mc = movesList.copy()
            for j in range(rounds):
                if j <= i:
                    mc[i - j] = ''
                    mc[i] = 'T'
            mc.reverse()
            movesMatrix.append(mc)

        movesMatrix.reverse()

        # Zip variables needed for Instructions
        instructionsMatrix = list(zip(movesMatrix, large_pile_practice, small_pile_practice,
                                      payoff_red_practice, payoff_blue_practice))
        self.session.vars['instructionsMatrix'] = instructionsMatrix
        print(instructionsMatrix)


class Group(BaseGroup):

    # Game on
    # Set to False when a player "takes", in which case the game stops
    # --------------------------------------------------------------------------------
    game_on = models.BooleanField(initial=True)

    # Stop game
    # If a player "takes", "game on" variable is set to False
    # --------------------------------------------------------------------------------
    def stop_game(self):
        for p in self.get_players():
            if p.take:
                self.game_on = False
                print('A player decided to take. Game terminated.')

    # Players' payoff
    # --------------------------------------------------------------------------------
    def set_payoffs(self):
        for p in self.get_players():

            # Payoff when a player "takes"
            if not self.game_on:
                if p.take:
                    p.payoff = p.large_pile
                else:
                    p.payoff = p.small_pile
                print(f"Player Final payoff: {p.payoff}")

            # Payoff if all rounds are played and no player "takes"
            elif self.round_number == Constants.num_rounds:
                if p.id_in_group == 1:
                    p.payoff = p.large_pile_pass
                else:
                    p.payoff = p.small_pile_pass
                print(f"Player {p.id_in_group}'s final payoff: {p.payoff}")


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
