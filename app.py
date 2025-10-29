import streamlit as st
import sys
import os
from textwrap import dedent

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.debate_agents import agent_pool
from agents.judge_agents import judge_pool
from crewai import Crew, Process, Task

# ------------------------------------------------------------
# 🌐 Streamlit Setup
# ------------------------------------------------------------
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

    # Sidebar
    st.sidebar.header("⚙️ Debate Configuration")

    debater1 = st.sidebar.selectbox("Select Debater 1", [a.name for a in agent_pool])
    debater2 = st.sidebar.selectbox("Select Debater 2", [a.name for a in agent_pool if a.name != debater1])

    stance1 = st.sidebar.radio(f"What stance should {debater1} take?", ["for", "against"])
    stance2 = "against" if stance1 == "for" else "for"

    judge_name = st.sidebar.selectbox("Select Judge", [j.name for j in judge_pool])
    topic = st.text_input("🧩 Enter the Debate Topic", placeholder="e.g., Should AI have legal rights?")

    start_button = st.button("🔥 Start Debate")

    # ------------------------------------------------------------
    # Debate Logic
    # ------------------------------------------------------------
    if start_button:
        if not topic.strip():
            st.error("Please enter a debate topic before starting!")
            st.stop()

        # Retrieve selected agents
        debater1_obj = next(a for a in agent_pool if a.name == debater1)
        debater2_obj = next(a for a in agent_pool if a.name == debater2)
        judge_obj = next(j for j in judge_pool if j.name == judge_name)

        # Assign stances
        debater1_obj.assign_stance(stance1)
        debater2_obj.assign_stance(stance2)

        # Setup display
        st.subheader("🎯 Debate Setup")
        st.write(f"**Topic:** {topic}")
        st.write(f"**{debater1_obj.name}** arguing **{stance1.upper()}** the motion.")
        st.write(f"**{debater2_obj.name}** arguing **{stance2.upper()}** the motion.")
        st.write(f"**Judge:** {judge_obj.name}")
        st.divider()

        debate_history = []

        def run_task(agent, prompt, context=""):
            """Execute one debate round for an agent."""
            task = Task(
                description=dedent(prompt),
                agent=agent.agent,
                expected_output="A coherent, logically structured debate response."
            )
            crew = Crew(
                agents=[agent.agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )
            return crew.kickoff(inputs={"context": context})

        # ------------------ Opening Statements ------------------
        with st.spinner("🧠 Generating Opening Statements..."):
            opening_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Present your opening statement in 6–8 sentences, focusing on reasoning and clarity.
            """
            opening_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Present your opening statement in 6–8 sentences, focusing on reasoning and clarity.
            """

            arg_for = run_task(debater1_obj, opening_for_prompt)
            arg_against = run_task(debater2_obj, opening_against_prompt)
            debate_history.append(f"{debater1_obj.name} (FOR): {arg_for}")
            debate_history.append(f"{debater2_obj.name} (AGAINST): {arg_against}")

        st.markdown("### 🗣️ Opening Statements")
        st.markdown(f"**{debater1_obj.name} (FOR):** {arg_for}")
        st.markdown(f"**{debater2_obj.name} (AGAINST):** {arg_against}")
        st.divider()

        # ------------------ Rebuttals ------------------
        with st.spinner("🤺 Generating Rebuttals..."):
            rebuttal_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Your opponent said:\n\n{arg_against}\n\n
            Write your rebuttal in 5–6 sentences, addressing their key points directly.
            """
            rebuttal_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Your opponent said:\n\n{arg_for}\n\n
            Write your rebuttal in 5–6 sentences, addressing their key points directly.
            """

            rebuttal_for = run_task(debater1_obj, rebuttal_for_prompt)
            rebuttal_against = run_task(debater2_obj, rebuttal_against_prompt)
            debate_history.append(f"{debater1_obj.name} Rebuttal: {rebuttal_for}")
            debate_history.append(f"{debater2_obj.name} Rebuttal: {rebuttal_against}")

        st.markdown("### 🧩 Rebuttals")
        st.markdown(f"**{debater1_obj.name}:** {rebuttal_for}")
        st.markdown(f"**{debater2_obj.name}:** {rebuttal_against}")
        st.divider()

        # ------------------ Closing Statements ------------------
        with st.spinner("🎤 Generating Closing Statements..."):
            closing_for_prompt = f"""
            You are {debater1_obj.name}, arguing {stance1.upper()} the motion: "{topic}".
            Summarize your side in 5–7 sentences. Base your reasoning on all previous exchanges:
            {debate_history}
            """
            closing_against_prompt = f"""
            You are {debater2_obj.name}, arguing {stance2.upper()} the motion: "{topic}".
            Summarize your side in 5–7 sentences. Base your reasoning on all previous exchanges:
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

        # ------------------ Verdict ------------------
        with st.spinner("⚖️ Judge Deliberating..."):
            verdict_prompt = f"""
            You are {judge_obj.name}, a judge known for your {judge_obj.judging_style}.
            Focus on {judge_obj.focus}.
            Here is the complete debate transcript:
            {debate_history}
            Analyze both sides, decide the winner, and explain why in 2–3 paragraphs.
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

    # --- Debaters ---
    with subtab1:
        for agent in agent_pool:
            st.markdown(f"#### {agent.name}")
            st.write(f"**Personality:** {agent.personality}")
            st.write(f"**Expertise:** {agent.expertise}")
            st.write(f"**Bio:** {getattr(agent, 'bio', getattr(agent, 'description', 'No bio available.'))}")
            st.divider()

    # --- Judges ---
    with subtab2:
        for judge in judge_pool:
            st.markdown(f"#### {judge.name}")
            st.write(f"**Judging Style:** {judge.judging_style}")
            st.write(f"**Focus Criteria:** {judge.focus}")
            st.write(f"**Bio:** {getattr(judge, 'bio', getattr(judge, 'description', 'No bio available.'))}")
            st.divider()
