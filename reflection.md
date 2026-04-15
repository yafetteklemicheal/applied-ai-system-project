## 💭 Reflection: Secret Number Investigator

### Limitations and Biases

The biggest limitation is API dependency — if Gemini is unavailable or rate limited, the hint system falls back to a static directional message, which is functional but loses the intelligence that makes the feature valuable. The free tier also introduces latency of 1-3 seconds per hint, which disrupts the flow of gameplay.

There is also a subtle bias in the hint variety. The prompt instructs Gemini to vary hint types, but in practice it defaults to directional and proximity hints most often. Parity and mathematical hints appear less frequently even when they would be more useful, meaning the hint quality is inconsistent across sessions.

Finally, the confidence score is self-reported by the same model generating the hint. There is no external validator checking whether the confidence rating is actually calibrated. It is possible for a model to be confidently wrong.

---

### Misuse and Prevention

Misuse potential of in this scenario is low. The secret number is passed directly into the prompt, so a user inspecting API traffic could technically obtain it. It may be necessary to pass only derived context like direction and difference to the API rather than the secret number itself for future versions of the app.

Prompt injection is a concern, but is mitigated here because `parse_guess` validates input as a numeric value only, rejecting any string that is not a number before it ever reaches the AI.

---

### What Surprised Me During Testing

The most surprising finding was how sensitive the hint quality was to prompt structure. Early versions of the prompt produced generic, repetitive hints. Once specific values like difference, parity, and attempts remaining were added to the context, the hints became noticeably more varied and useful without changing the model or any other settings.

---

### AI Collaboration

Throughout this project, AI was used for three purposes: generating or refactoring the game code based on carefully designed prompts, and assiting with debugging logic errors.

**Helpful suggestion:** When the hint direction logic was producing incorrect guidance, the AI correctly identified that the `direction` variable had the labels reversed — `"higher"` and `"lower"` were swapped in the conditional. This was a bug that was easy to miss, and having it flagged immediately saved significant time.

**Flawed suggestion:** The AI initially suggested a scoring formula that made it impossible to accumulate a positive score. It penalized every incorrect guess and with no weight added for guessing the secret number, which made the scoring feel punishing and unbalanced. The formula had to be redesigned manually to ensure wins produced meaningful point gains.