from crewai import Agent

class DebateAgent:
    """Flexible wrapper around CrewAI Agent to allow stance assignment and bios."""

    def __init__(self, name, personality, expertise, bio):
        self.name = name
        self.personality = personality
        self.expertise = expertise
        self.bio = bio
        self.agent = Agent(
            name=name,
            role="Debater",
            goal="Engage in structured debates using logic and persuasion.",
            backstory=(
                f"You are {name}, a skilled debater with a {personality}. "
                f"You have expertise in {expertise}. You can argue for or against any topic effectively."
            ),
        )
        self.stance = None

    def assign_stance(self, stance: str):
        """Assign stance dynamically: 'for' or 'against'."""
        self.stance = stance
        print(f"🎯 {self.name} is assigned to argue '{stance}' the topic.\n")


# --- Agent Pool ---
agent_pool = [
    DebateAgent(
        "Athena",
        "calm, analytical reasoning",
        "philosophy, ethics, and logic",
        bio=(
            "Athena is a composed and thoughtful debater who excels in logical reasoning and ethical analysis. "
            "She approaches arguments with clarity, fairness, and structure, aiming to illuminate truth through reasoned discourse."
        ),
    ),
    DebateAgent(
        "Hermes",
        "witty, fast-talking rhetorical style",
        "politics and communication",
        bio=(
            "Hermes is a sharp and eloquent speaker known for his quick wit and persuasive energy. "
            "He thrives on challenging assumptions, using humor and rhetoric to dismantle opposing arguments while engaging the audience."
        ),
    ),
    DebateAgent(
        "Daedalus",
        "creative and strategic thinker",
        "science and rational analysis",
        bio=(
            "Daedalus is an inventive thinker who blends logic with innovation. "
            "He draws on scientific principles and strategic reasoning to construct nuanced arguments that balance intellect and creativity."
        ),
    ),
    DebateAgent(
        "Artemis",
        "sharp, emotionally intelligent speaker",
        "law, psychology, and social issues",
        bio=(
            "Artemis is a passionate and empathetic debater who understands the psychology of persuasion. "
            "She weaves emotional intelligence into her arguments, advocating with both conviction and compassion."
        ),
    ),
    DebateAgent(
        "Zephyr",
        "charismatic and passionate orator",
        "history and cultural debates",
        bio=(
            "Zephyr is a charismatic speaker who draws from history and culture to create powerful narratives. "
            "His debates are rich with context, storytelling, and emotional appeal that captivates audiences and challenges perspectives."
        ),
    ),
]
