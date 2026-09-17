# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:** "Here are `parse_guess`, `check_guess` and `update_score` from logic_utils.py after my fixes. What are some edge-case inputs that could still break them? Write one short, simple pytest test for each."

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Decimal like `4.9` | Prompt above | `test_decimal_guess_is_rejected` | Yes | The starter quietly turned 4.9 into 4, which hides a typo from the player. |
| Empty or spaces-only input | Prompt above | `test_empty_or_spaces_guess_is_rejected` | Yes | Streamlit sends `""` before you type anything, and `"   "` used to reach `int()` and fail. |
| Negative number `-5` | Prompt above | `test_negative_guess_is_too_low` | Yes | Negatives are valid ints, so the comparison still has to give the right hint. |
| Huge number `99999999999` | Prompt above | `test_very_large_guess_is_too_high` | Yes | Makes sure very large numbers don't crash the comparison. |
| Win after 20 attempts | Prompt above | `test_late_win_still_gets_10_points` | Yes | Checks the 10-point minimum so the win formula can't go negative. |

**Suggestion I changed:** Claude first used `pytest.mark.parametrize` to run many inputs through one test. I rewrote them as separate small tests so each one is easy to read and matches one edge case in this table.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
