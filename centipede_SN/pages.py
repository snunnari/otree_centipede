from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Decision(Page):

    form_model = 'player'
    form_fields = ['take']

    def is_displayed(self):
        if self.player.id_in_group == 1 and self.round_number % 2 != 0 and self.group.game_on:
            return True
        elif self.player.id_in_group == 2 and self.round_number % 2 == 0 and self.group.game_on:
            return True
        else:
            return False

    def vars_for_template(self):
        return dict(
            game = self.subsession.game,
            game_node = self.subsession.game_node,
            large_pile = Constants.large_piles[self.subsession.game_node - 1],
            small_pile = Constants.small_piles[self.subsession.game_node - 1]
        )

    def before_next_page(self):
        return self.group.stop_game(), self.group.set_payoffs()

class WaitPage1(WaitPage):
    def after_all_players_arrive(self):
        pass

class Results(Page):
    def is_displayed(self):
        if self.round_number in Constants.last_rounds:
            return True
        else:
            return False

    def vars_for_template(self):
        return dict(
            game=self.subsession.game,
            last_node=self.group.last_node,
            large_pile=Constants.large_piles[self.group.last_node-1],
            small_pile=Constants.small_piles[self.group.last_node-1],
            large_pile_pass=Constants.large_piles[-1],
            small_pile_pass=Constants.small_piles[-1]
        )

class WaitPage2(WaitPage):
    def is_displayed(self):
        if self.round_number in Constants.last_rounds:
            return True
        else:
            return False
    wait_for_all_groups = True
    after_all_players_arrive = 'advance_game'

page_sequence = [
    Decision,
    WaitPage1,
    Results,
    WaitPage2
                ]
