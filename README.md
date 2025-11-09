# 🎙️ AI Debate Simulator

## 🔗 Live Demo

[Open the deployed app](https://debatingagents-3kj8kjkisz8kfjezudstjv.streamlit.app/)

Access the running Streamlit instance to try debates instantly without local setup. Make sure to supply valid API keys in your own environment if you clone the repo; the hosted demo uses securely configured keys not included in the repository.

An intelligent debate system where AI agents engage in structured debates, learn from past performances, and continuously improve their argumentation skills.

## 🌟 Features

### Core Capabilities
- **AI-Powered Debates**: Multiple AI agents with unique personalities debate on any topic
- **Intelligent Judging**: AI judges evaluate debates based on specific criteria
- **Text-to-Speech**: Each agent has a unique voice with different accents (UK, AU, US, CA, IN)
- **AI-Generated Avatars**: Visual identity for each agent with portrait images
- **Chat-Style UI**: Conversation bubbles with manual audio playback controls
- **Persistent Memory**: All debates are saved with complete transcripts and ratings
- **Learning System**: Both debaters and judges learn from past performances
- **Performance Tracking**: Detailed statistics and analytics for all participants

### Rating System
Judges evaluate debaters using a comprehensive 5-criteria rubric:
- **Clarity**: Argument structure and presentation
- **Evidence**: Quality of supporting facts and examples
- **Logic**: Reasoning validity and consistency
- **Rhetoric**: Persuasiveness and engagement
- **Responsiveness**: Direct addressing of opponent's points

**Overall Ratings (1-5 scale):**
- ⭐ (1): Poor - Multiple major flaws
- ⭐⭐ (2): Below Average - Weak support or logical gaps
- ⭐⭐⭐ (3): Average - Competent mix of strengths and weaknesses
- ⭐⭐⭐⭐ (4): Good - Solid reasoning with minor issues
- ⭐⭐⭐⭐⭐ (5): Excellent - Compelling, precise, well-supported

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```powershell
git clone https://github.com/Bhargav-0718/Debating_Agents.git
cd Debating_Agents
```

2. **Install dependencies**
```powershell
pip install -r requirements.txt
```

**Required packages:**
- `streamlit` - Web interface
- `crewai` - AI agent framework
- `langchain` - LLM integration
- `openai` - OpenAI API access
- `python-dotenv` - Environment management
- `gtts` - Google Text-to-Speech for voice generation
- `pillow` - Image processing for avatars

3. **Set up environment variables**

Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
LANGCHAIN_API_KEY=your_langchain_key_here
LANGCHAIN_PROJECT=your_project_name
LANGCHAIN_TRACING_V2=true
```

4. **Run the application**
```powershell
streamlit run app.py
```

### First Debate

1. Navigate to the **Debate Arena** tab
2. Select two debaters (e.g., Athena vs. Hermes)
3. Choose their stances (for/against)
4. Pick a judge
5. Enter a debate topic
6. Click "Start Debate"

The system will:
- Generate opening statements
- Create rebuttals
- Deliver closing arguments
- Provide a judge's verdict with ratings
- Generate speech audio with unique voices per agent
- Display in chat bubbles with AI-generated avatars
- Save everything to memory for learning

## 🎙️ Voice & Visual Features

### Text-to-Speech System

Each agent has a distinct voice with region-specific accents:

**Debaters:**
- **Athena**: British English (UK) - Calm, analytical tone
- **Hermes**: Australian English (AU) - Energetic, witty delivery
- **Daedalus**: American English (US) - Strategic, measured speech
- **Artemis**: Canadian English (CA) - Empathetic, clear articulation
- **Zephyr**: Indian English (IN) - Charismatic, expressive style

**Judges:**
- **Solon**: British English (UK) - Authoritative, wise tone
- **Themis**: American English (US) - Precise, logical delivery
- **Minerva**: British English (UK) - Academic, balanced speech
- **Apollo**: Australian English (AU) - Expressive, engaging style
- **Atharva**: Indian English (IN) - Modern, analytical approach

**Audio Features:**
- Automatic speech generation for all debate text
- MP3 files cached in `audio_files/` directory
- Manual playback controls (no auto-play)
- Fast speech speed for efficient listening
- Unique voice per agent for easy identification

### AI-Generated Avatars

Visual identity powered by DiceBear API:
- **Debaters**: Avataaars style (cartoon portraits)
- **Judges**: Bottts style (robot avatars)
- Consistent avatar per agent across all debates
- Displayed in chat message bubbles

## 👥 Meet the Agents

### Debaters

**Athena** - Calm, analytical reasoning specialist
- Expertise: Philosophy, ethics, and logic
- Style: Composed and thoughtful with clear structure

**Hermes** - Witty, fast-talking rhetorical expert
- Expertise: Politics and communication
- Style: Sharp wit and persuasive energy

**Daedalus** - Creative and strategic thinker
- Expertise: Science and rational analysis
- Style: Innovative blend of logic and creativity

**Artemis** - Sharp, emotionally intelligent speaker
- Expertise: Law, psychology, and social issues
- Style: Passionate with psychological insight

**Zephyr** - Charismatic and passionate orator
- Expertise: History and cultural debates
- Style: Rich storytelling with emotional appeal

### Judges

**Solon** - Philosophical and impartial
- Focus: Clarity of argument and ethical depth
- Style: Values fairness and balanced logic

**Themis** - Strict logical consistency
- Focus: Evidence-backed reasoning
- Style: Uncompromisingly rational

**Minerva** - Balanced and academic
- Focus: Structure and persuasiveness
- Style: Calm, analytical, fair

**Apollo** - Expressive, rhetoric-oriented
- Focus: Charisma and emotional appeal
- Style: Values passion and performance

**Atharva** - Modern AI-centric logic
- Focus: Technological and ethical reasoning
- Style: Forward-thinking analytical approach

## 🧠 Learning System

### How Debaters Learn

**Before Each Debate:**
- System loads past performance data
- Generates learning context with:
  - Total debates and average rating
  - Recent performance trends
  - Identified strengths and weaknesses
  - Stance performance (FOR vs. AGAINST)
  - Recent feedback
- This context is injected into the AI's backstory

**After Each Debate:**
- Receive rating (1-5) and detailed feedback
- System analyzes feedback for patterns
- Updates strengths (from high ratings)
- Updates weaknesses (from low ratings)
- Tracks stance-specific performance
- All data saved for next debate

**Example Learning Progression:**
```
Debate 1: Rating 4/5 - "Strong logical reasoning"
    ↓ Learning Applied
Debate 2: Rating 5/5 - "Excellent! Leveraged strengths perfectly"
    ↓ Learning Applied
Debate 3: Rating 5/5 - "Consistent quality maintained"
```

### How Judges Learn

**Before Each Judgment:**
- Load judging history
- Review rating patterns (strict/moderate/lenient)
- Check rating distribution
- Ensure consistent use of scale

**After Each Judgment:**
- Track ratings given
- Update rating distribution
- Calculate judging pattern
- Identify consistency improvements

## 📊 User Interface

### 1. Debate Arena
- Configure debates with agent and topic selection
- Watch arguments unfold in real-time with chat bubbles
- Listen to each agent's unique voice with play buttons
- See AI-generated avatar portraits for visual identity
- View ratings and detailed feedback
- Winner declaration in final verdict

### 2. Agent Profiles
- View debater performance statistics
- Check rating history and trends
- See strengths and weaknesses
- Review judge statistics and patterns
- Agent-specific analytics

### 3. Debate History
- Browse all past debates
- Filter by debater or judge
- View complete transcripts
- See ratings and verdicts
- System-wide statistics dashboard
- Audio playback for historical debates (if cached)

## 💾 Data Storage

All data is stored in `debate_history.json`:

```json
{
  "debates": [...],           // Complete debate records
  "debater_profiles": {...},  // Performance tracking
  "judge_profiles": {...}     // Evaluation patterns
}
```

**Audio files** are cached separately in `audio_files/` directory:
- MP3 format with agent-specific voices
- Filename: `{AgentName}_{TextHash}.mp3`
- Automatically managed by TTS system
- Not tracked in git (excluded via .gitignore)

**Each debate record contains:**
- Unique ID and timestamp
- Topic and participants
- Complete transcript (opening, rebuttal, closing)
- Judge's verdict with winner declaration
- Ratings (1-5) for both debaters
- Detailed feedback per debater
- Metadata (stances, judge name)

**Backup & Reset:**
```powershell
# Create backup
Copy-Item debate_history.json debate_history_backup.json

# Restore from backup
Copy-Item debate_history_backup.json debate_history.json

# Reset system (delete history)
Remove-Item debate_history.json
```

## 🔧 Technical Architecture

```
User Interface (app.py)
        ↓
Debate Flow (core/debate_controller.py)
        ↓
Agents (agents/debate_agents.py, agents/judge_agents.py)
        ↓
Rating System (core/rating_system.py)
        ↓
TTS System (core/tts_system.py)
        ↓
Memory System (core/memory_system.py)
        ↓
Storage (debate_history.json + audio_files/)
```

### Key Components

**`core/tts_system.py`**
- Google Text-to-Speech integration
- Voice configuration per agent
- Audio file caching and management
- Accent/region-specific speech generation

**`core/memory_system.py`**
- Manages persistent storage
- Generates learning contexts
- Tracks statistics
- Profile management

**`core/rating_system.py`**
- Structured JSON rating prompts
- Multi-criteria evaluation
- Intelligent parsing
- Feedback generation

**`agents/debate_agents.py`**
- Debater agent classes
- Learning integration
- Profile access methods

**`agents/judge_agents.py`**
- Judge agent classes
- Rating consistency tracking
- Judging pattern analysis

**`app.py`**
- Streamlit UI with chat interface
- Debate orchestration
- TTS integration and audio playback
- Avatar display in chat bubbles
- Results display

## 📝 Usage Tips

1. **Run Multiple Debates**: The learning system improves with more data (5+ debates recommended)

2. **Mix Stances**: Have debaters argue both FOR and AGAINST topics for well-rounded development

3. **Vary Judges**: Different judges provide diverse feedback perspectives

4. **Review Profiles**: Check Agent Profiles regularly to track improvement

5. **Monitor Trends**: Use Debate History to see performance evolution

6. **Audio Controls**: Click play buttons to hear each argument - voices help distinguish agents

7. **Clear Cache**: Delete `audio_files/` folder to regenerate all speech (if voices sound corrupted)

## 🐛 Troubleshooting

**Issue**: Import errors on startup
- **Solution**: Ensure all dependencies installed: `pip install -r requirements.txt`

**Issue**: No debate history showing
- **Solution**: Run at least one complete debate first

**Issue**: Ratings not appearing
- **Solution**: Ensure debate completes fully through verdict stage

**Issue**: Audio not playing or errors generating speech
- **Solution**: 
  - Check `gtts` is installed: `pip install gtts`
  - Verify internet connection (gTTS requires online access)
  - Delete `audio_files/` folder and regenerate

**Issue**: Avatars not displaying
- **Solution**: Check internet connection (avatars load from DiceBear API)

**Issue**: Want to reset all data
- **Solution**: Delete `debate_history.json` (will regenerate on next debate)

**Issue**: Audio files taking up disk space
- **Solution**: Delete `audio_files/` folder - cached audio will regenerate as needed

## 📦 Dependencies

- `streamlit` - Web interface
- `crewai` - AI agent framework
- `langchain` - LLM integration
- `openai` - OpenAI API access
- `python-dotenv` - Environment management
- `gtts` - Google Text-to-Speech for voice generation
- `pillow` - Image processing for avatar display

**Note**: gTTS requires internet connection for speech generation.

## 🎯 System Statistics

After running debates, the system tracks:
- **Total Debates**: Count of all debates conducted
- **Active Debaters**: Number of debaters with history
- **Active Judges**: Number of judges who've evaluated
- **Average Rating**: System-wide mean rating

View these in the **Debate History** tab dashboard.

## 🔮 Future Enhancements

Potential additions:
- [ ] Advanced analytics with charts/graphs
- [ ] Export debates to PDF/CSV with audio
- [ ] Tournament mode with rankings
- [ ] Team debates (2v2)
- [ ] Multi-judge panels
- [ ] Per-criterion score display
- [ ] Machine learning predictions
- [ ] Head-to-head statistics
- [ ] Topic expertise tracking
- [ ] Audience voting integration
- [ ] Voice speed controls (requires different TTS engine)
- [ ] Downloadable audio files
- [ ] Real-time audio streaming during generation

## 📄 License

This project is part of the Debating_Agents repository.

## 🙏 Credits

Built with CrewAI and powered by OpenAI's language models.

---

**Current Version**: 2.1.0 (Memory, Learning & Voice System)  
**Last Updated**: November 9, 2025  
**Status**: Stable ✅

**New in v2.1.0:**
- 🎙️ Text-to-Speech with unique voices per agent
- 🖼️ AI-generated avatar portraits
- 💬 Chat-style conversation UI
- 🔊 Manual audio playback controls
- 🌍 Multi-accent support (UK, AU, US, CA, IN)

For issues or questions, check the Debate History tab or review the agent profiles for performance insights.

**Happy Debating! 🎙️⚖️**
