import datetime
import unittest

from wordle import words
from wordle.game import MAX_GUESSES, Game, InvalidGuess, Mark, score_guess

C, P, A = Mark.CORRECT, Mark.PRESENT, Mark.ABSENT


class ScoreGuessTest(unittest.TestCase):
    def test_all_correct(self):
        self.assertEqual(score_guess("crane", "crane"), [C] * 5)

    def test_all_absent(self):
        self.assertEqual(score_guess("fghij", "crane"), [A] * 5)

    def test_present(self):
        self.assertEqual(score_guess("nacre", "crane"), [P, P, P, P, C])

    def test_duplicate_guess_letter_single_in_answer(self):
        # Only one E in ABIDE: the first E is present, the second is not.
        self.assertEqual(score_guess("speed", "abide"), [A, A, P, A, P])

    def test_duplicate_guess_letter_correct_takes_priority(self):
        # The exact-match E consumes ABIDE's only E, so the earlier Es are absent.
        self.assertEqual(score_guess("eerie", "abide"), [A, A, A, P, C])

    def test_duplicate_in_both(self):
        self.assertEqual(score_guess("label", "belle"), [P, A, P, P, P])

    def test_more_copies_in_answer(self):
        self.assertEqual(score_guess("lobby", "bobby"), [A, C, C, C, C])


class GameTest(unittest.TestCase):
    def setUp(self):
        self.allowed = {"crane", "slate", "trace", "eerie", "abide"}
        self.game = Game("crane", self.allowed)

    def test_rejects_wrong_length(self):
        with self.assertRaisesRegex(InvalidGuess, "5 letters"):
            self.game.submit("cran")

    def test_rejects_non_letters(self):
        with self.assertRaisesRegex(InvalidGuess, "5 letters"):
            self.game.submit("cr4ne")

    def test_rejects_unknown_word(self):
        with self.assertRaisesRegex(InvalidGuess, "word list"):
            self.game.submit("zzzzz")
        self.assertEqual(self.game.guesses, [])

    def test_normalizes_input(self):
        self.game.submit("  CRANE ")
        self.assertTrue(self.game.won)

    def test_loses_after_max_guesses(self):
        for _ in range(MAX_GUESSES):
            self.game.submit("slate")
        self.assertTrue(self.game.lost)
        with self.assertRaises(InvalidGuess):
            self.game.submit("crane")

    def test_letter_state_keeps_best_mark(self):
        self.game.submit("trace")  # c is present here
        self.assertEqual(self.game.letters["c"], P)
        self.game.submit("crane")  # c is correct here
        self.assertEqual(self.game.letters["c"], C)
        self.assertEqual(self.game.letters["t"], A)


class WordsTest(unittest.TestCase):
    def test_lists_load(self):
        answers = words.load_answers()
        allowed = words.load_allowed(answers)
        self.assertGreater(len(answers), 100)
        self.assertTrue(set(answers) <= allowed)
        self.assertTrue(all(len(w) == 5 for w in allowed))

    def test_daily_is_stable(self):
        answers = words.load_answers()
        day = datetime.date(2026, 10, 30)
        self.assertEqual(words.pick_daily(answers, day), words.pick_daily(answers, day))

    def test_seed_is_repeatable(self):
        answers = words.load_answers()
        self.assertEqual(words.pick_random(answers, 7), words.pick_random(answers, 7))


if __name__ == "__main__":
    unittest.main()
