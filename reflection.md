# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran it, the game looked finished: a title, a difficulty picker in the sidebar, a guess box, and Submit / New Game buttons. Once I opened **Developer Debug Info** to see the secret, it was clear the hints were wrong. A guess of 60 against a secret of 50 told me to "Go HIGHER". After I won, the **New Game** button didn't let me play again. The banner also said "Attempts left: 7" on Normal before I had guessed at all, even though Normal allows 8. Running `pytest` on the starter failed all 3 tests with `NotImplementedError`.

**Game session trace** (starter code, Normal, secret = 50):
```text
Start: secret=50 attempts=1 info='Guess a number between 1 and 100. Attempts left: 7'
Guess   '60' -> ['Go HIGHER!'] | attempts=2 score=5 status=playing
Guess   '40' -> ['Go LOWER!'] | attempts=3 score=0 status=playing
Guess    '9' -> ['Go HIGHER!'] | attempts=4 score=5 status=playing
Guess  'abc' -> ['That is not a number.'] | attempts=5 score=5 status=playing
Guess   '50' -> ['Correct!', 'You won! The secret was 50. Final score: 35'] | attempts=6 score=35 status=won
Guess    '7' -> ['You already won. Start a new game to play again.'] | attempts=6 score=35 status=won
New Game -> attempts=0 score=35 status=won history=[60, 40, 9, 'abc', 50]
Exceptions: none
```

**Bugs found and where they come from:**
1. **Hints are backwards.** In `check_guess`, the `guess > secret` branch returns "📈 Go HIGHER!" and the else branch returns "📉 Go LOWER!".
2. **The secret becomes a string on even attempts.** `app.py` does `secret = str(st.session_state.secret)` when `attempts % 2 == 0`. Then `guess > secret` raises a `TypeError`, and the `except` block compares strings alphabetically, so `"9" > "50"` is `True` and 9 is called "Too High".
3. **New Game doesn't reset the game.** It only resets `attempts` and `secret`. `status` stays `"won"`, so the game stays locked, and the new secret always uses 1–100 no matter the difficulty.
4. **The attempt counter is off.** `attempts` starts at `1` (so 7 left instead of 8), and a non-number like `abc` still uses up an attempt.
5. **The score is wrong.** A "Too High" guess on an even attempt *adds* 5 points, and a first-try win gives 80 instead of 100 because of `attempt_number + 1`.
6. **Difficulty ranges don't make sense.** Hard is 1–50, which is easier than Normal's 1–100, and the banner always says "between 1 and 100".

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret 50, guess `60` | "Go LOWER" | "📈 Go HIGHER!" | none |
| Secret 50, guess `9` on attempt 4 | "Too Low" outcome, score -5 | Counted as "Too High" and score went **up** 0 → 5 | none (`check_guess(9, "50")` → `('Too High', ...)`) |
| Win with `50`, click **New Game**, guess `7` | Fresh game with score 0 | "You already won. Start a new game to play again." Score still 35 | none |
| Load the game on Normal | "Attempts left: 8" | "Attempts left: 7" | none |
| Run `pytest` | Starter tests pass | 3 failed | `NotImplementedError: Refactor this function from app.py into logic_utils.py` |

-------|-------------------|-----------------|------------------------|
| | | | |
| | | | |
| | | | |

---

## 2. How did you use AI as a teammate?

I used **Claude** as my AI coding assistant. I gave it `app.py`, `logic_utils.py` and the tests, and asked about one bug at a time.

**AI explanation of a bug:** I asked Claude to explain step by step why the hints felt random on some turns. It pointed to `secret = str(st.session_state.secret)` on even attempts. Comparing an int to a string raises a `TypeError`, and the `except` block then compares both as strings. Strings compare character by character, so `"9" > "50"` is `True`.

**Correct suggestion (accepted):** Claude suggested deleting the string conversion completely instead of adding more `try/except`, and swapping the two hint messages in `check_guess`. I checked it by calling `check_guess(60, 50)`, which now gives `("Too High", "📉 Go LOWER!")`, and `check_guess(9, "50")`, which now gives `"Too Low"`. I also added a pytest case for each.

**Suggestion I did not accept as written:** Claude's first rewrite was over-engineered for this project. It added a settings dictionary for difficulty, a `new_game_state()` helper that took a random number generator as an argument, and an extra Streamlit testing script. It worked, but it was harder to read than the bugs were to fix, and more than a small guessing game needs. I asked for a simpler version that keeps the starter's structure: plain `if` statements in `get_range_for_difficulty` and a New Game block that resets each value directly. I checked the simpler version with pytest (9 passed) and by replaying the same game as in Section 1.

**Misleading explanation:** Claude also said that because of the string bug, a correct guess could *never* win on an even attempt. When I tested `check_guess(50, "50")` on the starter code, it returned `"Win"`, because the `except` block has its own `if g == secret` check. The real damage was the wrong high/low outcomes and the score going up on wrong guesses, so that's what I wrote down in my bug log.

---

## 3. Debugging and testing your fixes

I counted a bug as fixed only when (1) a pytest case for it passed and (2) the same inputs from my bug log behaved correctly in the game.

