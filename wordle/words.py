"""Word list loading and answer selection."""

import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DAILY_EPOCH = datetime.date(2026, 1, 1)


def _load(name: str) -> list[str]:
    path = DATA_DIR / name
    words = (line.strip().lower() for line in path.read_text().splitlines())
    return sorted({w for w in words if len(w) == 5 and w.isalpha()})


def load_answers() -> list[str]:
    return _load("answers.txt")


def load_allowed(answers: list[str]) -> set[str]:
    return set(_load("allowed.txt")) | set(answers)


def pick_random(answers: list[str], seed: int | None = None) -> str:
    return random.Random(seed).choice(answers)


def pick_daily(answers: list[str], today: datetime.date | None = None) -> str:
    """Same word for everyone on a given date, in a fixed shuffled order."""
    today = today or datetime.date.today()
    order = answers[:]
    random.Random("wordle-daily").shuffle(order)
    return order[(today - DAILY_EPOCH).days % len(order)]
