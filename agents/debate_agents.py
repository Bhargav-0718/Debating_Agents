from crewai import Agent
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_system import debate_memory


class DebateAgent:
    """Flexible wrapper around CrewAI Agent to allow stance assignment and bios."""

    def __init__(self, name, personality, expertise, bio, avatar_url=None):
        self.name = name
        self.personality = personality
        self.expertise = expertise
        self.bio = bio
        self.avatar_url = avatar_url or f"https://api.dicebear.com/7.x/avataaars/svg?seed={name}"
        self.stance = None
        self.learning_context = ""
        
        # Create a minimal agent immediately; we'll inject learning context
        # right before the debate when stance is assigned.
        self.agent = Agent(
            name=self.name,
            role="Debater",
            goal="Engage in structured debates using logic and persuasion.",
            backstory=(
                f"You are {self.name}, a skilled debater with a {self.personality}. "
                f"You have expertise in {self.expertise}. You can argue for or against any topic effectively."
            ),
        )

    def _update_agent(self):
        """Create or update the CrewAI agent with current learning context."""
        # Get learning context from memory
        self.learning_context = debate_memory.get_debater_learning_context(self.name)
        
        # Create agent with enhanced backstory including learning context
        self.agent = Agent(
            name=self.name,
            role="Debater",
            goal="Engage in structured debates using logic and persuasion, continuously improving based on past performance.",
            backstory=(
                f"You are {self.name}, a skilled debater with a {self.personality}. "
                f"You have expertise in {self.expertise}. You can argue for or against any topic effectively.\n\n"
                f"PERFORMANCE CONTEXT:\n{self.learning_context}\n\n"
                f"Use this information to refine your debating strategy and address any weaknesses identified in previous debates."
            ),
        )

    def assign_stance(self, stance: str):
        """Assign stance dynamically: 'for' or 'against'."""
        self.stance = stance
        # Refresh learning context when stance is assigned (before debate starts)
        self._update_agent()
        print(f"🎯 {self.name} is assigned to argue '{stance}' the topic.\n")
    
    def get_profile(self):
        """Get the debater's performance profile from memory."""
        return debate_memory.get_debater_profile(self.name)
    
    def get_rating_summary(self):
        """Get a summary of the debater's ratings."""
        profile = self.get_profile()
        if not profile:
            return "No debate history yet."
        
        summary = f"**Performance Summary for {self.name}**\n\n"
        summary += f"- Total Debates: {profile['total_debates']}\n"
        summary += f"- Average Rating: {profile['average_rating']:.2f}/5 ⭐\n"
        
        if profile['rating_history']:
            summary += f"\n**Recent Ratings (last 5):**\n"
            for record in profile['rating_history'][-5:]:
                summary += f"  - {record['rating']}/5 on topic: '{record['topic']}' ({record['stance']})\n"
        
        if profile['strengths']:
            summary += f"\n**Strengths:** {', '.join(profile['strengths'][:5])}\n"
        
        if profile['weaknesses']:
            summary += f"\n**Areas for Improvement:** {', '.join(profile['weaknesses'][:5])}\n"
        
        # Stance performance
        for_ratings = profile['stance_performance']['for']
        against_ratings = profile['stance_performance']['against']
        
        if for_ratings:
            for_avg = sum(for_ratings) / len(for_ratings)
            summary += f"\n**For Arguments:** Average {for_avg:.2f}/5 ({len(for_ratings)} debates)\n"
        
        if against_ratings:
            against_avg = sum(against_ratings) / len(against_ratings)
            summary += f"**Against Arguments:** Average {against_avg:.2f}/5 ({len(against_ratings)} debates)\n"
        
        return summary


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
