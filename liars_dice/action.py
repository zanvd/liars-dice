from dataclasses import dataclass


class CancelBidException(Exception):
    pass


@dataclass(frozen=True)
class Bid:
    value: int
    number: int

    def __str__(self) -> str:
        return f"{self.number} of {self.value}"

    def is_zero(self) -> bool:
        return self.value == 0


@dataclass(frozen=True)
class Challenge:
    pass


Action = Bid | Challenge
