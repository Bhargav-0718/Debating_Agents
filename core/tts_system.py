"""
Text-to-Speech System for Debate Agents
Generates audio files using gTTS for agent speeches.
"""

import os
from gtts import gTTS
from pathlib import Path
import hashlib


class TTSManager:
    """Manages text-to-speech generation and audio file caching."""
    
    def __init__(self, audio_dir: str = "audio_files"):
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(exist_ok=True)
        
        # Voice configurations for different agent personalities
        # gTTS supports different accents/languages
        self.voice_configs = {
            # Debaters
            "Athena": {"lang": "en", "tld": "co.uk", "slow": False},      # British - calm, analytical
            "Hermes": {"lang": "en", "tld": "com.au", "slow": False},     # Australian - witty, energetic
            "Daedalus": {"lang": "en", "tld": "com", "slow": False},      # American - strategic
            "Artemis": {"lang": "en", "tld": "ca", "slow": False},        # Canadian - empathetic
            "Zephyr": {"lang": "en", "tld": "co.in", "slow": False},      # Indian - charismatic
            
            # Judges
            "Solon": {"lang": "en", "tld": "co.uk", "slow": False},       # British - wise
            "Themis": {"lang": "en", "tld": "com", "slow": False},        # American - precise
            "Minerva": {"lang": "en", "tld": "co.uk", "slow": False},     # British - academic
            "Apollo": {"lang": "en", "tld": "com.au", "slow": False},     # Australian - expressive
            "Atharva": {"lang": "en", "tld": "co.in", "slow": False},     # Indian - modern
        }
    
    def _generate_audio_filename(self, agent_name: str, text: str) -> str:
        """Generate a unique filename based on agent and text content."""
        # Create hash of text for unique identification
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        filename = f"{agent_name}_{text_hash}.mp3"
        return str(self.audio_dir / filename)
    
    def generate_speech(self, agent_name: str, text: str) -> str:
        """
        Generate speech audio for the given text.
        
        Args:
            agent_name: Name of the agent speaking
            text: Text to convert to speech
            
        Returns:
            Path to the generated audio file
        """
        # Check cache first
        audio_path = self._generate_audio_filename(agent_name, text)
        
        if os.path.exists(audio_path):
            # Audio already generated, return cached version
            return audio_path
        
        # Get voice configuration for this agent
        voice_config = self.voice_configs.get(
            agent_name, 
            {"lang": "en", "tld": "com", "slow": False}  # Default
        )
        
        try:
            # Generate speech
            tts = gTTS(
                text=text,
                lang=voice_config["lang"],
                tld=voice_config["tld"],
                slow=voice_config["slow"]
            )
            
            # Save to file
            tts.save(audio_path)
            return audio_path
            
        except Exception as e:
            print(f"Error generating speech for {agent_name}: {e}")
            return None
    
    def generate_debate_audio(self, debate_data: dict) -> dict:
        """
        Generate audio files for all parts of a debate.
        
        Args:
            debate_data: Dictionary containing debate transcript
            
        Returns:
            Dictionary mapping segment IDs to audio file paths
        """
        audio_files = {}
        
        # Generate audio for each debate segment
        segments = [
            ("opening_debater1", debate_data.get("debater1_name"), debate_data.get("opening_for")),
            ("opening_debater2", debate_data.get("debater2_name"), debate_data.get("opening_against")),
            ("rebuttal_debater1", debate_data.get("debater1_name"), debate_data.get("rebuttal_for")),
            ("rebuttal_debater2", debate_data.get("debater2_name"), debate_data.get("rebuttal_against")),
            ("closing_debater1", debate_data.get("debater1_name"), debate_data.get("closing_for")),
            ("closing_debater2", debate_data.get("debater2_name"), debate_data.get("closing_against")),
            ("verdict", debate_data.get("judge_name"), debate_data.get("verdict")),
        ]
        
        for segment_id, agent_name, text in segments:
            if agent_name and text:
                # Convert text to string if it's a CrewOutput object
                text_str = str(text)
                audio_path = self.generate_speech(agent_name, text_str)
                if audio_path:
                    audio_files[segment_id] = audio_path
        
        return audio_files
    
    def cleanup_old_audio(self, keep_recent: int = 50):
        """
        Clean up old audio files to save disk space.
        
        Args:
            keep_recent: Number of most recent files to keep
        """
        try:
            audio_files = sorted(
                self.audio_dir.glob("*.mp3"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Delete old files beyond keep_recent
            for old_file in audio_files[keep_recent:]:
                old_file.unlink()
                
        except Exception as e:
            print(f"Error cleaning up audio files: {e}")


# Global TTS manager instance
tts_manager = TTSManager()
