from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Variables for all pages
# --------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return dict(
        game_on=self.group.game_on,
        game=self.participant.vars['game'],
        previous_game=self.participant.vars['game'] - 1,
        game_node=self.participant.vars['game_node'],

        large_pile_practice=self.session.vars['large_piles'],
        small_pile_practice=self.session.vars['small_piles'],

        large_pile_practice_second=self.session.vars['large_piles'][1],
        small_pile_practice_second=self.session.vars['small_piles'][1],
        large_pile_practice_third=self.session.vars['large_piles'][2],
        small_pile_practice_third=self.session.vars['small_piles'][2],

        large_pile_practice_last=self.session.vars['large_piles'][-2],
        small_pile_practice_last=self.session.vars['small_piles'][-2],
        large_pile_practice_pass=self.session.vars['large_piles'][-1],
        small_pile_practice_pass=self.session.vars['small_piles'][-1]
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
            turns=int(Constants.num_rounds / 2),
            instructionsMatrix=self.session.vars['instructionsMatrix']
        )


# Practice games
# --------------------------------------------------------------------------------
class Practice1Page1(FirstPage):
    pass


class Practice1Page2(FirstPage):
    pass


class Practice1Page3(FirstPage):
    pass


class Practice1Page4(FirstPage):
    pass


class Practice2Page1(FirstPage):
    pass


class Practice2Page2(FirstPage):
    pass


class Practice2Page3(FirstPage):
    pass


# Pages to be displayed at each round
# --------------------------------------------------------------------------------
class Decision(Page):

    form_model = 'player'
    form_fields = ['take']

    def is_displayed(self):
        if not self.group.game_on:
            return False
        elif self.player.id_in_group == 1 and self.participant.vars['game_node'] % 2 != 0:
            return True
        elif self.player.id_in_group == 2 and self.participant.vars['game_node'] % 2 == 0:
            return True
        else:
            return False

    def vars_for_template(self):
        return dict(
            large_pile=self.session.vars['large_piles'][self.participant.vars['game_node'] - 1],
            small_pile=self.session.vars['small_piles'][self.participant.vars['game_node'] - 1]
        )

    def before_next_page(self):
        return self.group.stop_game(), self.group.set_payoffs(), self.group.set_game_node(), self.group.set_game()


# Wait pages
# --------------------------------------------------------------------------------
class RegroupPage(WaitPage):

    wait_for_all_groups = True

    # after_all_players_arrive = 'shuffle_players'

    def is_displayed(self):
        return not self.group.game_on


class Wait(WaitPage):
    def after_all_players_arrive(self):
        pass


# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         pass


# Results pages
# --------------------------------------------------------------------------------
class ResultsInterim(Page):
    def is_displayed(self):
        return not self.group.game_on

    def vars_for_template(self):
        return dict(
            large_pile=self.session.vars['large_piles'][self.participant.vars['game_node'] - 1],
            small_pile=self.session.vars['small_piles'][self.participant.vars['game_node'] - 1],
            large_pile_pass=self.session.vars['large_piles'][-1],
            small_pile_pass=self.session.vars['small_piles'][-1]
        )

    def before_next_page(self):
        return self.group.repeat_game()


class Results(Page):
    def is_displayed(self):
        return not self.group.game_on and self.participant.vars['game'] == Constants.num_games

    def vars_for_template(self):
        return dict(
            large_pile=self.session.vars['large_piles'][self.participant.vars['game_node'] - 1],
            small_pile=self.session.vars['small_piles'][self.participant.vars['game_node'] - 1],
            large_pile_pass=self.session.vars['large_piles'][-1],
            small_pile_pass=self.session.vars['small_piles'][-1]
        )


page_sequence = [#Welcome, Instructions,
                 #RegroupPage,
                 #Practice1Page1, Practice1Page2, Practice1Page3, Practice1Page4, RegroupPage,
                 #Practice2Page1, Practice2Page2, Practice2Page3, RegroupPage,
                 Decision, Wait, ResultsInterim, #RegroupPage
                ]
