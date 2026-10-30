"""Terminal rendering with ANSI colors and a plain-text fallback."""

import os
import sys

from .game import MAX_GUESSES, WORD_LENGTH, Game, Mark

KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")

RESET = "\033[0m"
STYLES = {
    Mark.CORRECT: "\033[1;97;42m",  # bold white on green
    Mark.PRESENT: "\033[1;30;43m",  # bold black on yellow
    Mark.ABSENT: "\033[1;97;100m",  # bold white on gray
}
UNUSED = "\033[1;30;47m"            # bold black on light gray
PLAIN = {Mark.CORRECT: "[{}]", Mark.PRESENT: "({})", Mark.ABSENT: " {} "}


def color_supported() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


class Renderer:
    def __init__(self, color: bool):
        self.color = color

    def tile(self, letter: str, mark: Mark | None) -> str:
        letter = letter.upper()
        if self.color:
            return f"{UNUSED if mark is None else STYLES[mark]} {letter} {RESET}"
        if mark is None:
            return f" {letter} "
        return PLAIN[mark].format(letter)

    def clear(self) -> None:
        if self.color:
            print("\033[2J\033[H", end="")

    def board(self, game: Game) -> str:
        lines = []
        for guess, marks in game.guesses:
            lines.append(" ".join(self.tile(l, m) for l, m in zip(guess, marks)))
        empty = " ".join(self.tile("_", None) for _ in range(WORD_LENGTH))
        lines += [empty] * (MAX_GUESSES - len(game.guesses))
        return "\n".join("  " + line for line in lines)

    def keyboard(self, game: Game) -> str:
        lines = []
        for indent, row in enumerate(KEYBOARD_ROWS):
            marks = [game.letters.get(k) for k in row]
            if not self.color:
                # Plain absent tiles look like unused keys, so blank them out.
                row = ["-" if m is Mark.ABSENT else k for k, m in zip(row, marks)]
            keys = "".join(self.tile(k, m) for k, m in zip(row, marks))
            lines.append(" " * (indent * 2) + keys)
        return "\n".join(lines)

    def draw(self, game: Game, message: str = "") -> None:
        self.clear()
        print("\n  W O R D L E\n")
        print(self.board(game))
        print()
        print(self.keyboard(game))
        if not self.color:
            print("\n  [X] right spot   (X) wrong spot   X not in word")
        print(f"\n  {message}" if message else "")
