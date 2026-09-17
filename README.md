# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** a number guessing game built with Streamlit. You pick a difficulty (Easy 1–20, Normal 1–100, Hard 1–200), guess the secret number, get "Go HIGHER" / "Go LOWER" hints, and score more points the fewer guesses you need.
- [x] **Bugs I found:**
  1. The hints were backwards (60 vs a secret of 50 said "Go HIGHER").
  2. On even attempts the secret was turned into a string, so numbers were compared alphabetically (9 counted as higher than 50).
  3. New Game didn't reset the win/loss status, score or history, so the game stayed locked after a win.
  4. Attempts started at 1 (7 of 8 shown), and typing a non-number used up an attempt.
  5. Scoring was wrong: some wrong guesses added 5 points, and a first-try win only gave 80.
  6. Hard (1–50) was easier than Normal, and the banner always said "1 and 100".
  7. The starter tests failed: `logic_utils.py` wasn't written yet, and the tests compared a tuple to a string.
- [x] **Fixes I applied:**
  - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` into `logic_utils.py` and imported them in `app.py`.
  - Swapped the hint messages back, and `check_guess` now converts both values with `int()`.
  - Deleted the code in `app.py` that turned the secret into a string.
  - New Game resets attempts, secret, score, status and history, using the current difficulty's range.
  - Attempts start at 0 and only count valid guesses.
  - Wrong guesses always cost 5 points, and a first-try win gives 100.
  - Hard is now 1–200, and the banner shows the real range.
  - Updated the starter tests to unpack `(outcome, message)`.

## 📸 Demo Walkthrough

Normal difficulty (1–100, 8 attempts). I opened Developer Debug Info and the secret was 50.

1. The game loads with "Guess a number between 1 and 100. Attempts left: 8" and a score of 0.
2. I guess **60**. The hint says "📉 Go LOWER!", attempts go to 1, and the score is -5.
3. I guess **40**. The hint says "📈 Go HIGHER!", attempts go to 2, and the score is -10.
4. I guess **9**. The hint says "📈 Go HIGHER!", attempts go to 3, and the score is -15.
5. I type **abc**. It shows "That is not a whole number." Attempts stay at 3.
6. I guess **50**. It shows "🎉 Correct!" with balloons and "You won! The secret was 50. Final score: 55".
7. I click **New Game**. Attempts, score and history reset, and I can play again.
8. I switch to **Hard**. The banner says "Guess a number between 1 and 200. Attempts left: 5".

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0 -- /Users/noahdavis/Downloads/gameglitch/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/noahdavis/Downloads/gameglitch
plugins: anyio-4.15.1
collecting ... collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 28%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 35%]
tests/test_game_logic.py::test_string_secret_is_compared_as_a_number PASSED [ 42%]
tests/test_game_logic.py::test_wrong_guess_never_adds_points PASSED      [ 50%]
tests/test_game_logic.py::test_first_try_win_is_100_points PASSED        [ 57%]
tests/test_game_logic.py::test_hard_range_is_bigger_than_normal PASSED   [ 64%]
tests/test_game_logic.py::test_decimal_guess_is_rejected PASSED          [ 71%]
tests/test_game_logic.py::test_empty_or_spaces_guess_is_rejected PASSED  [ 78%]
tests/test_game_logic.py::test_negative_guess_is_too_low PASSED          [ 85%]
tests/test_game_logic.py::test_very_large_guess_is_too_high PASSED       [ 92%]
tests/test_game_logic.py::test_late_win_still_gets_10_points PASSED      [100%]

============================== 14 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [x] **Challenge 1: Advanced Edge-Case Testing.** Added 5 edge-case tests (decimals, empty input, negative numbers, huge numbers, very late wins) at the bottom of `tests/test_game_logic.py`. Prompts and reasons are in `ai_interactions.md`.
