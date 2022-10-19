from dataclasses import dataclass, field, astuple
from numpy import clip
from numpy.random import normal
from random import random


def normfield(mean: float, std: float, _min: float = 0, _max: float = 1 ):
    return field(default_factory = lambda: clip(normal(mean, std), _min, _max))


@dataclass
class Offering:
    odds: float = normfield(.5, .2, .05, .95)
    payout_multiplier: float = field(init=False)
    outcome: bool = field(init=False)
    
    def __post_init__(self):
        self.payout_multiplier = (1-self.odds) / (self.odds + .05)
        self.outcome = self.odds > random()

   
@dataclass
class Player:
    balance: float
    skill: float = normfield(0, .1, -1, 1)
    bet_preference: float = normfield(.5, .25)
    risk_preference: float = normfield(.1, .2, .01)
    activeness: float = normfield(.4, .3)
    bets_made: int = field(default=0, init=False)
    
    def takes(self, bet: Offering):
        return (
            self.balance > 0 and
            self.activeness > random() and
            abs(self.bet_preference - bet.odds) < normal(.6, .2) and
            (
                bet.outcome if self.skill > random()
                else not bet.outcome if self.skill < -random()
                else True
            )
        )


@dataclass
class Game:
    players: list[Player]
    offerings: list[Offering]
    minBalance: int
    burn: int
