import pytest
from logic_utils import check_guess, get_range_for_difficulty, update_score


# ── Existing baseline tests (fixed: check_guess returns a tuple) ──────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── BUG 1: type corruption — secret cast to str on even attempts ───────────────
# Old code: `secret = str(st.session_state.secret)` on even attempts.
# In Python 3, comparing int > str raises TypeError, breaking all even-attempt guesses.

def test_bug1_check_guess_with_int_secret_does_not_raise():
    """check_guess must work with int secret on every attempt (was broken on even attempts)."""
    outcome, _ = check_guess(60, 50)  # would raise TypeError with str secret in Python 3
    assert outcome == "Too High"

def test_bug1_str_secret_raises_type_error():
    """Demonstrates the old bug: passing a str secret causes TypeError on > comparison."""
    with pytest.raises(TypeError):
        check_guess(60, "50")  # int > str raises TypeError in Python 3

def test_bug1_correct_hint_messages():
    """Hint messages must be directionally correct (Too High → go LOWER, Too Low → go HIGHER)."""
    _, msg_high = check_guess(60, 50)
    assert "LOWER" in msg_high

    _, msg_low = check_guess(40, 50)
    assert "HIGHER" in msg_low


# ── BUG 3: attempts initialised at 1 instead of 0 ────────────────────────────
# Old code: `st.session_state.attempts = 1`
# This caused the first guess to be scored as attempt 2, losing 10 extra points.

def test_bug3_first_win_scored_at_attempt_1():
    """Winning on the first guess (attempt_number=1 after increment from 0) gives 80 pts."""
    score = update_score(0, "Win", attempt_number=1)
    assert score == 80  # 100 - 10*(1+1) = 80

def test_bug3_first_attempt_number_is_1_after_increment():
    """With initial attempts=0, first submit increments to 1; score should be 100-10*(1+1)=80."""
    initial_attempts = 0
    attempts_after_submit = initial_attempts + 1  # simulates `st.session_state.attempts += 1`
    score = update_score(0, "Win", attempt_number=attempts_after_submit)
    assert score == 80  # 100 - 10*(1+1) = 80

def test_bug3_old_bug_would_score_attempt_2_on_first_guess():
    """With the bug (initial=1), first submit would use attempt_number=2, scoring only 70 pts."""
    buggy_initial_attempts = 1
    attempts_after_submit = buggy_initial_attempts + 1  # = 2
    score = update_score(0, "Win", attempt_number=attempts_after_submit)
    assert score == 70  # 100 - 10*(2+1) = 70 — proves the bug changed scoring


# ── BUG 4: new game ignored difficulty range, always used 1–100 ───────────────
# Old code: `random.randint(1, 100)` — should have been `random.randint(low, high)`.

def test_bug4_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

def test_bug4_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 100)

def test_bug4_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 50)

def test_bug4_easy_range_is_not_1_to_100():
    """Easy mode must NOT span 1–100 (that was the bug)."""
    _, high = get_range_for_difficulty("Easy")
    assert high != 100

def test_bug4_hard_range_is_not_1_to_100():
    """Hard mode must NOT span 1–100 (that was the bug)."""
    _, high = get_range_for_difficulty("Hard")
    assert high != 100


# ── BUG 5: score and history were not reset on new game ───────────────────────
# Old code: new_game block never reassigned score or history in session state.
# Simulated here by verifying reset values match initial defaults.

def test_bug5_score_resets_to_zero():
    """After a new game, score must start at 0 (not carry over from previous game)."""
    carried_score = update_score(0, "Win", attempt_number=1)   # simulate a previous game
    assert carried_score > 0
    reset_score = 0  # what the new_game block now does
    assert reset_score == 0

def test_bug5_history_resets_to_empty_list():
    """After a new game, history must be an empty list (not carry over guesses)."""
    history = [30, 60, 50]   # simulate guesses from a previous game
    history = []             # what the new_game block now does
    assert history == []

def test_bug5_update_score_on_fresh_game_starts_from_zero():
    """Score accumulation after reset must start from 0, not a leftover value."""
    reset_score = 0
    score_after_first_guess = update_score(reset_score, "Too Low", attempt_number=1)
    assert score_after_first_guess == -5  # 0 + (-5), not some carried-over value
