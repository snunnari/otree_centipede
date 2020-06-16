from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Variables for all pages
# --------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return dict(
        page=self.round_number
    )


# Define class of pages to be displayed only at first round
# --------------------------------------------------------------------------------
class FirstPage(Page):
    def is_displayed(self):
        return self.round_number == 1


# Pages to be displayed only at first round
# --------------------------------------------------------------------------------
class Welcome(FirstPage):
    pass


class Instructions(FirstPage):

    def vars_for_template(self):
        return dict(
            large_pile_practice=self.session.vars['large_pile_practice'],
            small_pile_practice=self.session.vars['small_pile_practice'],
            instructionsMatrix=self.session.vars['instructionsMatrix'],
            large_pile_practice_second=self.session.vars['large_pile_practice'][1],
            small_pile_practice_second=self.session.vars['small_pile_practice'][1],
            large_pile_practice_last=self.session.vars['large_pile_practice'][-2],
            small_pile_practice_last=self.session.vars['small_pile_practice'][-2],
            large_pile_practice_pass=self.session.vars['large_pile_practice'][-1],
            small_pile_practice_pass=self.session.vars['small_pile_practice'][-1],
            turns=int(Constants.num_rounds / 2)
        )


# Practice round 1
# --------------------------------------------------------------------------------
class Practice1Page1(FirstPage):

    form_model = 'player'

    def vars_for_template(self):
        return dict(
            large_pile_practice=self.session.vars['large_pile_practice'][0],
            small_pile_practice=self.session.vars['small_pile_practice'][0]
        )


class Practice1Page2(FirstPage):

    form_model = 'player'

    def vars_for_template(self):
        return dict(
            large_pile_practice=self.session.vars['large_pile_practice'][0],
            small_pile_practice=self.session.vars['small_pile_practice'][0]
        )


class Practice1Page3(FirstPage):

    form_model = 'player'

    def vars_for_template(self):
        return dict(
            large_pile_practice=self.session.vars['large_pile_practice'][1],
            small_pile_practice=self.session.vars['small_pile_practice'][1]
        )


class Practice1Page4(FirstPage):
    def vars_for_template(self):
        return dict(
            large_pile_practice=self.session.vars['large_pile_practice'][1],
            small_pile_practice=self.session.vars['small_pile_practice'][1]
        )


# Pages to be displayed at each round
# --------------------------------------------------------------------------------
class Decision(Page):

    form_model = 'player'
    form_fields = ['take']

    def is_displayed(self):
        if self.player.id_in_group == 1 and self.round_number % 2 != 0:
            return True
        if self.player.id_in_group == 2 and self.round_number % 2 == 0:
            return True
        else:
            return False

    def before_next_page(self):
        return self.group.stop_game(), self.group.set_payoffs()


# Wait pages
# --------------------------------------------------------------------------------
# class RegroupPage(WaitPage):
#     wait_for_all_groups = True
#
#     def is_displayed(self):
#         return self.subsession.round_number == 1
#
#     def after_all_players_arrive(self):
#
#         players = self.subsession.get_players()
#         import itertools
#
#         global matches
#         matches = [(1, 3), (2, 5), (4, 6)]
#         # matches = itertools.combinations(players, 2)
#
#         groups = []
#         for A, B in matches:
#             groups.append([players[A - 1], players[B - 1]])
#
#         self.subsession.set_group_matrix(groups)


class Wait(WaitPage):
    def after_all_players_arrive(self):
        pass


# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         pass


class Results(Page):
    def is_displayed(self):
        return not self.group.game_on or self.round_number == Constants.num_rounds


page_sequence = [#RegroupPage,
                 Welcome, Instructions,
                 Practice1Page1, Practice1Page2, Practice1Page3, Practice1Page4,
                 Decision, Wait, Results]
