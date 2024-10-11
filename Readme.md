# Liar's Dice

## Overview

This is a command-line interface (CLI) implementation of the popular dice game [Liar's Dice][1] written in Python.
Players take turns bidding on the number of dice with a specific face value, or challenging the previous bid.
The game continues until only one player remains.

## How to Play

1. Each player starts with a set number of dice (2).
2. On each player's turn, one can:
    * **Make a Bid:** Bid a higher number or value of dice than the last bid.
    * **Challenge:** If a player believes the last bid is incorrect, he can challenge.
      All the dice are revealed and the challenger wins if there are fewer dice than bid and looses otherwise.
      Looser of a challenge discards one die.
3. If a player looses all of his dice, he is out of the game.
4. The game ends when only one player has any die remaining.

## Game options

* **Wild ones:** if turned on, dice with the value of 1 count as wild (any value).

## Installation

1. Clone the repository:
    ```shell
    git clone https://bitbucket.org:zanvd/liars-dice.git
    ```
2. Navigate to the project's root:
    ```shell
    cd liars-dice
    ```
3. Run the game:
    ```shell
    python -m liars_dice.main
    ```

## Controls

* **Bid:** Enter a die face (1-6) and the quantity of dice you believe are present in the game.
* **Challenge:** Challenge previous player's bid.

## Requirements

* Python 3.x

## Testing

Execute:

```shell
python -m unittest discover -s tests/
```

## License

This project is licensed under the [MIT License](./License.md).

[1]: https://en.wikipedia.org/wiki/Liar's_dice
