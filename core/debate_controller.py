import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from crewai import Agent, Task, Crew, Process
from textwrap import dedent
from agents.debate_agents import agent_pool
from agents.judge_agents import judge_pool
from core.memory_system import debate_memory
from core.rating_system import generate_detailed_ratings


# --- Helper Function ---
def run_task(agent, prompt, context=""):
    """Run a single debate round for an agent."""
    task = Task(
        description=dedent(prompt),
        agent=agent.agent,
        expected_output="A detailed and logically sound debate response."
    )
    crew = Crew(
        agents=[agent.agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False
    )
    result = crew.kickoff(inputs={"context": context})
    return result


# --- Streamlit / Programmatic Debate Runner ---
def run_debate(debater1_name, debater2_name, stance1, judge_name, topic):
    """Non-interactive debate runner with memory integration."""
    print("\n🎙️ === AI Debate Simulator (Streamlit Mode) ===\n")

    debater1 = next(a for a in agent_pool if a.name == debater1_name)
    debater2 = next(a for a in agent_pool if a.name == debater2_name)
    judge = next(j for j in judge_pool if j.name == judge_name)

    # Assign stances (this updates learning context)
    debater1.assign_stance(stance1)
    debater2.assign_stance("against" if stance1 == "for" else "for")
    
    # Prepare judge for judgment
    judge.prepare_for_judgment()

    debate_history = []

    # Round 1: Openings
    opening_for_prompt = f"""
    You are {debater1.name}. You are arguing {debater1.stance.upper()} the motion: "{topic}".
    Present your opening statement in 6-8 sentences, establishing your core reasoning.
    """
    opening_against_prompt = f"""
    You are {debater2.name}. You are arguing {debater2.stance.upper()} the motion: "{topic}".
    Present your opening statement in 6-8 sentences, presenting your stance clearly.
    """

    arg_for = run_task(debater1, opening_for_prompt)
    arg_against = run_task(debater2, opening_against_prompt)
    debate_history.append(f"{debater1.name} (FOR): {arg_for}")
    debate_history.append(f"{debater2.name} (AGAINST): {arg_against}")

    # Round 2: Rebuttals
    rebuttal_for_prompt = f"""
    You are {debater1.name}. You are arguing {debater1.stance.upper()} the motion: "{topic}".
    Your opponent said:\n{arg_against}
    Write a rebuttal in 5-6 sentences.
    """
    rebuttal_against_prompt = f"""
    You are {debater2.name}. You are arguing {debater2.stance.upper()} the motion: "{topic}".
    Your opponent said:\n{arg_for}
    Write a rebuttal in 5-6 sentences.
    """

    rebuttal_for = run_task(debater1, rebuttal_for_prompt)
    rebuttal_against = run_task(debater2, rebuttal_against_prompt)
    debate_history.append(f"{debater1.name} Rebuttal: {rebuttal_for}")
    debate_history.append(f"{debater2.name} Rebuttal: {rebuttal_against}")

    # Round 3: Closings
    closing_for_prompt = f"""
    You are {debater1.name}. Closing argument for "{topic}".
    Summarize your position in 5-7 sentences. Debate so far:\n{debate_history}
    """
    closing_against_prompt = f"""
    You are {debater2.name}. Closing argument for "{topic}".
    Summarize your position in 5-7 sentences. Debate so far:\n{debate_history}
    """

    closing_for = run_task(debater1, closing_for_prompt)
    closing_against = run_task(debater2, closing_against_prompt)
    debate_history.append(f"{debater1.name} Closing: {closing_for}")
    debate_history.append(f"{debater2.name} Closing: {closing_against}")

    # Verdict
    verdict_prompt = f"""
    You are {judge.name}, the judge known for {judge.judging_style}.
    Focus on {judge.focus}.
    Debate Transcript:
    {debate_history}
    Decide the winner objectively and provide reasoning in 2-3 paragraphs.
    
    IMPORTANT: End your verdict with a clear winner declaration on a new line in this exact format:
    "Winner: [Debater Name]"
    """

    verdict = run_task(judge, verdict_prompt)
    
    # Generate ratings
    debate_transcript_str = "\n\n".join(debate_history)
    debater1_rating, debater2_rating, debater1_feedback, debater2_feedback = generate_detailed_ratings(
        judge,
        debater1.name,
        debater2.name,
        debater1.stance,
        debater2.stance,
        debate_transcript_str,
        topic
    )
    
    # Save to memory
    # Convert CrewOutput objects to strings for JSON serialization
    debate_transcript_dict = {
        "opening_for": str(arg_for),
        "opening_against": str(arg_against),
        "rebuttal_for": str(rebuttal_for),
        "rebuttal_against": str(rebuttal_against),
        "closing_for": str(closing_for),
        "closing_against": str(closing_against)
    }
    
    debate_memory.save_debate(
        topic=topic,
        debater1_name=debater1.name,
        debater2_name=debater2.name,
        debater1_stance=debater1.stance,
        debater2_stance=debater2.stance,
        judge_name=judge.name,
        debate_transcript=debate_transcript_dict,
        verdict=str(verdict),  # Convert to string
        debater1_rating=debater1_rating,
        debater2_rating=debater2_rating,
        debater1_feedback=debater1_feedback,
        debater2_feedback=debater2_feedback
    )

    return f"""
    🧠 Topic: {topic}

    {debater1.name} ({debater1.stance}): {arg_for}

    {debater2.name} ({debater2.stance}): {arg_against}

    {debater1.name} Rebuttal: {rebuttal_for}

    {debater2.name} Rebuttal: {rebuttal_against}

    {debater1.name} Closing: {closing_for}

    {debater2.name} Closing: {closing_against}

    🏆 Verdict by {judge.name}:
    {verdict}
    
    📊 Ratings:
    {debater1.name}: {debater1_rating}/5 - {debater1_feedback}
    {debater2.name}: {debater2_rating}/5 - {debater2_feedback}
    """


