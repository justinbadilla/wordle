"""Entry point: python -m wordle"""

import argparse

from . import words
from .game import MAX_GUESSES, Game, InvalidGuess
from .ui import Renderer, color_supported


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="wordle", description="Play Wordle in the terminal.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--daily", action="store_true", help="play today's word")
    mode.add_argument("--seed", type=int, help="seed for a repeatable random word")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    return parser.parse_args()


def play(game: Game, ui: Renderer) -> None:
    message = f"Guess the word in {MAX_GUESSES} tries."
    while not game.over:
        ui.draw(game, message)
        try:
            game.submit(input(f"  Guess {len(game.guesses) + 1}/{MAX_GUESSES}: "))
            message = ""
        except InvalidGuess as e:
            message = str(e)

    if game.won:
        n = len(game.guesses)
        ui.draw(game, f"Solved in {n} {'guess' if n == 1 else 'guesses'}!")
    else:
        ui.draw(game, f"Out of guesses. The word was {game.answer.upper()}.")


def main() -> None:
    args = parse_args()
    answers = words.load_answers()
    allowed = words.load_allowed(answers)
    ui = Renderer(color=color_supported() and not args.no_color)

    try:
        if args.daily:
            play(Game(words.pick_daily(answers), allowed), ui)
            return
        seed = args.seed
        while True:
            play(Game(words.pick_random(answers, seed), allowed), ui)
            if input("  Play again? [y/N] ").strip().lower() not in ("y", "yes"):
                return
            seed = None if seed is None else seed + 1
    except (KeyboardInterrupt, EOFError):
        print("\n  Bye!")


if __name__ == "__main__":
    main()
