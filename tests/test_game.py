import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from liars_dice.action import Bid, Challenge
from liars_dice.game import Die, Game, Result, Round, Throw
from liars_dice.player import Player, Players


class CheckChallengeTestCase(TestCase):
    player: Player
    throws: list[Throw]

    def setUp(self) -> None:
        self.player: Player = Player(1, "p1")
        self.throws: list[Throw] = [
            Throw(dice=[Die(1), Die(2)], player=self.player),
            Throw(dice=[Die(5), Die(4)], player=self.player),
            Throw(dice=[Die(4), Die(4)], player=self.player),
        ]

    @patch('builtins.print')
    def test_challenge_lost(self, _) -> None:
        last_bid: Bid = Bid(value=4, number=3)
        r = Round._check_challenge(last_bid=last_bid, throws=self.throws, are_ones_wild=False)
        self.assertFalse(r)

        last_bid: Bid = Bid(value=2, number=2)
        r = Round._check_challenge(last_bid=last_bid, throws=self.throws, are_ones_wild=True)
        self.assertFalse(r)

    @patch('builtins.print')
    def test_challenge_won(self, _) -> None:
        last_bid: Bid = Bid(value=4, number=4)
        r = Round._check_challenge(last_bid=last_bid, throws=self.throws, are_ones_wild=False)
        self.assertTrue(r)

        last_bid: Bid = Bid(value=2, number=3)
        r = Round._check_challenge(last_bid=last_bid, throws=self.throws, are_ones_wild=True)
        self.assertTrue(r)


class DiceThrowTestCase(TestCase):
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_throws_num_eq_players_num(self, *_) -> None:
        players: Players = Players({i: Player(i, f"p{i}") for i in range(1, 4)})
        throws, _ = Round._throw_dice(players)

        self.assertEqual(len(players), len(throws))

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_correct_num_of_dice_default(self, *_) -> None:
        players: Players = Players()
        for i in range(1, 5):
            players[i] = Player(i, f"p{i}")
        throws, max_dice_num = Round._throw_dice(players)

        self.assertEqual(8, max_dice_num)
        self.assertEqual(8, sum([len(t.dice) for t in throws]))

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('os.system')
    def test_correct_num_of_dice_non_default(self, *_) -> None:
        players: Players = Players()
        for i in range(1, 5):
            players[i] = Player(i, f"p{i}", num_of_dice=i)
        throws, max_dice_num = Round._throw_dice(players)

        self.assertEqual(10, max_dice_num)
        self.assertEqual(10, sum([len(t.dice) for t in throws]))


class GameTestCase(TestCase):
    @patch('builtins.input')
    @patch('builtins.print')
    @patch.object(Round, 'start')
    def test_game_play(self, m_round_start, *_) -> None:
        def lose_die(p):
            p.num_of_dice -= 1

        m_p1 = MagicMock(id=1, name="p1", num_of_dice=2)
        m_p1.lose_die = lambda: lose_die(m_p1)
        m_p2 = MagicMock(id=2, name="p2", num_of_dice=2)
        m_p2.lose_die = lambda: lose_die(m_p2)
        m_p3 = MagicMock(id=3, name="p3", num_of_dice=1)
        m_p3.lose_die = lambda: lose_die(m_p3)

        mock_players = MagicMock()
        mock_players.__getitem__.side_effect = lambda i: [m_p1, m_p2, m_p3][i - 1]
        mock_players.get_next.side_effect = lambda i: m_p2 if i == 2 else m_p3 if i == 3 else m_p1
        mock_players.__len__.side_effect = [3, 3, 2, 1]

        m_round_start.side_effect = [Result(m_p3), Result(m_p1), Result(m_p1), Result(m_p2), Result(m_p1)]

        Game.play(False, 1, mock_players)

        self.assertEqual(0, m_p1.num_of_dice)
        self.assertEqual(1, m_p2.num_of_dice)
        self.assertEqual(0, m_p3.num_of_dice)


class RoundStartTestCase(TestCase):
    m_p1: MagicMock
    m_p2: MagicMock
    m_players: MagicMock

    def setUp(self) -> None:
        self.m_p1 = MagicMock(id=1, name="p1")
        self.m_p1.play_turn.side_effect = [Bid(value=2, number=1)]
        self.m_p2 = MagicMock(id=2, name="p2")
        self.m_p2.play_turn.side_effect = [Challenge()]

        self.m_players = MagicMock()
        self.m_players.__getitem__.side_effect = lambda i: self.m_p1 if i == 1 else self.m_p2
        self.m_players.get_next.side_effect = lambda i: self.m_p2 if i == 1 else self.m_p1

    @patch('builtins.print')
    @patch('os.system')
    @patch.object(Round, '_check_challenge', return_value=True)
    @patch.object(Round, '_throw_dice', return_value=([], 4))
    def test_challenger_lost(self, *_) -> None:
        res = Round.start(1, self.m_players, 1, False)

        self.assertEqual(self.m_p1, res.loser)

    @patch('builtins.print')
    @patch('os.system')
    @patch.object(Round, '_check_challenge', return_value=False)
    @patch.object(Round, '_throw_dice', return_value=([], 4))
    def test_challenger_won(self, *_) -> None:
        res = Round.start(1, self.m_players, 1, False)

        self.assertEqual(self.m_p2, res.loser)


if __name__ == '__main__':
    unittest.main()
