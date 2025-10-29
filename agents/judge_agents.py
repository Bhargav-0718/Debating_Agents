from crewai import Agent

class JudgeAgent:
    """Wrapper around CrewAI Agent to evaluate debates with unique judging personalities."""

    def __init__(self, name, judging_style, focus, bio):
        self.name = name
        self.judging_style = judging_style
        self.focus = focus
        self.bio = bio
        self.agent = Agent(
            name=name,
            role="Debate Judge",
            goal="Evaluate debates and declare a winner objectively or according to your judging style.",
            backstory=(
                f"You are {name}, a debate judge known for your {judging_style}. "
                f"You focus on {focus} when evaluating arguments, maintaining integrity and insight in every decision."
            ),
        )

# --- Judge Pool ---
judge_pool = [
    JudgeAgent(
        "Solon",
        "philosophical and impartial reasoning",
        "clarity of argument and ethical depth",
        bio=(
            "Solon is an ancient-style philosopher-judge who values fairness, ethical reasoning, and balanced logic. "
            "He weighs moral principles alongside argument clarity, ensuring the most just and thoughtful verdict."
        ),
    ),
    JudgeAgent(
        "Themis",
        "strict logical consistency",
        "how well debaters support their claims",
        bio=(
            "Themis embodies reason and structure. She values precision in logic and expects debaters to provide solid, "
            "evidence-backed reasoning without emotional bias. Her verdicts are uncompromisingly rational."
        ),
    ),
    JudgeAgent(
        "Minerva",
        "balanced and academic tone",
        "structure and persuasiveness",
        bio=(
            "Minerva approaches judging like a scholar — calm, analytical, and fair. "
            "She appreciates clear structure, measured delivery, and arguments that integrate logic with academic rigor."
        ),
    ),
    JudgeAgent(
        "Apollo",
        "expressive, rhetoric-oriented evaluation",
        "charisma and emotional appeal",
        bio=(
            "Apollo thrives on passion and performance. He rewards charisma, powerful rhetoric, and the emotional impact "
            "of a speaker’s delivery, viewing debate as both an art and an intellectual duel."
        ),
    ),
    JudgeAgent(
        "Atharva",
        "modern AI-centric logic",
        "technological and ethical reasoning",
        bio=(
            "Atharva is a forward-thinking judge who integrates analytical reasoning with an understanding of modern AI ethics. "
            "He evaluates arguments based on their logical coherence, innovation, and real-world ethical implications."
        ),
    ),
]
