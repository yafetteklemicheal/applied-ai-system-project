# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

UI looked good but the immediately the hints became an issue. The confetti and ballons looked good when the user guessed the correct number.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Bug 1 - Out of bounds guesses are allowed. I expected the app to restrict user submission to remain between 1 and 100 as is in the instructions. However, the app allows users to submit numbers outside of that range.

Bug 2 - Hints provided should nudge the user towards the correct answer but the hints were doing the opposite.

Bug 3 - I expected the app to allow the user to use all available attempts before displaying the "Out of attempts" message. Currently the message appears when the user has 1 attempt remaining.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude and Copilot.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI suggested the attempt counter was off by one which confirmed my suspicion. I then tested the refactored code by playing the game which was behaving as expected.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The IDE was marking the streamlit import line as a problem. When I asked the AI, it eagerly installed streamlit again even though it was already installed. The issue was that the python interpreter in the IDE was not the same version as the venv.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I asked the AI to generate test cases to verify if the bug was fixed and the code passed all test cases. I also ran the app to verify that it was behaving as expected.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran the app and started guessing the secret number. I updated my guess using the hints provided and eventually arrived at the secret number. This verified that the suggested hints were now nudging the user to the correct answer.

- Did AI help you design or understand any tests? How?

The AI did help me understand all the tests that it generated. I asked the AI to include a comment with each test explaining how it works which was very helpful.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
