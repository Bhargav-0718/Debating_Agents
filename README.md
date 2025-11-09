# 🎙️ AI Debate Simulator

An intelligent debate system where AI agents engage in structured debates, learn from past performances, and continuously improve their argumentation skills.

## 🌟 Features

### Core Capabilities
- **AI-Powered Debates**: Multiple AI agents with unique personalities debate on any topic
- **Intelligent Judging**: AI judges evaluate debates based on specific criteria
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
- Save everything to memory for learning

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
- Configure debates
- Watch arguments unfold in real-time
- See ratings and feedback
- Winner declaration

### 2. Agent Profiles
- View debater performance statistics
- Check rating history and trends
- See strengths and weaknesses
- Review judge statistics and patterns

### 3. Debate History
- Browse all past debates
- Filter by debater or judge
- View complete transcripts
- See ratings and verdicts
- System-wide statistics dashboard

## 💾 Data Storage

All data is stored in `debate_history.json`:

```json
{
  "debates": [...],           // Complete debate records
  "debater_profiles": {...},  // Performance tracking
  "judge_profiles": {...}     // Evaluation patterns
}
```

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
Memory System (core/memory_system.py)
        ↓
Storage (debate_history.json)
```

### Key Components

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
- Streamlit UI
- Debate orchestration
- Results display

## 📝 Usage Tips

1. **Run Multiple Debates**: The learning system improves with more data (5+ debates recommended)

2. **Mix Stances**: Have debaters argue both FOR and AGAINST topics for well-rounded development

3. **Vary Judges**: Different judges provide diverse feedback perspectives

4. **Review Profiles**: Check Agent Profiles regularly to track improvement

5. **Monitor Trends**: Use Debate History to see performance evolution

## 🐛 Troubleshooting

**Issue**: Import errors on startup
- **Solution**: Ensure all dependencies installed: `pip install -r requirements.txt`

**Issue**: No debate history showing
- **Solution**: Run at least one complete debate first

**Issue**: Ratings not appearing
- **Solution**: Ensure debate completes fully through verdict stage

**Issue**: Want to reset all data
- **Solution**: Delete `debate_history.json` (will regenerate on next debate)

## 📦 Dependencies

- `streamlit` - Web interface
- `crewai` - AI agent framework
- `langchain` - LLM integration
- `openai` - OpenAI API access
- `python-dotenv` - Environment management

No additional dependencies required for the memory/learning system!

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
- [ ] Export debates to PDF/CSV
- [ ] Tournament mode with rankings
- [ ] Team debates (2v2)
- [ ] Multi-judge panels
- [ ] Per-criterion score display
- [ ] Machine learning predictions
- [ ] Head-to-head statistics
- [ ] Topic expertise tracking
- [ ] Audience voting integration

## 📄 License

This project is part of the Debating_Agents repository.

## 🙏 Credits

Built with CrewAI and powered by OpenAI's language models.

---

**Current Version**: 2.0.0 (Memory & Learning System)  
**Last Updated**: November 9, 2025  
**Status**: Stable ✅

For issues or questions, check the Debate History tab or review the agent profiles for performance insights.

**Happy Debating! 🎙️⚖️**
