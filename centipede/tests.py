from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

import numpy as np


class PlayerBot(Bot):
    def play_round(self):

        if self.group.game_on:
            coinflip = np.random.binomial(1, 0.9)
            if coinflip == 1:
                yield pages.Decision, dict(take=True)
            else:
                yield pages.Decision, dict(take=False)

