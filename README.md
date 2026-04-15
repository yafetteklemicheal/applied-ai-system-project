# 🎮 Secret Number Investigator

A number guessing game powered by AI-generated hints using the Gemini API.

---

## Original Project

This project originated as **Game Glitch Investigator**, a Streamlit-based number guessing game that was intentionally shipped with bugs. The original goals were to find and fix real bugs in AI-generated code — including broken hints, incorrect attempt tracking, and unstable game state. The base game allowed players to guess a secret number within a range, with difficulty settings and a scoring system. Using the project as a foundation, it has now been upgraded and rebranded to **Secret Number Investigator**

---

## Title and Summary

**Secret Number Investigator** is an interactive number guessing game where players try to guess a secret number within a limited number of attempts. What makes it different from a standard guessing game is the AI-powered hint system — on every incorrect guess, the game calls Google's Gemini API to generate a contextual, varied hint based on the current game state. Rather than always saying "go higher" or "go lower," the AI reasons about the guess, the remaining attempts, the difficulty, and the parity of the secret number to give the most useful hint possible. This makes the game more engaging and demonstrates how AI can enhance even simple applications.

---

## Architecture Overview

The system is split into two files. `app.py` handles all Streamlit UI logic, session state, and user interaction. `logic_utils.py` contains the core game logic and AI integration.

Data flows as follows: the player enters a guess through the Streamlit form → `parse_guess` validates the input → `check_guess` compares it to the secret number → `update_score` adjusts the score → if the guess is incorrect and hints are enabled, `get_ai_hint` constructs a prompt with full game context and calls the Gemini API → the returned hint is displayed to the player. If the API fails, a static directional fallback is returned so the game never breaks. A developer debug panel in the sidebar exposes live session state for transparency and testing.

See the system diagram in the repository for a visual representation of this flow.

---

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yafetteklemicheal/applied-ai-system-project.git
cd secret-number-investigator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

5. Run the app:
```bash
streamlit run app.py
```

---

## Sample Interactions

**Example 1 — Far off guess on Normal difficulty**
- Secret number: 60, Guess: 12, Attempts left: 7
- AI hint: "You're quite a distance away — the number is much higher than 12, think closer to the upper half of the range."

**Example 2 — Close guess with few attempts remaining**
- Secret number: 45, Guess: 52, Attempts left: 2
- AI hint: "You're close but a bit high — with only 2 attempts left, try somewhere in the low 40s."

**Example 3 — Parity-based hint on Hard difficulty**
- Secret number: 317, Guess: 200, Attempts left: 5
- AI hint: "You need to go higher, and here's a clue — the secret number is odd."

---

## Design Decisions

**Why Gemini over other APIs?** Gemini's free tier is generous enough for a game context with no cost barrier for anyone running the project locally.

**Why keep a static fallback?** API calls can fail due to rate limits or network issues. The fallback ensures the game always works even without AI hints, which is important for a reliable user experience.

**Why `logic_utils.py` as a separate file?** Separating game logic from UI logic makes the code testable with pytest without needing to run Streamlit. It also makes it easy to swap out the AI provider in one place.

**Trade-offs:** The AI hint adds 1-3 seconds of latency per guess. This is acceptable for a game but would need a loading indicator in a production app. The hint quality also depends on the model's free tier response time, which can vary. To minimize latency, AI hint have been limited to 80 tokens per response which will reduce not just latency, but also tokens used for hint generation.

---

## Testing Summary

Tests were written using `pytest` and cover the four core logic functions in `logic_utils.py`:

- `parse_guess` — handles valid integers, floats, empty strings, and non-numeric input
- `check_guess` — correctly returns Win, Too High, and Too Low outcomes
- `update_score` — validates scoring logic for wins and incorrect guesses
- `get_range_for_difficulty` — confirms correct ranges for all three difficulty levels

All tests pass. The AI hint function is not unit tested directly due to its external API dependency, but the fallback behavior is verified manually by disabling the API key and confirming the static hints appear correctly.

**What was learned:** Separating logic from UI early made testing straightforward. The biggest challenge was ensuring the hint direction logic was correct — an early bug had the direction labels reversed, causing the AI to confidently give the wrong advice.

---

## Reflection

This project taught me that AI works best when it receives structured, specific context rather than vague prompts. Early versions of the hint prompt produced generic responses — once the prompt was tightened to include exact values like the difference, parity, range, and attempts remaining, the hints became noticeably more useful and varied.

It also reinforced that AI-generated code requires the same scrutiny as human-written code. The original codebase had subtle bugs that were easy to miss — incorrect hint direction logic, off-by-one errors in attempt counting, and unstable session state. Debugging AI-generated code is a real and necessary skill.

Finally, integrating a live API into an application requires thinking about failure modes from the start. The fallback hint system was not an afterthought, but rather a design requirement. The mindset of "what happens when the AI fails" is something every AI engineer needs to develop.