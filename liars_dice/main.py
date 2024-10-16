from liars_dice.game import Game
from liars_dice.player import LivePlayer, Players


def main() -> None:
    player_num: int = 0
    while player_num < 2:
        try:
            player_num = int(input("Number of players: "))
            if player_num < 2:
                print("Insufficient number of players (at least 2).")
        except ValueError:
            print("Insufficient number of players (at least 2).")

    first_p_id: int = 1
    players: Players = Players()
    for i in range(first_p_id, player_num + 1):
        name: str = ""
        while len(name) == 0:
            name = str(input(f"Name for player #{i}: "))
            if len(name) == 0:
                print("Please enter a name.")
        players[i] = LivePlayer(id=i, name=name)

    are_ones_wild: bool = input("Count ones as wild? (y/N) ") == "y"

    Game.play(are_ones_wild, first_p_id, players)
    if len(players) > 1:
        raise ValueError("Too many players remaining.")
    winner = next(iter(players.values()))

    print("Game finished.")
    print(f"The winner of the game is player {winner.name}!")


if __name__ == '__main__':
    main()
