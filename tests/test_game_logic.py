import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import importlib

import streamlit as st
import app
from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high_hint_is_correct():
    # If secret is 50 and guess is 60, message should guide the player lower
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low_hint_is_correct():
    # If secret is 50 and guess is 40, message should guide the player higher
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_attempts_start_at_zero_after_new_game():
    # The app should initialize attempts at 0 (not 1), so you get the full attempt_limit.
    st.session_state.clear()
    importlib.reload(app)
    assert st.session_state.attempts == 0
