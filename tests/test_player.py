import unittest
from unittest import TestCase
from unittest.mock import patch

from liars_dice.action import Bid, CancelBidException, Challenge
from liars_dice.player import LivePlayer, Players, ZeroPlayer


class PlayerTestCase(TestCase):
    # Valid same value and valid different value.
    @patch('builtins.input', side_effect=["2", "3", "5", "1"])
    @patch('builtins.print')
    def test_bid_valid(self, *_) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=2, number=2)

        bid = player._bid(last_bid, 10)

        self.assertEqual(bid.value, 2)
        self.assertEqual(bid.number, 3)

        bid = player._bid(last_bid, 10)

        self.assertEqual(bid.value, 5)
        self.assertEqual(bid.number, 1)

    # Invalid lower value, invalid out-of-bounds value, valid value.
    @patch('builtins.input', side_effect=["3", "7", "6", "2"])
    @patch('builtins.print')
    def test_bid_invalid_value_retry(self, *_) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=4, number=3)

        bid = player._bid(last_bid, 10)

        self.assertEqual(bid.value, 6)
        self.assertEqual(bid.number, 2)

    # Invalid lower number, invalid out-of-bounds number, valid number.
    @patch('builtins.input', side_effect=["3", "1", "n", "3", "11", "n", "3", "3"])
    @patch('builtins.print')
    def test_bid_invalid_number_retry(self, *_) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=3, number=2)

        bid = player._bid(last_bid, 10)

        self.assertEqual(bid.value, 3)
        self.assertEqual(bid.number, 3)

    @patch('builtins.input', side_effect=["6", "4", "y"])
    @patch('builtins.print')
    def test_bid_cancel_bid_exception(self, *_) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=6, number=5)

        with self.assertRaises(CancelBidException):
            player._bid(last_bid, 10)

    def test_is_zero(self) -> None:
        self.assertFalse(LivePlayer(1, "p1").is_zero)

    def test_lose_die(self) -> None:
        p = LivePlayer(1, "p1", 2)

        p.lose_die()
        self.assertEqual(1, p.num_of_dice)

        p.lose_die()
        self.assertEqual(0, p.num_of_dice)

    @patch('builtins.input', return_value="1")
    def test_play_turn_valid_bid(self, _) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=2, number=1)

        with patch.object(player, '_bid', return_value=Bid(value=3, number=3)):
            action = player.play_turn(last_bid, max_dice_num=10)

            self.assertIsInstance(action, Bid)
            self.assertEqual(action.number, 3)
            self.assertEqual(action.value, 3)

    @patch('builtins.input', return_value="2")
    def test_play_turn_choose_challenge(self, _) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=3, number=2)

        action = player.play_turn(last_bid, max_dice_num=10)

        self.assertIsInstance(action, Challenge)

    @patch('builtins.input', side_effect=["6", "7", "1"])
    @patch('builtins.print')
    def test_play_turn_invalid_action(self, *_) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=5, number=3)

        with patch.object(player, '_bid', return_value=Bid(value=6, number=4)):
            action = player.play_turn(last_bid, max_dice_num=10)

            self.assertIsInstance(action, Bid)
            self.assertEqual(action.number, 4)
            self.assertEqual(action.value, 6)

    @patch('builtins.input', return_value="1")
    def test_play_turn_cancel_bid_then_challenge(self, _) -> None:
        player = LivePlayer(id=1, name="p1")
        last_bid = Bid(value=6, number=5)

        with patch.object(player, '_bid', side_effect=CancelBidException):
            action = player.play_turn(last_bid, max_dice_num=10)

            self.assertIsInstance(action, Challenge)


class PlayersTestCase(TestCase):
    p1: LivePlayer
    p2: LivePlayer
    p3: LivePlayer
    p4: LivePlayer
    players: Players

    def setUp(self):
        self.p1 = LivePlayer(id=1, name="p1")
        self.p2 = LivePlayer(id=2, name="p2")
        self.p3 = LivePlayer(id=3, name="p3")
        self.p4 = LivePlayer(id=5, name="p4")

        self.players = Players()
        self.players[self.p1.id] = self.p1
        self.players[self.p2.id] = self.p2
        self.players[self.p3.id] = self.p3
        self.players[self.p4.id] = self.p4

    def test_get_next_middle_player(self) -> None:
        next_player = self.players.get_next(curr_id=1)

        self.assertEqual(next_player, self.p2)

    def test_get_next_last_player(self) -> None:
        next_player = self.players.get_next(curr_id=3)

        self.assertEqual(next_player, self.p4)

    def test_get_next_wrap_player(self) -> None:
        next_player = self.players.get_next(curr_id=5)

        self.assertEqual(next_player, self.p1)

    def test_get_next_single_player(self) -> None:
        single_player = Players()
        single_player[self.p1.id] = self.p1
        next_player = single_player.get_next(curr_id=1)

        self.assertEqual(next_player, self.p1)


class ZeroPlayerTestCase(TestCase):
    def test_is_zero(self) -> None:
        self.assertTrue(ZeroPlayer().is_zero)


if __name__ == '__main__':
    unittest.main()
