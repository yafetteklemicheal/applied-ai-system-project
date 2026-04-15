import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_hint(guess: int, secret: int, low: int, high: int, attempts_left: int, difficulty: str):
    """
    Generate an AI-powered hint using Gemini API.
    
    Returns a varied hint including directional, range, temperature, mathematical,
    parity, proximity, or urgency hints.
    """
    try:
        # Determine the direction
        if guess > secret:
            direction = "lower"
            difference = guess - secret
        else:
            direction = "higher"
            difference = secret - guess
        
        # Determine if the number is odd or even
        parity = "odd" if secret % 2 == 1 else "even"
        
        # Create a prompt for Gemini to generate a creative hint
        prompt = f"""You are a hint generator for a number guessing game.

Context: secret={secret}, guess={guess}, direction={direction}, difference={difference}, range={low}-{high}, attempts_left={attempts_left}, parity={parity}, difficulty={difficulty}

Give ONE short encouraging hint (1-2 sentences) to help narrow down the range. Vary between: directional, range narrowing, temperature, mathematical, parity, proximity, or urgency hints.

On a new line add: Hint Accuracy Confidence: X%"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=80)
        )
        hint = response.text.strip()
        return hint
    except Exception as e:
        # Fallback to simple hint if API fails
        print(f"AI Hint Error: {e}")  # Debug: print the actual error
        if guess > secret:
            return f"📉 Go LOWER!"
        else:
            return f"📈 Go HIGHER!"


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score