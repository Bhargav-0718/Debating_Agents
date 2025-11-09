import streamlit as st
import sys
import os
from textwrap import dedent

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.debate_agents import agent_pool
from agents.judge_agents import judge_pool
from core.memory_system import debate_memory
from core.rating_system import generate_detailed_ratings, display_rating_stars
from crewai import Crew, Process, Task

# ------------------------------------------------------------
# 🌐 Streamlit Setup
# ------------------------------------------------------------
st.set_page_config(page_title="AI Debate Simulator", page_icon="🎙️", layout="wide")
st.title("🎙️ AI Debate Simulator")

tab1, tab2, tab3 = st.tabs(["🧩 Debate Arena", "🧠 Agent Profiles", "📊 Debate History"])

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

        # Assign stances (this also updates learning context)
        debater1_obj.assign_stance(stance1)
        debater2_obj.assign_stance(stance2)
        
        # Prepare judge for judgment (updates learning context)
        judge_obj.prepare_for_judgment()

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
            debate_history.append(f"{debater1_obj.name} ({stance1.upper()}): {arg_for}")
            debate_history.append(f"{debater2_obj.name} ({stance2.upper()}): {arg_against}")

        st.markdown("### 🗣️ Opening Statements")
        st.markdown(f"**{debater1_obj.name} ({stance1.upper()}):** {arg_for}")
        st.markdown(f"**{debater2_obj.name} ({stance2.upper()}):** {arg_against}")
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
            
            IMPORTANT: End your verdict with a clear winner declaration on a new line in this exact format:
            "Winner: [Debater Name]"
            """
            verdict = run_task(judge_obj, verdict_prompt)

        st.markdown("## 🏆 Final Verdict")
        st.success(f"**Judge {judge_obj.name}:** {verdict}")
        st.divider()
        
        # ------------------ Ratings & Feedback ------------------
        with st.spinner("📊 Generating Ratings and Feedback..."):
            debate_transcript_str = "\n\n".join(debate_history)
            
            debater1_rating, debater2_rating, debater1_feedback, debater2_feedback = generate_detailed_ratings(
                judge_obj,
                debater1_obj.name,
                debater2_obj.name,
                stance1,
                stance2,
                debate_transcript_str,
                topic
            )
        
        st.markdown("## 📊 Performance Ratings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {debater1_obj.name}")
            st.markdown(f"**Rating:** {display_rating_stars(debater1_rating)} ({debater1_rating}/5)")
            st.info(f"**Feedback:** {debater1_feedback}")
        
        with col2:
            st.markdown(f"### {debater2_obj.name}")
            st.markdown(f"**Rating:** {display_rating_stars(debater2_rating)} ({debater2_rating}/5)")
            st.info(f"**Feedback:** {debater2_feedback}")
        
        # ------------------ Save to Memory ------------------
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
            debater1_name=debater1_obj.name,
            debater2_name=debater2_obj.name,
            debater1_stance=stance1,
            debater2_stance=stance2,
            judge_name=judge_obj.name,
            debate_transcript=debate_transcript_dict,
            verdict=str(verdict),  # Convert to string
            debater1_rating=debater1_rating,
            debater2_rating=debater2_rating,
            debater1_feedback=debater1_feedback,
            debater2_feedback=debater2_feedback
        )
        
        st.success("✅ Debate saved to memory! Agents will learn from this experience.")


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
            
            # Display performance stats
            with st.expander("📊 View Performance Statistics"):
                profile = agent.get_profile()
                if profile:
                    st.markdown(agent.get_rating_summary())
                else:
                    st.info("No debate history yet. This debater will improve with each debate!")
            
            st.divider()

    # --- Judges ---
    with subtab2:
        for judge in judge_pool:
            st.markdown(f"#### {judge.name}")
            st.write(f"**Judging Style:** {judge.judging_style}")
            st.write(f"**Focus Criteria:** {judge.focus}")
            st.write(f"**Bio:** {getattr(judge, 'bio', getattr(judge, 'description', 'No bio available.'))}")
            
            # Display judging stats
            with st.expander("📊 View Judging Statistics"):
                profile = judge.get_profile()
                if profile:
                    st.markdown(judge.get_judging_summary())
                else:
                    st.info("No judging history yet. This judge will refine their criteria with experience!")
            
            st.divider()

# ------------------------------------------------------------
# 📊 TAB 3: DEBATE HISTORY
# ------------------------------------------------------------
with tab3:
    st.markdown("### 📜 Complete Debate History")
    
    stats = debate_memory.get_statistics()
    
    # Display overall statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Debates", stats['total_debates'])
    with col2:
        st.metric("Active Debaters", stats['total_debaters'])
    with col3:
        st.metric("Active Judges", stats['total_judges'])
    with col4:
        st.metric("Avg Rating", f"{stats['average_debate_rating']:.2f}/5")
    
    st.divider()
    
    # Filter options
    all_debates = debate_memory.get_all_debates()
    
    if all_debates:
        filter_option = st.selectbox(
            "Filter debates by:",
            ["All Debates", "By Debater", "By Judge"]
        )
        
        filtered_debates = all_debates
        
        if filter_option == "By Debater":
            debater_names = list(set([d["participants"]["debater1"]["name"] for d in all_debates] + 
                                    [d["participants"]["debater2"]["name"] for d in all_debates]))
            selected_debater = st.selectbox("Select Debater", debater_names)
            filtered_debates = debate_memory.get_debates_by_debater(selected_debater)
        
        elif filter_option == "By Judge":
            judge_names = list(set([d["judge"] for d in all_debates]))
            selected_judge = st.selectbox("Select Judge", judge_names)
            filtered_debates = debate_memory.get_debates_by_judge(selected_judge)
        
        # Display debates in reverse chronological order
        for debate in reversed(filtered_debates):
            with st.expander(
                f"🎯 Debate #{debate['id']}: {debate['topic']} ({debate['timestamp'][:10]})"
            ):
                st.markdown(f"**Topic:** {debate['topic']}")
                st.markdown(f"**Date:** {debate['timestamp']}")
                st.markdown(f"**Judge:** {debate['judge']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    d1 = debate['participants']['debater1']
                    st.markdown(f"### {d1['name']} ({d1['stance'].upper()})")
                    st.markdown(f"**Rating:** {display_rating_stars(d1['rating'])} ({d1['rating']}/5)")
                    st.info(f"**Feedback:** {d1['feedback']}")
                
                with col2:
                    d2 = debate['participants']['debater2']
                    st.markdown(f"### {d2['name']} ({d2['stance'].upper()})")
                    st.markdown(f"**Rating:** {display_rating_stars(d2['rating'])} ({d2['rating']}/5)")
                    st.info(f"**Feedback:** {d2['feedback']}")
                
                st.markdown("---")
                st.markdown("**🏆 Verdict:**")
                st.success(debate['verdict'])
    else:
        st.info("No debates have been conducted yet. Start your first debate in the Debate Arena!")

