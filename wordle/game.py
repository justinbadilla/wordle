"""Core Wordle rules and game state. No I/O lives here."""

from collections import Counter
from enum import IntEnum

WORD_LENGTH = 5
MAX_GUESSES = 6


class Mark(IntEnum):
    # Ordered so max() gives the best-known state of a letter.
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2


class InvalidGuess(ValueError):
    pass


def score_guess(guess: str, answer: str) -> list[Mark]:
    """Score a guess against the answer, handling repeated letters correctly."""
    marks = [Mark.ABSENT] * len(guess)
    unmatched = Counter()

    # Pass 1: exact matches; remember the answer letters left over.
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            marks[i] = Mark.CORRECT
        else:
            unmatched[a] += 1

    # Pass 2: misplaced letters, each consuming one leftover answer letter.
    for i, g in enumerate(guess):
        if marks[i] is not Mark.CORRECT and unmatched[g] > 0:
            marks[i] = Mark.PRESENT
            unmatched[g] -= 1

    return marks


class Game:
    def __init__(self, answer: str, allowed: set[str]):
        self.answer = answer.lower()
        self.allowed = allowed
        self.guesses: list[tuple[str, list[Mark]]] = []
        self.letters: dict[str, Mark] = {}

    @property
    def won(self) -> bool:
        return bool(self.guesses) and self.guesses[-1][0] == self.answer

    @property
    def lost(self) -> bool:
        return not self.won and len(self.guesses) >= MAX_GUESSES

    @property
    def over(self) -> bool:
        return self.won or self.lost

    def submit(self, guess: str) -> list[Mark]:
        if self.over:
            raise InvalidGuess("Game is over")
        guess = guess.strip().lower()
        if len(guess) != WORD_LENGTH or not guess.isalpha():
            raise InvalidGuess(f"Must be {WORD_LENGTH} letters")
        if guess not in self.allowed:
            raise InvalidGuess("Not in word list")

        marks = score_guess(guess, self.answer)
        self.guesses.append((guess, marks))
        for letter, mark in zip(guess, marks):
            self.letters[letter] = max(mark, self.letters.get(letter, Mark.ABSENT))
        return marks
