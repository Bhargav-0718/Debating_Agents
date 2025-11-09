"""Rating and Feedback System for Debate Agents.

Enhancements:
 - Structured JSON output requested from judge to reduce ambiguous formatting.
 - Explicit multi-criteria rubric (clarity, evidence, logic, rhetoric, responsiveness).
 - Differentiation requirement to discourage identical overall scores without justification.
 - Robust parser that first attempts JSON parsing, then falls back to legacy pattern parsing.
"""

from crewai import Task, Crew, Process
from textwrap import dedent
import json
import re
from typing import Tuple

RUBRIC_TEXT = dedent(
    """Use this RUBRIC for each debater (score each 1–5, integers only):
    - Clarity: Was the argument easy to follow and structured?
    - Evidence: Did they use relevant facts/examples/support?
    - Logic: Was reasoning valid and internally consistent?
    - Rhetoric: Was style persuasive & engaging (aligned with their persona)?
    - Responsiveness: Did they address opponent's points directly?

    Overall Score Guidance (1–5):
      1 = Poor: Multiple major flaws; reasoning unclear or incorrect
      2 = Below Average: Some structure but weak support / notable logical gaps
      3 = Average: Competent; mix of strengths & weaknesses; acceptable coherence
      4 = Good: Solid reasoning & support; minor issues only
      5 = Excellent: Compelling, precise, well-supported, strategically strong

    Avoid giving both debaters the same overall score unless their criteria subtotals are genuinely close. If you give same overall, explain precise parity in 'differentiation_reason'.
    """
)


def generate_detailed_ratings(
    judge_agent,
    debater1_name: str,
    debater2_name: str,
    debater1_stance: str,
    debater2_stance: str,
    debate_transcript: str,
    topic: str,
) -> Tuple[int, int, str, str]:
    """Generate detailed ratings and feedback for both debaters.

    Returns:
        (debater1_rating, debater2_rating, debater1_feedback, debater2_feedback)
    """

    rating_prompt = dedent(
        f"""
        You are {judge_agent.name}, a debate judge focusing on: {judge_agent.focus}.

        Debate Topic: "{topic}"
        Debater 1: {debater1_name} (stance: {debater1_stance.upper()})
        Debater 2: {debater2_name} (stance: {debater2_stance.upper()})

        Transcript:
        {debate_transcript}

        {RUBRIC_TEXT}

        TASK: Evaluate each debater rigorously. First assign per-criterion scores, then derive the overall (not an average—holistic judgment). Provide targeted strengths and improvements separately.

        OUTPUT FORMAT (valid JSON ONLY, no commentary outside JSON):
        {{
          "debater1": {{
            "overall": <int 1-5>,
            "criteria": {{
              "clarity": <int>,
              "evidence": <int>,
              "logic": <int>,
              "rhetoric": <int>,
              "responsiveness": <int>
            }},
            "feedback_strengths": "<comma-separated or sentences>",
            "feedback_improvements": "<comma-separated or sentences>",
            "justification": "<2-3 sentences giving a holistic justification>"
          }},
          "debater2": {{
            "overall": <int 1-5>,
            "criteria": {{
              "clarity": <int>,
              "evidence": <int>,
              "logic": <int>,
              "rhetoric": <int>,
              "responsiveness": <int>
            }},
            "feedback_strengths": "<comma-separated or sentences>",
            "feedback_improvements": "<comma-separated or sentences>",
            "justification": "<2-3 sentences giving a holistic justification>"
          }},
          "differentiation_reason": "<Explain why scores differ OR why they are identical>"
        }}

        RULES:
        - Must be valid JSON.
        - Use integers only for scores.
        - Use full scale when justified; do not default both to 4.
        - Avoid markdown.
        """
    )

    task = Task(
        description=rating_prompt,
        agent=judge_agent.agent,
        expected_output="Valid JSON object containing ratings, criteria, and feedback."
    )

    crew = Crew(
        agents=[judge_agent.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    raw_text = str(result)
    return parse_rating_response(raw_text, debater1_name, debater2_name)


def _safe_int(value, default=3):
    try:
        iv = int(value)
        if 1 <= iv <= 5:
            return iv
    except Exception:
        pass
    return default


def parse_rating_response(response: str, debater1_name: str, debater2_name: str) -> Tuple[int, int, str, str]:
    """Parse the rating response.

    Attempt JSON parsing first. If it fails, fall back to legacy pattern parsing.
    Returns overall ratings and combined feedback strings for each debater.
    """
    # Try JSON
    try:
        json_start = response.find('{')
        json_end = response.rfind('}')
        if json_start != -1 and json_end != -1:
            json_blob = response[json_start: json_end + 1]
            data = json.loads(json_blob)
            d1 = data.get('debater1', {})
            d2 = data.get('debater2', {})
            r1 = _safe_int(d1.get('overall', 3))
            r2 = _safe_int(d2.get('overall', 3))
            fb1_parts = [
                d1.get('feedback_strengths', ''),
                d1.get('feedback_improvements', ''),
                d1.get('justification', ''),
            ]
            fb2_parts = [
                d2.get('feedback_strengths', ''),
                d2.get('feedback_improvements', ''),
                d2.get('justification', ''),
            ]
            fb1 = ' '.join(p.strip() for p in fb1_parts if p and p.strip()) or f"Good effort from {debater1_name}."
            fb2 = ' '.join(p.strip() for p in fb2_parts if p and p.strip()) or f"Good effort from {debater2_name}."
            return r1, r2, fb1, fb2
    except Exception as e:
        print(f"Rating JSON parse failed, falling back. Error: {e}")

    # Legacy pattern fallback
    try:
        lines = response.split('\n')
        debater1_rating = 3
        debater2_rating = 3
        debater1_feedback = f"Good effort from {debater1_name}."
        debater2_feedback = f"Good effort from {debater2_name}."

        rating1_pattern = re.compile(r"RATING_1:\s*(\d)")
        rating2_pattern = re.compile(r"RATING_2:\s*(\d)")

        for i, line in enumerate(lines):
            line = line.strip()
            m1 = rating1_pattern.match(line)
            m2 = rating2_pattern.match(line)
            if m1:
                debater1_rating = _safe_int(m1.group(1), 3)
            elif m2:
                debater2_rating = _safe_int(m2.group(1), 3)
            elif line.startswith('FEEDBACK_1:'):
                debater1_feedback = line.replace('FEEDBACK_1:', '').strip()
            elif line.startswith('FEEDBACK_2:'):
                debater2_feedback = line.replace('FEEDBACK_2:', '').strip()

        return debater1_rating, debater2_rating, debater1_feedback, debater2_feedback
    except Exception as e:
        print(f"Legacy rating parse failed: {e}")
        return 3, 3, f"Good effort from {debater1_name}.", f"Good effort from {debater2_name}."


def display_rating_stars(rating: int) -> str:
    """Convert numeric rating to star display."""
    return "⭐" * rating + "☆" * (5 - rating)
