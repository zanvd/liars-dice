import os
import random
from dataclasses import dataclass

from liars_dice.action import Action, Bid, Challenge
from liars_dice.player import Player, Players


@dataclass(frozen=True)
class Die:
    value: int

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Result:
    loser: Player


@dataclass(frozen=True)
class Throw:
    dice: list[Die]
    player: Player

    def print_dice(self) -> str:
        return ", ".join([str(d.value) for d in self.dice])


class Round:
    @staticmethod
    def start(number: int, players: Players, starting_id: int, are_ones_wild) -> Result:
        os.system("clear")
        print(f"Starting round #{number}")

        throws, max_dice_num = Round._throw_dice(players)

        last_bid = Bid(value=0, number=0)

        prev_id: int = -1
        curr_id: int = starting_id
        while True:
            print(f"Player {players[curr_id].name}'s turn.")

            action: Action = players[curr_id].play_turn(last_bid, max_dice_num)
            if isinstance(action, Challenge):
                if Round._check_challenge(last_bid, throws, are_ones_wild):
                    print("Challenge won!")
                    return Result(loser=players[prev_id])
                else:
                    print("Challenge lost!")
                    return Result(loser=players[curr_id])

            os.system("clear")

            prev_id = curr_id
            curr_id = players.get_next(curr_id).id

            last_bid = action
            print(f"Last bid is {last_bid.number} of {last_bid.value} by {players[prev_id].name}.")

    @staticmethod
    def _check_challenge(last_bid: Bid, throws: list[Throw], are_ones_wild: bool) -> bool:
        print(f"Challenging last bid: {last_bid}")
        counter: int = 0
        for t in throws:
            print(f"Player {t.player.name}'s throw: {t.print_dice()}.")
            for d in t.dice:
                if d.value == last_bid.value or (are_ones_wild and d.value == 1):
                    counter += 1
        return counter < last_bid.number

    @staticmethod
    def _throw_dice(players: Players) -> (list[Throw], int):
        max_dice_num: int = 0
        throws: list[Throw] = []
        for p_id, p in players.items():
            input(f"Press return to throw for player {p.name}.")

            dice: list[Die] = [Die(random.randint(1, 6)) for _ in range(p.num_of_dice)]
            t: Throw = Throw(dice=dice, player=p)
            throws.append(t)

            max_dice_num += p.num_of_dice

            print(f"Your throw is: {t.print_dice()}")

            if len(players) == len(throws):
                input("Press return to continue.")
            else:
                input("Press return for the next player.")
            os.system("clear")

        return throws, max_dice_num


class Game:
    @staticmethod
    def play(are_ones_wild, first_p_id: int, players: Players) -> None:
        round_num: int = 1
        while True:
            res: Result = Round.start(round_num, players, first_p_id, are_ones_wild)

            p: Player = players[res.loser.id]
            p.lose_die()

            print(f"Player {p.name} lost a die.")

            first_p_id = p.id
            if p.num_of_dice == 0:
                first_p_id = players.get_next(p.id).id
                del players[p.id]
                print(f"Player {p.name} is eliminated from the game.")

            if len(players) == 1:
                break

            print(f"Round #{round_num} done.")
            input("Press return to continue.")

            round_num += 1
