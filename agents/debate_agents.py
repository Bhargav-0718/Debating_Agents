from crewai import Agent

class DebateAgent:
    """Flexible wrapper around CrewAI Agent to allow stance assignment."""

    def __init__(self, name, personality, expertise):
        self.name = name
        self.personality = personality
        self.expertise = expertise
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
    DebateAgent("Athena", "calm, analytical reasoning", "philosophy, ethics, logic"),
    DebateAgent("Hermes", "witty, fast-talking rhetorical style", "politics and communication"),
    DebateAgent("Daedalus", "creative and strategic thinker", "science and rational analysis"),
    DebateAgent("Artemis", "sharp, emotionally intelligent speaker", "law, psychology, and social issues"),
    DebateAgent("Zephyr", "charismatic and passionate orator", "history and cultural debates")
]