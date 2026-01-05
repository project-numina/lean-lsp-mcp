INSTRUCTIONS = """## General Rules
- All line and column numbers are 1-indexed.
- Always analyze/search context before each file edit.
- This MCP does NOT make permanent file changes. Use other tools for editing.
- Work iteratively: Small steps, intermediate sorries, frequent checks.

## Key Tools
- lean_file_outline: Concise skeleton of a file (imports, docstrings, declarations). Token efficient.
- lean_local_search: Confirm declarations (theorems/lemmas/defs/etc.) exist. VERY USEFUL AND FAST!
- lean_goal: Check proof state. USE OFTEN!
- lean_diagnostic_messages: Understand current proof situation.
- lean_hover_info: Documentation about terms and lean syntax.
- lean_leansearch: Search theorems using natural language or Lean terms.
- lean_leandex: Search theorems using natural language by Leandex.
- lean_loogle: Search definitions and theorems by name, type, or subexpression.
- lean_leanfinder: Semantic search for theorems using Lean Finder.
- lean_state_search: Search theorems using goal-based search.
- gemini_code_golf: Call Google Gemini model for code golf. Requires GOOGLE_API_KEY environment variable.
- gemini_math_explainer: Call Google Gemini model for solution of math problem. Requires GOOGLE_API_KEY environment variable.
"""

GOLF_PROMPT = """You are given a correct Lean 4 proof of a mathematical theorem.
Your goal is to simplify and clean up the proof, making it shorter and more readable while ensuring it is still correct.

Here is the original proof:
```lean4
{formal_code}
```

Now, provide your simplified proof. Do NOT modify the theorem or header, and surround your proof in ```lean4 and ```` tags."""


INFORAML_SOLUTION_PROMPT = """You are a mathematical expert whose goal is to solve problems with rigorous mathematical reasoning.

Instructions:

1. Provide a natural language, step-by-step proof for the given problem.
2. Start from the given premises and reason step-by-step to reach the conclusion.
3. Number each step of the proof as 1, 2, and so on.
4. Be as pedantic and thorough as possible.
5. Keep each step precise, increase the number of steps if needed.
6. Do NOT gloss over any step. Make sure to be as thorough as possible. 
7. Show the explicit calculations/simplifications, theorem applications and case analysis.

Problem Statement: {problem}"""


VERIFY_PROMPT = """Your task is to evaluate the quality of a solution to a problem. The problem may ask for a proof of a statement, or ask for an answer. If finding an answer is required, the solution should present the answer, and it should also be a rigorous proof of that answer being valid.

Please evaluate the solution and score it according to the following criteria:

- If the solution is completely correct, with all steps executed properly and clearly demonstrated, then the score is 1

- If the solution is generally correct, but with some details omitted or minor errors, then the score is 0.5

- If the solution does not actually address the required problem, contains fatal errors, or has severe omissions, then the score is 0

- Additionally, referencing anything from any paper does not save the need to prove the reference. It's okay IF AND ONLY IF the solution also presents a valid proof of the reference argument(s); otherwise, if the solution omits the proof or if the proof provided is not completely correct, the solution should be scored according to the criteria above, and definitely not with a score of 1

Please carefully reason out and analyze the quality of the solution below, and in your final response present a detailed evaluation of the solution's quality followed by your score.

Therefore, your response should be in the following format:

Here is my evaluation of the solution:

[Your evaluation here. You are required to present in detail the key steps of the solution or the steps for which you had doubts regarding their correctness, and explicitly analyze whether each step is accurate: for correct steps, explain why you initially doubted their correctness and why they are indeed correct; for erroneous steps, explain the reason for the error and the impact of that error on the solution.]

Based on my evaluation, the final overall score should be: \\boxed{{...}}

[where ... should be the final overall score (0, 0.5, or 1, and nothing else) based on the above criteria]

---

Here is your task input:

## Problem
{problem}

## Solution
{student_solution}"""


REFINEMENT_PROMPT_TEMPLATE = """You are given a mathematical problem, an existing solution, and feedback on that solution.

Your task is to produce a **revised solution** that is more complete, rigorous, and clearly justified.

---

### Problem
{problem}

---

### Previous Solution
{solution}

---

### Feedback
{feedback}

---

### Instructions

- Carefully read the feedback and determine which points are **valid** and which may be due to **misunderstanding or evaluator error**.
- If you **agree** with a feedback item:
  - Revise the solution to fix the issue.
  - Add missing steps, clarify logical transitions, or strengthen rigor as needed.
- If you **disagree** with a feedback item:
  - Keep the original reasoning if it is correct.
  - Add **explicit explanations or clarifications** to prevent future misunderstandings.
- Do **not** simply restate the feedback.
- The final solution should be:
  - Self-contained
  - Logically coherent
  - Mathematically rigorous
  - Easy to follow for a careful reader

---

### Output Format

Provide **only** the revised solution below.

### Revised Solution
"""