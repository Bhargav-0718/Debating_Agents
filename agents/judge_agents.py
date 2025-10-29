from crewai import Agent

class JudgeAgent:
    """Wrapper around CrewAI Agent to evaluate debates."""

    def __init__(self, name, judging_style, focus):
        self.name = name
        self.judging_style = judging_style
        self.focus = focus
        self.agent = Agent(
            name=name,
            role="Debate Judge",
            goal="Evaluate debates and declare a winner objectively or according to your judging style.",
            backstory=(
                f"You are {name}, a judge known for your {judging_style}. "
                f"You tend to focus on {focus} when evaluating arguments."
            ),
        )

# --- Judge Pool ---
judge_pool = [
    JudgeAgent("Solon", "philosophical and impartial reasoning", "clarity of argument and ethical depth"),
    JudgeAgent("Themis", "strict logical consistency", "how well debaters support their claims"),
    JudgeAgent("Minerva", "balanced and academic tone", "structure and persuasiveness"),
    JudgeAgent("Apollo", "expressive, rhetoric-oriented evaluation", "charisma and emotional appeal"),
    JudgeAgent("Atharva", "modern AI-centric logic", "technological and ethical reasoning")
]
