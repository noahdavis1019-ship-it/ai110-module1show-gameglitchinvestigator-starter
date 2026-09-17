from logic_utils import check_guess, update_score, get_range_for_difficulty

# FIX: check_guess returns (outcome, message), so the starter tests were
# comparing a tuple to a string. They now look at the outcome only.


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- New tests for the bugs I fixed ---

def test_too_high_hint_says_go_lower():
    # Bug 1: a guess above the secret used to say "Go HIGHER"
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message


def test_string_secret_is_compared_as_a_number():
    # Bug 2: "9" > "50" alphabetically, but 9 is lower than 50
    outcome, message = check_guess(9, "50")
    assert outcome == "Too Low"


def test_wrong_guess_never_adds_points():
    # Bug 5: a "Too High" guess on an even attempt used to add 5
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too Low", 3) == -5


def test_first_try_win_is_100_points():
    assert update_score(0, "Win", 1) == 100


def test_hard_range_is_bigger_than_normal():
    # Bug 6: Hard used to be 1-50
    assert get_range_for_difficulty("Hard") == (1, 200)
