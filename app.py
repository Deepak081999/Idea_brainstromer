import streamlit as st
from agents.idea_collector import IdeaCollectorAgent
from core.utils import check_similarity, save_idea


st.set_page_config(page_title="Idea Brainstormer", layout="wide")
st.title("💡 Multi-Agentic Idea Brainstorming Chatbot")
st.write("This chatbot helps you brainstorm and refine startup ideas using AI agents.")


idea_collector = IdeaCollectorAgent()


# --- Initialize session state ---
for key in ["matched_idea", "new_idea_data", "chat_mode", "chat_response"]:
    if key not in st.session_state:
        st.session_state[key] = None


# --- New Idea Submission Form ---
with st.form("idea_form"):
    idea_name = st.text_input("Idea Name")
    purpose = st.text_area("Purpose of the Idea")
    problem = st.text_area("What problem does this idea solve?")
    advantage = st.text_area("How is it better than existing solutions?")
    business_model = st.text_area("Business Model")
    features = st.text_area("Initial Features")
    scaling = st.text_area("How to scale this idea?")


    submitted = st.form_submit_button("Submit Idea")


if submitted:
    new_idea_data = {
    "name": idea_name,
    "purpose": purpose,
    "problem": problem,
    "advantage": advantage,
    "business_model": business_model,
    "features": features,
    "scaling": scaling,
    "description": " ".join([idea_name, purpose, problem, advantage, business_model, features, scaling])
    }
    st.session_state.new_idea_data = new_idea_data


    # Check similarity excluding self-match
    is_similar, matched_idea, score = check_similarity(new_idea_data)


    if is_similar:
        st.session_state.matched_idea = matched_idea
        st.session_state.chat_mode = "existing"
        st.info(f"We found a similar idea ({score}% match): {matched_idea['name']}. You can now chat with it interactively.")
    else:
        st.session_state.matched_idea = None
        st.session_state.chat_mode = "new"
        save_idea(new_idea_data)
        st.success("Your idea is new! You can now chat with AI to improve it.")


# --- Chat Form for both new and existing ideas ---
if st.session_state.chat_mode:
    with st.form("chat_form"):
        user_message = st.text_input("Type your message to AI:", key="chat_input")
        chat_submitted = st.form_submit_button("Send")


    if chat_submitted and user_message.strip() != "":
        if st.session_state.chat_mode == "existing":
            # Chat with matched idea
            response = idea_collector.advisor_agent.chat_with_existing_idea(
            st.session_state.matched_idea, user_message
            )
        else:
            # Chat with new idea (critique + suggestions)
            response = idea_collector.critique_agent.provide_feedback(
            st.session_state.new_idea_data, user_message
            )
        st.session_state.chat_response = response


    if st.session_state.chat_response:
        st.success(st.session_state.chat_response)