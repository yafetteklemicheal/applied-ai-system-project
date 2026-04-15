
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import importlib

import streamlit as st
import app
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

# --- check_guess ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

def test_guess_too_high_hint_is_correct():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low_hint_is_correct():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_check_guess_boundary_one_above():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"

def test_check_guess_boundary_one_below():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"


# --- parse_guess ---

def test_parse_guess_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_guess_valid_float_truncates():
    ok, val, err = parse_guess("42.9")
    assert ok is True
    assert val == 42

def test_parse_guess_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_guess_none_input():
    ok, val, err = parse_guess(None)
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_guess_non_numeric():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_guess_negative_number():
    ok, val, err = parse_guess("-5")
    assert ok is True
    assert val == -5


# --- update_score ---

def test_update_score_win_early():
    # Win on attempt 1 should give max points
    score = update_score(0, "Win", 1)
    assert score > 0

def test_update_score_win_minimum_points():
    # Win very late should still give at least 10 points
    score = update_score(0, "Win", 20)
    assert score >= 10

def test_update_score_too_low_decrements():
    score = update_score(50, "Too Low", 1)
    assert score < 50

def test_update_score_too_high_even_attempt_increments():
    score = update_score(50, "Too High", 2)
    assert score > 50

def test_update_score_too_high_odd_attempt_decrements():
    score = update_score(50, "Too High", 1)
    assert score < 50

def test_update_score_unknown_outcome_unchanged():
    score = update_score(50, "Unknown", 1)
    assert score == 50


# --- get_range_for_difficulty ---

def test_range_easy():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_range_normal():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_range_hard():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 500

def test_range_easy_is_smaller_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_range_normal_is_smaller_than_hard():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert normal_high < hard_high


# --- session state ---

def test_attempts_start_at_zero_after_new_game():
    st.session_state.clear()
    importlib.reload(app)
    assert st.session_state.attempts == 0