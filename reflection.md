# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1) The number entered keeps saying to go lower when the secret number was higher when we entered and the opposite when we need to go lower it kept going to say higher

2) The reset game button doesnt allow to submit the guess button once its reset

3) Easy says 6 attempts but gives the answer in 5 attempts when it should give it on the 6th attempt

4) The range of the number of attemps for easy is  smaller compared to the normal - The levels of difficulty have different attempts - Hard = 5, Easy = 6, Normal = 8 with ranges that dont seem to align with the difficulty level
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

1) I used Claude Chat on this project
2) One example that Claude suggested was for the error with regards to the high and low. It explained to me well regarding where and why the error was occuring as I asked with examples. This is a snippet of the explaination that it provided me :

    "String comparison is lexicographic, not numeric. So "9" > "42" is True because "9" > "4" character-by-character. This causes completely wrong hints — e.g., guessing 9 when the secret is 42 would say "Go HIGHER!" (correct numerically), but guessing 50 when secret is 42 would compare "50" vs "42" — "5" > "4", so it correctly says higher... but guessing 9 vs 90 would compare "9" > "9..." and break down.

    The root cause: The intentional type-switching on even attempts (str vs int) poisons the comparison logic into unreliable string ordering instead of numeric ordering."
This helped me understand the error and I asked it what could be done to fix it and move the logic to logic_utils and it showed me the suggestions which I verified before accepting
3) The AI wasn't incorrect when I was checking the code, one area I thought it mislead me was when I was trying to understand what the parse_guess function is doing and whether it removed its usage when trying to refactor the code but when I asked it again, it showed me that the function is still being used. However, when using AI to write test cases, it did write an incorrect test case which was trying to assert 80 == 90 but it found the error within itself and I specifically asked it to fix it so it fixed the test case accordingly

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
1) I individually read each of the logic and psedocoded it and then I tried running the streamlit run app.py to check each of the errors that have been fixed using the help of AI.
2) One of the tests that I checked was to ensure that the number entered gets the right hint of going higher or lower according to the secret number and once the number is guessed correctly, I made sure that once the new game is clicked, the history and score is cleared and reset. Once that is done, I checked to see if the game actually worked when I pressed submit guess button with the new game.
3) Yes, AI was used to create the pytest cases. Once each case was created, I looked over them to understand what was done and ever asked claude to explain me what each individual test does so that I can reconfirm my understanding.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

1) The secret number kept changing in the original app because interacting on the Streamlit app reran the entire python script from top to bottom. In the original app, the secret number was not protectured by a session_state guard, so every rerun would call the random integer generator again and assign a new secret number. 

2) I would explain it in the context of a webpage, letting them imagine that everytime they click a button or any interaction on the stremlit website it reloads the entire page from scratch. It basically causes python to re-execute the entire script from the top meaning any regular variable that was set initially gets thrown away and recreated fresh every time. The session state is like a small notepad that Streamlit keeps on the side and instead of writing a value to its regular variable that dissapers on the next rerun, using the st.session_state allows to store the value across reruns as long as they are in the same browser session. If they want the secret number to stay teh same while the player keeps guessing, it is import to store it in the session state once and read it back every rerun instead of generating a new one each time.

3) I understood that the st.session_state is Streamlit's way of persisting values acroos those reruns. By wrapping the assignment with an if "secret" not in st.session_state, the secret is only generated once when the session first starts, and the same value is reused on every subsequent rerun until a new game is started.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

1. One strategy that I would like to take is trying to understand existing code better with the help of AI. I think its important to identify the logic of the code and using that for testing where necessary so I would like to use that

2. I would prefer to read the code more before directly jumping into trying to ask the claude chat why I'm getting the error. Once I get a sense of an understandingm it makes sense to use AI to help get a faster understanding

3. One main way is to understand how much more efficient it is to use AI to understand someone else's code and to ensure that I am following the right strategies to prompt AI to get it to code how I would like it and also to understand to cross verify the code generated by AI because there are chances that AI could give wrong code and it important to ensure we are not just blindly following the code..
