# Wordle

A terminal Wordle clone in pure Python (3.10+, standard library only). Made to test Claude Code

## Play

```sh
python3 -m wordle            # random word
python3 -m wordle --daily    # today's word, same for everyone
python3 -m wordle --seed 42  # repeatable word
python3 -m wordle --no-color # plain-text markers instead of ANSI colors
```

Guess the 5-letter word in 6 tries. Green = right letter, right spot; yellow = in the
word, wrong spot; gray = not in the word. Colors are disabled automatically when
`NO_COLOR` is set or output isn't a terminal. Ctrl+C or Ctrl+D quits.

## Layout

- `wordle/game.py` — scoring and game state (no I/O)
- `wordle/words.py` — word list loading, random/daily selection
- `wordle/ui.py` — terminal rendering
- `wordle/__main__.py` — CLI and game loop
- `data/answers.txt` — curated list of possible answers
- `data/allowed.txt` — accepted guesses (5-letter words from `/usr/share/dict/words`
  plus `+s` plurals of its 4-letter words); answers are always accepted too

## Test

```sh
python3 -m unittest -v
```
