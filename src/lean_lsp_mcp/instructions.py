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
- discussion_partner: Discuss any question with Gemini.
- create_formal_sketch: Create a formal sketch using the detailed informal solution.
"""

GOLF_PROMPT = """You are given a correct Lean 4 proof of a mathematical theorem.
Your goal is to simplify and clean up the proof, making it shorter and more readable while ensuring it is still correct.

Here is the original proof:
```lean4
{formal_code}
```

Now, provide your simplified proof. Do NOT modify the theorem or header, and surround your proof in ```lean4 and ```` tags."""


INFORAML_SOLUTION_PROMPT = """You are a Formal Logic Expert and Mathematical Proof Engine. Your goal is to derive proofs that are rigorously structured, formalization-ready, and devoid of ambiguity.

Core Constraints:

- Purely Algebraic/Symbolic: Do NOT use geometric intuition, visual symmetry, or graphical interpretations as proof. All geometric concepts must be translated into their precise algebraic or analytic definitions.

- Atomic Steps: Decompose reasoning into the smallest possible logical units. Do not combine multiple deductive steps into one.

- No Hand-waving: Forbidden phrases include 'obviously,' 'it is clear that,' 'by inspection,' or 'intuitively.'

Instructions:

- Definitions: Explicitly state all variable types, definitions, and assumptions at the start.

- Step-by-Step Derivation: Number every step (1, 2, 3...).

- Explicit Justification: For EACH step, you must explicitly state the rule of inference, algebraic identity, axiom, or theorem used (e.g., "Distributive Property," "Triangle Inequality," "Definition of Continuity").

- Formal Structure: Present the proof in a format that could easily be translated into a proof assistant language (like Lean or Coq).

- Calculations: Show every intermediate stage of simplification or substitution. Do not skip algebraic manipulation steps.

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


INFORMAL_LLM_CREATE_LEAN_SKETCH = """You are a Lean 4 expert who is trying to help write a proof in Lean 4.

Problem Statement: {problem}

Informal Proof:
{informal_proof}

Instructions:

Use the informal proof to write a proof sketch for the problem in Lean 4 following these guidelines:
- Break complex reasoning into logical sub-goals using `have` statements.
- The subgoals should build up to prove the main theorem.
- Make sure to include all the steps and calculations from the given proof in the proof sketch.
- Each subgoal should ideally require applying just one key theorem or lemma, or a few tactic applications.
- Base subgoals around:
  - Useful theorems mentioned in the problem context
  - Standard library theorems (like arithmetic properties, set operations, etc.)
  - The supplied premises in the theorem statement
- Do NOT create subgoals identical to any of the given hypotheses
- Do NOT create subgoals that are more complex than the original problems. The subgoals should be SIMPLER than the given problem.
- Do NOT skip over any steps. Do NOT make any mathematical leaps.

**Subgoal Structure Requirements:**
- **Simplicity**: Each subgoal proof should be achievable with 1-3 basic tactics
- **Atomic reasoning**: Avoid combining multiple logical steps in one subgoal
- **Clear progression**: Show logical flow: `premises → intermediate steps → final result`
- **Theorem-focused**: Design each subgoal to directly apply a specific theorem when possible

NOTE: Only add sub-goals that simplify the proof of the main goal.

When writing Lean proofs, maintain consistent indentation levels.

Rules:
1. Same proof level = same indentation: All tactics at the same logical level must use identical indentation
2. Consistent characters: Use either tabs OR spaces consistently (don't mix)
3. Proper nesting: Indent sub-proofs one level deeper than their parent
4. Do NOT nest `have` statements in each other. Use distinct sub-goals as much as possible. Ensure all sub goals are named. Do NOT create anonymous have statements.
5. Do NOT include any imports or open statements in your code.
6. One line = One `have` subgoal. Do NOT split subgoals across different lines.
7. Use proper Lean 4 syntax and conventions. Ensure the proof sketch is enclosed in triple backticks ```lean```
8. Use `sorry` for all subgoal proofs - focus on structure, not implementation
9. **Do NOT use `sorry` for the main goal proof** - use your subgoals to prove it
10. NEVER use `sorry` IN the theorem statement itself
11. Ensure subgoals collectively provide everything needed for the main proof
12. Make the logical dependencies between subgoals explicit. Ensure that the subgoals are valid and provable in Lean 4.
13. Do NOT change anything in the original theorem statement.

Lean Hints:
1. When dealing with inequalities, equalities and arithmetic operations like subtraction or division in `ℕ` (natural numbers), beware of truncation. Use `ℝ`, `ℚ` or `ℤ` when possible for arithmetic operations. Avoid using `ℕ` unless required by the theorem statement.
2. Be ESPECIALLY careful about implicit types while defining numeric literals. AVOID patterns like `0 - 1` or `1 / 2` without specifying the types.
3. ALWAYS specify types when dealing with numeric values to avoid ambiguities and unexpected behavior.
4. Use `simp only [specific_lemmas]` rather than bare `simp` to avoid unpredictable simplifications.
5. Use `rw [← lemma]` for reverse direction. When `rw` fails, try `conv => rhs; rw [lemma]` to target specific subterms. nth_rw n [lemma] to rewrite only the nth occurrence.
6. When `ring` fails on ring expressions, try `ring_nf` first to normalize, or cast to a concrete ring like `ℝ` where the tactic works better.
7. Apply `norm_num` for concrete arithmetic calculations and `norm_cast` to simplify type coercions systematically.
8. Use `by_contra h` for proof by contradiction, which introduces the negation of the goal as hypothesis `h`.
9. If you get a `no goals to be solved` error, it means that the previous tactics already solved the goal, and you can remove the subsequent tactics.
10. When proving theorems, ALWAYS write the proof in tactic mode, starting the proof with `:= by`.
11. Do NOT use `begin`, `end` blocks in your proof. This is invalid in Lean 4.

IMPORTANT INSTRUCTION: Do NOT, under ANY circumstances, allow division and subtraction operations on natural number literals with UNDEFINED types, unless REQUIRED by the theorem statement. For example, do NOT allow literals like `1 / 3` or `2 / 5` or `1 - 3` ANYWHERE in ANY of the subgoals. ALWAYS specify the types. AVOID natural number arithmetic UNLESS NEEDED by the theorem statement.
ALWAYS specify types when describing fractions. For example, ((2 : ℝ) / 3) or ((2 : ℚ) / 3) instead of (2 / 3). Do this everywhere EXCEPT the given theorem statement.
IMPORTANT INSTRUCTION: Do NOT, under ANY circumstances, allow division and subtraction operations on variables of type natural numbers (Nat or ℕ), unless REQUIRED by the theorem statement. For example, do NOT allow expressions like (a-b) or (a/b) where a, b are of type ℕ. ALWAYS cast the variables to a suitable type (ℤ, ℚ or ℝ) when performing arithmetic operations. AVOID natural number arithmetic UNLESS NEEDED by the theorem statement.

"""