from dataclasses import dataclass

from liars_dice.action import Action, Bid, CancelBidException, Challenge


@dataclass
class Player:
    id: int
    name: str
    num_of_dice: int = 2

    @staticmethod
    def bid(last_bid: Bid, max_dice_num: int) -> Bid:
        value: int = 0
        number: int = 0

        valid_val: bool = False
        valid_num: bool = False
        while not (valid_val and valid_num):
            try:
                value = int(input("Specify a die value: "))
                valid_val = True
                if value not in [1, 2, 3, 4, 5, 6]:
                    print(f"Invalid die value ({value}).")
                    valid_val = False
                elif value < last_bid.value:
                    print(f"Value has to be greater than or equal to {last_bid.value}.")
                    valid_val = False
            except ValueError:
                print(f"Invalid die value ({value}).")
                valid_val = False
            if not valid_val:
                continue

            try:
                number = int(input("Specify a number of dice: "))
                valid_num = True
                if number > max_dice_num:
                    print(f"There's only {max_dice_num} dice in play.")
                    valid_num = False
                elif value == last_bid.value and number <= last_bid.number:
                    print(f"Number has to be greater than {last_bid.number}.")
                    valid_num = False
            except ValueError:
                print(f"Invalid number ({number}).")
                valid_num = False
            if not valid_num and not last_bid.is_zero():
                # There's a chance someone's not paying attention and lands in a bid where there's no way to pass
                # validation (e.g. value is 6 and highest number of dice). This is a fallback for such a case.
                if input("Would you like to challenge, instead? (y/N) ") == "y":
                    raise CancelBidException()

        return Bid(value=value, number=number)

    @property
    def is_zero(self) -> bool:
        return False

    def lose_die(self) -> None:
        self.num_of_dice -= 1

    def play_turn(self, last_bid: Bid, max_dice_num: int) -> Action:
        if not last_bid.is_zero():
            try:
                action: int = int(input("Please choose an action (1 for bid, 2 for challenge): "))
            except ValueError:
                print("Invalid action. Please try again.")
                return self.play_turn(last_bid, max_dice_num)
        else:
            action: int = 1

        match action:
            case 1:
                try:
                    return self.bid(last_bid, max_dice_num)
                except CancelBidException:
                    return Challenge()
            case 2:
                return Challenge()
            case _:
                print("Invalid action. Please try again.")
                return self.play_turn(last_bid, max_dice_num)


@dataclass
class ZeroPlayer(Player):
    id: int = -1
    name: str = ""
    num_of_dice: int = 0

    @property
    def is_zero(self) -> bool:
        return True


class Players(dict[int, Player]):
    def get_next(self, curr_id: int) -> Player:
        keys: list[int] = list(self.keys())
        next_ix: int = keys.index(curr_id) + 1
        if next_ix >= len(keys):
            next_ix = 0
        return self.get(keys[next_ix])
