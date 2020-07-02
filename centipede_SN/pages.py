from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

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
            groupid = self.group.id_in_subsession,
            game = self.participant.vars['game'],
            game_node = self.participant.vars['game_node'],
            large_pile = self.session.vars['large_piles'][self.participant.vars['game_node'] - 1],
            small_pile = self.session.vars['small_piles'][self.participant.vars['game_node'] - 1]
        )

    def before_next_page(self):
        return self.group.stop_game_or_advance_node(), self.group.set_payoffs()

class WaitPage1(WaitPage):
    def after_all_players_arrive(self):
        pass

class Results(Page):
    def is_displayed(self):
        return not self.group.game_on

    def vars_for_template(self):
        return dict(
            game=self.participant.vars['game'],
            game_node = self.participant.vars['game_node'],
            large_pile=self.session.vars['large_piles'][self.participant.vars['game_node']-1],
            small_pile=self.session.vars['small_piles'][self.participant.vars['game_node']-1],
            large_pile_pass=self.session.vars['large_piles'][-1],
            small_pile_pass=self.session.vars['small_piles'][-1]
        )

class WaitPage2(WaitPage):
    def is_displayed(self):
        return not self.group.game_on
    wait_for_all_groups = True
    after_all_players_arrive = 'advance_game'

page_sequence = [
    Decision,
    WaitPage1,
    Results,
    WaitPage2
                ]
