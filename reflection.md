# 💭 Reflection: Secret Number Investigator

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

The secret number would continue to change with each rerun if we continue to initialize it without checking if it already exists. If we dont check it then with every rerun, the secret number would generate a new random number between the low and high for the difficulty level set.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Its like a website that loads all the info when its start at first, and every time you interact with the website in any way, the screen and all the data displayed will refresh. This continues to happen without the user having to manually reload anything.

- What change did you make that finally gave the game a stable secret number?

The addition of the if statmeent before we initialize the secret number checks if the number has already been initialized and doesnt generate a new one if there is already one generated.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Designing prompts with intent to make sure the response it fine tuned to the problem we are trying to solve, rahter than giving a general instructions and having the AI give a lengthy general answer.

- What is one thing you would do differently next time you work with AI on a coding task?

Take some time to figure out what I want the AI to do so I can craft well thought out prompts so I get a response that actually solves my problem.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I learned how powerful it can be to have the burden of writing code removed from the engineers shoulders. Learning syntax and understanding data structures and algorithms is still crucial, but just as important is learning system design, and system design is exactly the skill I can develop by creating projects using AI generated code.
