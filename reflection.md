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

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
