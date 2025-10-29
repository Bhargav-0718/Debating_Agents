import streamlit as st
import sys
import os
from textwrap import dedent

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.debate_agents import agent_pool
from agents.judge_agents import judge_pool
from crewai import Crew, Process, Task

st.set_page_config(page_title="AI Debate Simulator", page_icon="🎙️", layout="wide")
st.title("🎙️ AI Debate Simulator")

tab1, tab2 = st.tabs(["🧩 Debate Arena", "🧠 Agent Profiles"])

# ------------------------------------------------------------
# 🧩 TAB 1: DEBATE ARENA
# ------------------------------------------------------------
with tab1:
    st.markdown("""
    Welcome to the **AI Debate Arena** — where intelligent agents take the stage 
    to argue, refute, and persuade on any topic of your choice!
    """)

    # Sidebar Configuration
    st.sidebar.header("⚙️ Debate Configuration")
    debater1 = st.sidebar.selectbox("Select Debater 1", [a.name for a in agent_pool])
    debater2 = st.sidebar.selectbox("Select Debater 2", [a.name for a in agent_pool if a.name != debater1])

    stance1 = st.sidebar.radio(f"What stance should {debater1} take?", ["for", "against"])
    stance2 = "against" if stance1 == "for" else "for"

    judge_name = st.sidebar.selectbox("Select Judge", [j.name for j in judge_pool])
    topic = st.text_input("🧩 Enter the Debate Topic", placeholder="e.g., Should AI have legal rights?")

    start_button = st.button("🔥 Start Debate")

    if start_button:
        if not topic.strip():
            st.error("Please enter a debate topic before starting!")
            st.stop()

        debater1_obj = next(a for a in agent_pool if a.name == debater1)
        debater2_obj = next(a for a in agent_pool if a.name == debater2)
        judge_obj = next(j for j in judge_pool if j.name == judge_name)

        debater1_obj.assign_stance(stance1)
        debater2_obj.assign_stance(stance2)

        st.subheader("🎯 Debate Setup")
        st.write(f"**Topic:** {topic}")
        st.write(f"**{debater1_obj.name}** arguing **{stance1.upper()}** the motion.")
        st.write(f"**{debater2_obj.name}** arguing **{stance2.upper()}** the motion.")
        st.write(f"**Judge:** {judge_obj.name}")
        st.divider()

        # ---- Debate Transcript Collector ----
        debate_history = []

        def run_task(agent, prompt, context=""):
            """Run a CrewAI task for one agent."""
            task = Task(
                description=dedent(prompt),
                agent=agent.agent,
                expected_output="A logical and well-structured debate response."
            )
            crew = Crew(
                agents=[agent.agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )
            result = crew.kickoff(inputs={"context": context})
            return result

        with st.spinner("🧠 Generating Opening Statements..."):
            opening_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Give your opening statement (6-8 sentences) laying out your main reasoning.
            """
            opening_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Give your opening statement (6-8 sentences) with your counter stance.
            """

            arg_for = run_task(debater1_obj, opening_for_prompt)
            arg_against = run_task(debater2_obj, opening_against_prompt)
            debate_history.append(f"{debater1_obj.name} (FOR): {arg_for}")
            debate_history.append(f"{debater2_obj.name} (AGAINST): {arg_against}")

        st.markdown("### 🗣️ Opening Statements")
        st.markdown(f"**{debater1_obj.name} (FOR):** {arg_for}")
        st.markdown(f"**{debater2_obj.name} (AGAINST):** {arg_against}")
        st.divider()

        with st.spinner("🤺 Generating Rebuttals..."):
            rebuttal_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Your opponent said:\n{arg_against}
            Write your rebuttal in 4-6 sentences.
            """
            rebuttal_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Your opponent said:\n{arg_for}
            Write your rebuttal in 4-6 sentences.
            """

            rebuttal_for = run_task(debater1_obj, rebuttal_for_prompt)
            rebuttal_against = run_task(debater2_obj, rebuttal_against_prompt)
            debate_history.append(f"{debater1_obj.name} Rebuttal: {rebuttal_for}")
            debate_history.append(f"{debater2_obj.name} Rebuttal: {rebuttal_against}")

        st.markdown("### 🧩 Rebuttals")
        st.markdown(f"**{debater1_obj.name}:** {rebuttal_for}")
        st.markdown(f"**{debater2_obj.name}:** {rebuttal_against}")
        st.divider()

        with st.spinner("🎤 Generating Closing Arguments..."):
            closing_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Summarize your position in 5-7 sentences, based on the discussion so far:
            {debate_history}
            """
            closing_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Summarize your position in 5-7 sentences, based on the discussion so far:
            {debate_history}
            """

            closing_for = run_task(debater1_obj, closing_for_prompt)
            closing_against = run_task(debater2_obj, closing_against_prompt)
            debate_history.append(f"{debater1_obj.name} Closing: {closing_for}")
            debate_history.append(f"{debater2_obj.name} Closing: {closing_against}")

        st.markdown("### 🏁 Closing Statements")
        st.markdown(f"**{debater1_obj.name}:** {closing_for}")
        st.markdown(f"**{debater2_obj.name}:** {closing_against}")
        st.divider()

        with st.spinner("⚖️ Judge Deliberating..."):
            verdict_prompt = f"""
            You are {judge_obj.name}, known for your {judge_obj.judging_style}.
            Here's the full debate transcript:
            {debate_history}
            Objectively analyze both sides, choose a winner, and give a concise justification.
            """
            verdict = run_task(judge_obj, verdict_prompt)

        st.markdown("## 🏆 Final Verdict")
        st.success(f"**Judge {judge_obj.name}:** {verdict}")

# ------------------------------------------------------------
# 🧠 TAB 2: AGENT PROFILES
# ------------------------------------------------------------
with tab2:
    st.markdown("### Meet the AI Debaters and Judges 👇")
    subtab1, subtab2 = st.tabs(["🎙️ Debaters", "⚖️ Judges"])

    with subtab1:
        for agent in agent_pool:
            st.markdown(f"#### {agent.name}")
            st.write(f"**Personality:** {agent.personality}")
            st.write(f"**Specialty:** {getattr(agent, 'specialty', 'General Debate')}")
            st.write(f"**Description:** {getattr(agent, 'description', 'No bio available.')}")
            st.divider()

    with subtab2:
        for judge in judge_pool:
            st.markdown(f"#### {judge.name}")
            st.write(f"**Judging Style:** {judge.judging_style}")
            st.write(f"**Focus Criteria:** {getattr(judge, 'focus', 'Logical balance and evidence quality')}")
            st.write(f"**Description:** {getattr(judge, 'description', 'No bio available.')}")
            st.divider()
