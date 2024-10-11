import unittest
from unittest import TestCase

from liars_dice.action import Bid


class BidTestCase(TestCase):
    def test_is_zero(self) -> None:
        self.assertTrue(Bid(value=0, number=1).is_zero())
        self.assertFalse(Bid(value=1, number=2).is_zero())


if __name__ == '__main__':
    unittest.main()
