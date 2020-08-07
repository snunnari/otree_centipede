from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FirstPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class Welcome(FirstPage):
    pass


class Instructions(FirstPage):

    def vars_for_template(self):
        return dict(
            turns=int(Constants.num_rounds / 2),
            instructionsMatrix=Constants.instructionsMatrix,
            rounds_range=Constants.rounds_range,
            large_pile_practice=Constants.large_piles,
            small_pile_practice=Constants.small_piles,
            large_pile_practice_second=Constants.large_piles[1],
            small_pile_practice_second=Constants.small_piles[1],
            large_pile_practice_third=Constants.large_piles[2],
            small_pile_practice_third=Constants.small_piles[2],
            large_pile_practice_last=Constants.large_piles[-2],
            small_pile_practice_last=Constants.small_piles[-2],
            large_pile_practice_pass=Constants.large_piles[-1],
            small_pile_practice_pass=Constants.small_piles[-1]
        )


class Practice1Page1(FirstPage):
    pass


class Practice1Page2(FirstPage):
    def vars_for_template(self):
        return dict(
            large_pile_practice=Constants.large_piles,
            small_pile_practice=Constants.small_piles,
            large_pile_practice_second=Constants.large_piles[1],
            small_pile_practice_second=Constants.small_piles[1],
        )


class Practice1Page3(FirstPage):

    def vars_for_template(self):
        return dict(
            large_pile_practice=Constants.large_piles,
            small_pile_practice=Constants.small_piles,
            large_pile_practice_second=Constants.large_piles[1],
            small_pile_practice_second=Constants.small_piles[1],
        )


class Practice1Page4(FirstPage):

    def vars_for_template(self):
        return dict(
            large_pile_practice=Constants.large_piles,
            small_pile_practice=Constants.small_piles,
            large_pile_practice_second=Constants.large_piles[1],
            small_pile_practice_second=Constants.small_piles[1],
        )


class Practice2Page1(FirstPage):

    def vars_for_template(self):
        return dict(
            large_pile_practice_second=Constants.large_piles[1],
            small_pile_practice_second=Constants.small_piles[1],
            large_pile_practice_third=Constants.large_piles[2],
            small_pile_practice_third=Constants.small_piles[2]
        )


class Practice2Page2(FirstPage):

    def vars_for_template(self):
        return dict(
            large_pile_practice_last=Constants.large_piles[-2],
            small_pile_practice_last=Constants.small_piles[-2],
            large_pile_practice_pass=Constants.large_piles[-1],
            small_pile_practice_pass=Constants.small_piles[-1],
        )


class Practice2Page3(FirstPage):
    pass


class WaitPage1(WaitPage):

    def is_displayed(self):
        return self.round_number == 1

    wait_for_all_groups = True


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

class WaitPage2(WaitPage):
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


class WaitPage3(WaitPage):
    def is_displayed(self):
        if self.round_number in Constants.last_rounds:
            return True
        else:
            return False
    wait_for_all_groups = True
    after_all_players_arrive = 'advance_game'


page_sequence = [
    Welcome,
    Instructions,
    #Practice1Page1,
    #Practice1Page2,
    #Practice1Page3,
    #Practice1Page4,
    #Practice2Page1,
    #Practice2Page2,
    WaitPage1,
    Decision,
    WaitPage2,
    Results,
    WaitPage3
                ]
