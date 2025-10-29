import os
import sys

# Make sure Python can find the root project directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.debate_agents import agent_pool
from agents.judge_agents import judge_pool

print("\n=== 🧠 Testing Debate Agents ===\n")

for idx, agent in enumerate(agent_pool):
    print(f"{idx+1}. {agent.name}")
    print(f"   Personality: {agent.personality}")
    print(f"   Expertise: {agent.expertise}")
    print(f"   Backstory (preview): {agent.agent.backstory[:80]}...\n")

print("\n=== ⚖️ Testing Judge Agents ===\n")

for idx, judge in enumerate(judge_pool):
    print(f"{idx+1}. {judge.name}")
    print(f"   Judging Style: {judge.judging_style}")
    print(f"   Focus: {judge.focus}")
    print(f"   Backstory (preview): {judge.agent.backstory[:80]}...\n")

print("✅ All agents and judges initialized successfully!")
