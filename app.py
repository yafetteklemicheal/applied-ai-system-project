import random
import streamlit as st

from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 300px;
    }
    </style>
    <script>
    window.scrollTo(0, 0);
    </script>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Secret Number Investigator")
st.caption("A production-ready guessing game built by an AI")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 9,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty
elif st.session_state.current_difficulty != difficulty:
    # Difficulty changed, restart the game with the new range
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""
    st.session_state.hint_message = None
    st.session_state.show_hint_display = False
    st.session_state.balloons_shown = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "hint_message" not in st.session_state:
    st.session_state.hint_message = None

if "show_hint_display" not in st.session_state:
    st.session_state.show_hint_display = False

if "balloons_shown" not in st.session_state:
    st.session_state.balloons_shown = False

with st.sidebar.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

def reset_game():
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.current_difficulty = difficulty
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.guess_input = ""
    st.session_state.hint_message = None
    st.session_state.show_hint_display = False
    st.session_state.balloons_shown = False

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

if st.session_state.hint_message and st.session_state.show_hint_display:
    st.warning(st.session_state.hint_message)

with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key="guess_input"
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        submit = st.form_submit_button("Submit Guess 🚀")
    with col2:
        new_game = st.form_submit_button("New Game 🔁", on_click=reset_game)
    with col3:
        show_hint = st.checkbox("Show hint", value=True)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        if not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True
        st.success(f"You won! Final score: {st.session_state.score}. Start a new game to play again.")
    else:
        st.error(f"Game over. Final score: {st.session_state.score}. Start a new game to try again.")
    st.stop()

if submit:
    if not raw_guess.strip():
        st.error("Enter a guess")
    else:
        st.session_state.attempts += 1

        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.history.append(raw_guess)
            st.error(err)
        else:
            st.session_state.history.append(guess_int)

            outcome, message = check_guess(guess_int, st.session_state.secret)

            # Store hint in session state for persistent display
            if show_hint:
                st.session_state.hint_message = message
                st.session_state.show_hint_display = True
            else:
                st.session_state.hint_message = None
                st.session_state.show_hint_display = False

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.session_state.status = "won"
                st.success(
                    f"You won! The secret was {st.session_state.secret}. "
                    f"Final score: {st.session_state.score}"
                )
            else:
                if st.session_state.attempts >= attempt_limit:
                    st.session_state.status = "lost"
                    st.error(
                        f"Out of attempts! "
                        f"The secret was {st.session_state.secret}. "
                        f"Score: {st.session_state.score}"
                    )
        st.rerun()