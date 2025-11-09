"""
Persistent Memory System for Debate Agents
Stores debate history, scores, and learning data for both debaters and judges.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class DebateMemory:
    """Manages persistent storage of debate history and agent performance."""

    def __init__(self, storage_path: str = "debate_history.json"):
        self.storage_path = storage_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load existing debate history from JSON file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Normalize structure for compatibility across versions
                    self._normalize_data(data)
                    return data
            except (json.JSONDecodeError, IOError):
                return self._initialize_empty_data()
        return self._initialize_empty_data()

    def _initialize_empty_data(self) -> Dict:
        """Initialize empty data structure."""
        return {
            "debates": [],
            "debater_profiles": {},
            "judge_profiles": {}
        }

    def _save_data(self):
        """Save debate history to JSON file."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving debate history: {e}")

    def _normalize_data(self, data: Dict):
        """Ensure rating distribution keys are strings '1'..'5' and present.
        Also ensures stance performance keys exist for debaters.
        """
        try:
            # Judges
            judge_profiles = data.get("judge_profiles", {})
            for jname, prof in judge_profiles.items():
                rd = prof.get("rating_distribution", {})
                # Convert keys to strings and ensure 1..5
                new_rd = {str(k): int(v) for k, v in rd.items()}
                for k in ['1', '2', '3', '4', '5']:
                    new_rd.setdefault(k, 0)
                prof["rating_distribution"] = new_rd
                # Ensure judging_patterns exists
                prof.setdefault("judging_patterns", {"strict": 0, "moderate": 0, "lenient": 0})

            # Debaters
            deb_profiles = data.get("debater_profiles", {})
            for dname, prof in deb_profiles.items():
                sp = prof.get("stance_performance") or {}
                sp.setdefault("for", [])
                sp.setdefault("against", [])
                prof["stance_performance"] = sp
        except Exception as e:
            print(f"Warning: normalization error: {e}")

    def save_debate(self, topic: str, debater1_name: str, debater2_name: str,
                   debater1_stance: str, debater2_stance: str, judge_name: str,
                   debate_transcript: Dict, verdict: str, 
                   debater1_rating: int, debater2_rating: int,
                   debater1_feedback: str, debater2_feedback: str):
        """
        Save a complete debate record with ratings and feedback.
        
        Args:
            topic: The debate topic
            debater1_name: Name of first debater
            debater2_name: Name of second debater
            debater1_stance: Stance of first debater ('for' or 'against')
            debater2_stance: Stance of second debater
            judge_name: Name of the judge
            debate_transcript: Dict containing opening, rebuttal, closing statements
            verdict: Judge's final verdict
            debater1_rating: Rating for debater 1 (1-5)
            debater2_rating: Rating for debater 2 (1-5)
            debater1_feedback: Detailed feedback for debater 1
            debater2_feedback: Detailed feedback for debater 2
        """
        debate_record = {
            "id": len(self.data["debates"]) + 1,
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "participants": {
                "debater1": {
                    "name": debater1_name,
                    "stance": debater1_stance,
                    "rating": debater1_rating,
                    "feedback": debater1_feedback
                },
                "debater2": {
                    "name": debater2_name,
                    "stance": debater2_stance,
                    "rating": debater2_rating,
                    "feedback": debater2_feedback
                }
            },
            "judge": judge_name,
            "transcript": debate_transcript,
            "verdict": verdict
        }

        self.data["debates"].append(debate_record)
        
        # Update debater profiles
        self._update_debater_profile(debater1_name, debater1_rating, debater1_feedback, topic, debater1_stance)
        self._update_debater_profile(debater2_name, debater2_rating, debater2_feedback, topic, debater2_stance)
        
        # Update judge profile
        self._update_judge_profile(judge_name, topic, verdict, debater1_rating, debater2_rating)
        
        self._save_data()

    def _update_debater_profile(self, name: str, rating: int, feedback: str, topic: str, stance: str):
        """Update a debater's performance profile."""
        if name not in self.data["debater_profiles"]:
            self.data["debater_profiles"][name] = {
                "total_debates": 0,
                "average_rating": 0.0,
                "rating_history": [],
                "strengths": [],
                "weaknesses": [],
                "topics_debated": [],
                "stance_performance": {"for": [], "against": []}
            }

        profile = self.data["debater_profiles"][name]
        profile["total_debates"] += 1
        profile["rating_history"].append({
            "rating": rating,
            "topic": topic,
            "stance": stance,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update average rating
        all_ratings = [r["rating"] for r in profile["rating_history"]]
        profile["average_rating"] = sum(all_ratings) / len(all_ratings)
        
        # Track stance performance
        profile["stance_performance"][stance].append(rating)
        
        # Add topic to debated topics
        if topic not in profile["topics_debated"]:
            profile["topics_debated"].append(topic)
        
        # Extract strengths and weaknesses from feedback
        self._analyze_feedback(profile, feedback, rating)

    def _analyze_feedback(self, profile: Dict, feedback: str, rating: int):
        """Analyze feedback to identify strengths and weaknesses."""
        # Simple keyword-based analysis (can be enhanced with NLP)
        positive_keywords = ["strong", "excellent", "compelling", "persuasive", "effective", "well-structured", "logical", "convincing"]
        negative_keywords = ["weak", "lacking", "insufficient", "unclear", "unconvincing", "poor", "flawed", "missing"]
        
        feedback_lower = feedback.lower()
        
        if rating >= 4:
            for keyword in positive_keywords:
                if keyword in feedback_lower and keyword not in profile["strengths"]:
                    profile["strengths"].append(keyword)
                    if len(profile["strengths"]) > 10:  # Keep top 10
                        profile["strengths"].pop(0)
        
        if rating <= 2:
            for keyword in negative_keywords:
                if keyword in feedback_lower and keyword not in profile["weaknesses"]:
                    profile["weaknesses"].append(keyword)
                    if len(profile["weaknesses"]) > 10:  # Keep top 10
                        profile["weaknesses"].pop(0)

    def _update_judge_profile(self, name: str, topic: str, verdict: str, 
                             rating1: int, rating2: int):
        """Update a judge's evaluation profile."""
        if name not in self.data["judge_profiles"]:
            self.data["judge_profiles"][name] = {
                "total_judgments": 0,
                "average_rating_given": 0.0,
                # Use string keys for JSON stability
                "rating_distribution": {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0},
                "topics_judged": [],
                "verdict_history": [],
                "judging_patterns": {
                    "strict": 0,  # Avg rating < 2.5
                    "moderate": 0,  # Avg rating 2.5-3.5
                    "lenient": 0  # Avg rating > 3.5
                }
            }

        profile = self.data["judge_profiles"][name]
        profile["total_judgments"] += 1
        
        # Track rating distribution (string keys)
        rd = profile["rating_distribution"]
        r1k = str(max(1, min(5, int(rating1))))
        r2k = str(max(1, min(5, int(rating2))))
        rd[r1k] = rd.get(r1k, 0) + 1
        rd[r2k] = rd.get(r2k, 0) + 1
        
        # Calculate average rating given
        total_ratings = 0
        total_count = 0
        for rk, count in rd.items():
            try:
                total_ratings += int(rk) * int(count)
                total_count += int(count)
            except Exception:
                continue
        avg_rating = total_ratings / total_count if total_count > 0 else 0
        profile["average_rating_given"] = avg_rating
        
        # Track judging pattern
        if avg_rating < 2.5:
            profile["judging_patterns"]["strict"] += 1
        elif avg_rating <= 3.5:
            profile["judging_patterns"]["moderate"] += 1
        else:
            profile["judging_patterns"]["lenient"] += 1
        
        # Add topic to judged topics
        if topic not in profile["topics_judged"]:
            profile["topics_judged"].append(topic)
        
        # Store verdict for learning
        profile["verdict_history"].append({
            "topic": topic,
            "verdict": verdict,
            "ratings": [rating1, rating2],
            "timestamp": datetime.now().isoformat()
        })

    def get_debater_profile(self, name: str) -> Optional[Dict]:
        """Retrieve a debater's complete profile."""
        return self.data["debater_profiles"].get(name)

    def get_judge_profile(self, name: str) -> Optional[Dict]:
        """Retrieve a judge's complete profile."""
        return self.data["judge_profiles"].get(name)

    def get_debater_learning_context(self, name: str) -> str:
        """
        Generate a learning context string for a debater based on past performance.
        This will be used to help the debater improve.
        """
        profile = self.get_debater_profile(name)
        if not profile:
            return "This is your first debate. Give it your best effort!"

        context_parts = []
        
        # Overall performance
        context_parts.append(f"You have participated in {profile['total_debates']} debates with an average rating of {profile['average_rating']:.2f}/5.")
        
        # Recent performance trend
        if len(profile["rating_history"]) >= 3:
            recent_ratings = [r["rating"] for r in profile["rating_history"][-3:]]
            recent_avg = sum(recent_ratings) / len(recent_ratings)
            if recent_avg > profile["average_rating"]:
                context_parts.append("Your recent performance shows improvement! Keep it up.")
            elif recent_avg < profile["average_rating"]:
                context_parts.append("Your recent debates have been below your average. Focus on your core strengths.")
        
        # Strengths
        if profile["strengths"]:
            context_parts.append(f"Your identified strengths include: {', '.join(profile['strengths'][:5])}. Leverage these in your arguments.")
        
        # Weaknesses to address
        if profile["weaknesses"]:
            context_parts.append(f"Areas for improvement: {', '.join(profile['weaknesses'][:5])}. Work on addressing these points.")
        
        # Stance performance
        for_avg = sum(profile["stance_performance"]["for"]) / len(profile["stance_performance"]["for"]) if profile["stance_performance"]["for"] else 0
        against_avg = sum(profile["stance_performance"]["against"]) / len(profile["stance_performance"]["against"]) if profile["stance_performance"]["against"] else 0
        
        if for_avg > against_avg + 0.5:
            context_parts.append("You tend to perform better when arguing FOR a motion.")
        elif against_avg > for_avg + 0.5:
            context_parts.append("You tend to perform better when arguing AGAINST a motion.")
        
        # Recent feedback
        if profile["rating_history"]:
            last_feedback = profile["rating_history"][-1]["feedback"]
            context_parts.append(f"Most recent feedback: {last_feedback}")
        
        return "\n".join(context_parts)

    def get_judge_learning_context(self, name: str) -> str:
        """
        Generate a learning context string for a judge based on past judgments.
        This helps judges refine their evaluation criteria.
        """
        profile = self.get_judge_profile(name)
        if not profile:
            return "This is your first time judging. Apply your judging principles fairly and consistently."

        context_parts = []
        
        # Overall judging experience
        context_parts.append(f"You have judged {profile['total_judgments']} debates with an average rating of {profile['average_rating_given']:.2f}/5.")
        
        # Judging pattern
        patterns = profile["judging_patterns"]
        dominant_pattern = max(patterns, key=patterns.get)
        context_parts.append(f"Your judging style tends to be {dominant_pattern}.")
        
        # Rating distribution
        context_parts.append("Your rating distribution:")
        for rating in range(1, 6):
            count = profile["rating_distribution"][rating]
            percentage = (count / sum(profile["rating_distribution"].values()) * 100) if sum(profile["rating_distribution"].values()) > 0 else 0
            context_parts.append(f"  {rating} stars: {count} times ({percentage:.1f}%)")
        
        # Consistency advice
        total_verdicts = sum(profile["rating_distribution"].values())
        if total_verdicts >= 10:
            if profile["rating_distribution"][3] / total_verdicts < 0.3:
                context_parts.append("Consider using the full rating scale more consistently. The middle ratings (3) can be useful for average performances.")
        
        # Topics judged
        if len(profile["topics_judged"]) > 0:
            context_parts.append(f"Topics you've judged: {', '.join(profile['topics_judged'][-5:])}.")
        
        return "\n".join(context_parts)

    def get_all_debates(self) -> List[Dict]:
        """Retrieve all debate records."""
        return self.data["debates"]

    def get_debates_by_debater(self, debater_name: str) -> List[Dict]:
        """Get all debates involving a specific debater."""
        return [
            debate for debate in self.data["debates"]
            if debate["participants"]["debater1"]["name"] == debater_name
            or debate["participants"]["debater2"]["name"] == debater_name
        ]

    def get_debates_by_judge(self, judge_name: str) -> List[Dict]:
        """Get all debates judged by a specific judge."""
        return [
            debate for debate in self.data["debates"]
            if debate["judge"] == judge_name
        ]

    def get_statistics(self) -> Dict:
        """Get overall system statistics."""
        return {
            "total_debates": len(self.data["debates"]),
            "total_debaters": len(self.data["debater_profiles"]),
            "total_judges": len(self.data["judge_profiles"]),
            "average_debate_rating": self._calculate_average_debate_rating()
        }

    def _calculate_average_debate_rating(self) -> float:
        """Calculate the average rating across all debates."""
        if not self.data["debates"]:
            return 0.0
        
        total_ratings = 0
        count = 0
        for debate in self.data["debates"]:
            total_ratings += debate["participants"]["debater1"]["rating"]
            total_ratings += debate["participants"]["debater2"]["rating"]
            count += 2
        
        return total_ratings / count if count > 0 else 0.0


# Global memory instance
debate_memory = DebateMemory()
