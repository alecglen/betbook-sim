import pandas as pd
from dataclasses import fields
from models import *


def init_game(
    player_count: int = 12,
    offering_count: int = 100,
    startBalance: int = 1000,
    minBalance: int = 0,
    burn: int = 0
):
    players = [Player(startBalance) for _ in range(player_count)]
    offerings = [Offering() for _ in range(offering_count)]
    return Game(players, offerings, minBalance, burn)


def sim(game: Game):
    for bet in game.offerings:
        for player in game.players:
            if player.takes(bet):
                player.bets_made += 1
                wager = player.balance * player.risk_preference
                if bet.outcome:
                    winnings = wager * bet.payout_multiplier
                    player.revenue += winnings
                    player.balance += winnings
                else:
                    player.balance -= wager
            else:
                player.balance -= game.burn
            player.balance = max(player.balance, game.minBalance)
    return game
                
                
def summarize(game: Game, iteration: int):
    ps = game.players
    return pd.DataFrame({
        "game": [iteration]*len(ps),
        "player": range(len(ps)),
        **{
            f.name: [round(getattr(p, f.name), 2) for p in ps]
            for f in fields(ps[0])
        }
    })