- **pytest:** the 3 starter tests were failing because the functions in `logic_utils.py` weren't written yet, and because they compared the returned tuple to a string. After moving the logic over and changing those tests to unpack `outcome, message`, I added 6 more tests. `python -m pytest` shows **9 passed**.
- **One test that taught me something:** `test_string_secret_is_compared_as_a_number` checks `check_guess(9, "50")`. It showed that converting both values with `int()` in one place fixes the problem even if a string sneaks in from somewhere else.
- **Replaying the game:** same secret (50) and the same guesses as before the fixes:

```text
Start: secret=50 attempts=0 info='Guess a number between 1 and 100. Attempts left: 8'
Guess   '60' -> ['Go LOWER!'] | attempts=1 score=-5 status=playing
Guess   '40' -> ['Go HIGHER!'] | attempts=2 score=-10 status=playing
Guess    '9' -> ['Go HIGHER!'] | attempts=3 score=-15 status=playing
Guess  'abc' -> ['That is not a whole number.'] | attempts=3 score=-15 status=playing
Guess   '50' -> ['Correct!', 'You won! The secret was 50. Final score: 55'] | attempts=4 score=55 status=won
Guess    '7' -> ['You already won. Start a new game to play again.'] | attempts=4 score=55 status=won
New Game -> attempts=0 score=0 status=playing history=[]
Exceptions: none
Switch to Hard -> info='Guess a number between 1 and 200. Attempts left: 5'
```

Hints point the right way. `abc` doesn't use up an attempt. The score goes down on every wrong guess, and a win on attempt 4 earns 70 (-15 + 70 = 55). New Game resets everything, and Hard now uses 1–200.

- **AI and tests:** Claude suggested testing the exact inputs from my bug log (60 vs 50, and 9 vs "50"), so each test lines up with one row of the table.

---

## 4. What did you learn about Streamlit and state?

Streamlit runs your whole script again from top to bottom every time you click a button or type in a box. That's called a rerun. Normal variables get reset on every rerun, so if you wrote `secret = random.randint(1, 100)` it would pick a new number on every click. `st.session_state` is like a dictionary that survives reruns, so the secret, score and attempts need to live there. The starter did save them in session state, but New Game only reset some of them, which is why the game got stuck on "You already won."

---

## 5. Looking ahead: your developer habits

- **Habit to keep:** reproduce the bug with the same inputs before and after fixing it (I pinned the secret to 50 and used the same guesses each time), and turn each row of my bug log into a pytest case.
- **What I'd do differently:** tell the AI my skill level and "keep the existing structure" in the first prompt. Its first fix was more complicated than it needed to be, and I had to ask it to simplify.
- **How this changed my thinking:** code that runs without crashing can still be very wrong. I now test AI code with specific inputs instead of trusting that it looks right.

---

## 6. Mistakes I made while fixing the code

- **Fixed the hint in the wrong place.** My first attempt swapped the `"Too High"` and `"Too Low"` labels instead of the messages. The hints looked right on screen, but `update_score` got the wrong outcome, and `test_guess_too_high` failed. The labels were correct all along; only the "Go HIGHER" / "Go LOWER" text was backwards.
- **Patched the string bug with another `str()`.** To stop the `TypeError`, I first wrapped the guess in `str()` too, so both sides matched. The crash went away, but now *every* attempt compared alphabetically, and 9 counted as higher than 50. Converting both sides with `int()` was the real fix.
- **Left the old functions in `app.py` after the refactor.** I copied the functions into `logic_utils.py` but forgot to delete them from `app.py`. The game kept using the old buggy copies, so my fixes "didn't work" in the browser even though pytest passed. Deleting the duplicates and adding the import fixed it.
- **Put Streamlit code in `logic_utils.py`.** I added `import streamlit as st` to show an error message from `parse_guess`. Running pytest then printed Streamlit warnings, and the logic was no longer testable on its own. I moved all `st.` calls back into `app.py`.
- **Forgot that Streamlit reruns the whole script.** I reset the score by writing `score = 0` at the top of `app.py`. It reset on *every* button click, so the score never went below -5. It has to live in `st.session_state` and only be set once with `if "score" not in st.session_state`.
- **New Game only half-fixed.** I added `st.session_state.status = "playing"` but forgot `history` and `score`, so old guesses still showed in Debug Info. I caught it by clicking New Game after a win and checking every value in the panel.
- **Off-by-one in the win formula.** When I changed `attempts` to start at 0, I also changed the formula to `100 - 10 * attempt_number`. A first-try win then gave 90 instead of 100. Because attempts go up *before* scoring, the first guess is attempt 1, so the formula needed `attempt_number - 1`. `test_first_try_win_is_100_points` caught this.
- **`parse_guess(None)` crashed.** My new version called `raw.strip()` before checking for `None`, which raised `AttributeError: 'NoneType' object has no attribute 'strip'`. I moved the `raw is None` check first.
- **A test passed for the wrong reason.** One early test did `assert check_guess(60, 50)`, which is always `True` because a non-empty tuple is truthy. It passed even with the bug still there. I changed it to unpack `outcome, message` and compare `outcome == "Too High"`.
- **Changed difficulty and the secret was out of range.** After making Hard 1–200, I switched from Hard to Easy and the secret was still 143, so I couldn't win on a 1–20 range. I added a check that picks a new secret when the difficulty changes.

