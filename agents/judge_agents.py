from crewai import Agent
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory_system import debate_memory


class JudgeAgent:
    """Wrapper around CrewAI Agent to evaluate debates with unique judging personalities."""

    def __init__(self, name, judging_style, focus, bio, avatar_url=None):
        self.name = name
        self.judging_style = judging_style
        self.focus = focus
        self.bio = bio
        self.avatar_url = avatar_url or f"https://api.dicebear.com/7.x/bottts/svg?seed={name}"
        self.learning_context = ""
        # Create a minimal agent immediately to avoid heavy work at import time.
        # Learning-enhanced context will be injected later via prepare_for_judgment().
        self.agent = Agent(
            name=self.name,
            role="Debate Judge",
            goal="Evaluate debates and declare a winner fairly.",
            backstory=(
                f"You are {self.name}, a debate judge known for your {self.judging_style}. "
                f"You focus on {self.focus} when evaluating arguments."
            ),
        )
    
    def _update_agent(self):
        """Create or update the CrewAI agent with current learning context."""
        # Get learning context from memory
        self.learning_context = debate_memory.get_judge_learning_context(self.name)
        
        self.agent = Agent(
            name=self.name,
            role="Debate Judge",
            goal="Evaluate debates, rate debaters (1-5), and declare a winner objectively or according to your judging style.",
            backstory=(
                f"You are {self.name}, a debate judge known for your {self.judging_style}. "
                f"You focus on {self.focus} when evaluating arguments, maintaining integrity and insight in every decision.\n\n"
                f"JUDGING CONTEXT:\n{self.learning_context}\n\n"
                f"Use this information to maintain consistency and fairness in your evaluations."
            ),
        )
    
    def get_profile(self):
        """Get the judge's evaluation profile from memory."""
        return debate_memory.get_judge_profile(self.name)
    
    def get_judging_summary(self):
        """Get a summary of the judge's past judgments."""
        profile = self.get_profile()
        if not profile:
            return "No judging history yet."
        
        summary = f"**Judging Summary for {self.name}**\n\n"
        summary += f"- Total Judgments: {profile['total_judgments']}\n"
        summary += f"- Average Rating Given: {profile['average_rating_given']:.2f}/5\n"
        
        # Judging pattern
        patterns = profile['judging_patterns']
        total_judgments = sum(patterns.values())
        if total_judgments > 0:
            summary += f"\n**Judging Pattern:**\n"
            for pattern, count in patterns.items():
                percentage = (count / total_judgments) * 100
                summary += f"  - {pattern.capitalize()}: {percentage:.1f}%\n"
        
        # Rating distribution
        summary += f"\n**Rating Distribution:**\n"
        rd = profile['rating_distribution']
        # Support both legacy int keys and new string keys
        # Normalize view: iterate 5..1
        total_ratings = sum(int(v) for v in rd.values()) if rd else 0
        for rating in range(5, 0, -1):
            key_str = str(rating)
            count = rd.get(key_str, rd.get(rating, 0))
            percentage = (count / total_ratings * 100) if total_ratings > 0 else 0
            stars = "⭐" * rating
            summary += f"  {stars} ({rating}): {count} times ({percentage:.1f}%)\n"
        
        # Topics judged
        if profile['topics_judged']:
            summary += f"\n**Recent Topics Judged:** {', '.join(profile['topics_judged'][-5:])}\n"
        
        return summary
    
    def prepare_for_judgment(self):
        """Refresh learning context before judging a debate."""
        try:
            self._update_agent()
        except Exception as e:
            # Fallback gracefully if memory lookup or update fails
            print(f"Warning: JudgeAgent prepare_for_judgment fallback due to error: {e}")

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
