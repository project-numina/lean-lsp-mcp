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


VERIFY_PROMPT = """## Instruction: 
Please act as a strict math grader. Review the following problem and the student's solution.

Task:

Go through the student's solution line by line. For each line, determine if the mathematical logic and calculation are valid based on the previous line.

Output Format:

Step 1: [Valid/Invalid] - [Reason]

Step 2: [Valid/Invalid] - [Reason]

...

Final Grade: [Pass/Fail]

## Input:

The Problem: {problem}

The Student's Solution: {student_solution}"""