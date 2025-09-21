import streamlit as st
import time
import fitz  # PyMuPDF
import plotly.graph_objects as go
from main import (
    analyze_clause,
    analyze_image_clause
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Law4You - AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

# Start a new chat on the first run of the session
if not st.session_state.current_chat_id:
    chat_id = f"chat_{int(time.time())}"
    st.session_state.current_chat_id = chat_id
    st.session_state.chat_sessions[chat_id] = {
        "history": [],
        "analysis": None,
        "name": "New Chat"
    }

# --- HELPER FUNCTIONS ---
def new_chat():
    """Creates a new, empty chat session and sets it as the current one."""
    chat_id = f"chat_{int(time.time())}"
    st.session_state.current_chat_id = chat_id
    st.session_state.chat_sessions[chat_id] = {"history": [], "analysis": None, "name": "New Chat"}

def get_current_chat():
    """Gets the data for the currently active chat session."""
    return st.session_state.chat_sessions.get(st.session_state.current_chat_id)

def extract_text_from_pdf(pdf_file):
    """Safely extracts text from an uploaded PDF file."""
    try:
        pdf_file.seek(0)
        return "".join(page.get_text() for page in fitz.open(stream=pdf_file.read(), filetype="pdf"))
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

# --- CORE LOGIC & CALLBACKS ---
def handle_user_input(input_type, data):
    """Processes all user inputs, triggers analysis, and updates the session state."""
    current_chat = get_current_chat()
    if not current_chat:
        st.error("No active chat session. Please start a new chat.")
        return

    input_content, user_prompt = None, ""

    if input_type == "pdf":
        input_content = extract_text_from_pdf(data)
        user_prompt = f"📄 Analyzed PDF: {data.name}"
    elif input_type == "image":
        input_content = data
        user_prompt = f"🖼️ Analyzed Image: {data.name}"
    elif input_type == "text":
        input_content = data
        user_prompt = data

    if not user_prompt or (input_type != "text" and not input_content):
        st.warning("Could not process input. Please try again.")
        return

    if not current_chat["history"]:
        current_chat["name"] = user_prompt[:35] + "..." if len(user_prompt) > 35 else user_prompt
    
    current_chat["history"].append({"role": "user", "content": user_prompt})
    
    with st.spinner("AI is analyzing the document..."):
        if input_type == "image":
            analysis_result = analyze_image_clause(input_content)
        else:
            analysis_result = analyze_clause(input_content)

    if "error" in analysis_result:
        ai_response = f"An error occurred during analysis: {analysis_result['error']}"
    else:
        ai_response = "Analysis complete. See the dashboard for your detailed report."

    current_chat["analysis"] = analysis_result
    current_chat["history"].append({"role": "assistant", "content": ai_response})

def process_uploaded_file(input_type, file_key):
    """Callback to handle file uploads and prevent reprocessing."""
    uploaded_file = st.session_state.get(file_key)
    if uploaded_file:
        handle_user_input(input_type, uploaded_file)

# --- UI RENDERING ---
# --- SIDEBAR ---
with st.sidebar:
    st.header("Law4You")
    if st.button("➕ New Chat", use_container_width=True):
        new_chat()
        st.rerun()
    st.divider()
    
    for chat_id in reversed(list(st.session_state.chat_sessions.keys())):
        is_current = chat_id == st.session_state.current_chat_id
        chat_name = st.session_state.chat_sessions[chat_id]["name"]
        if st.button(chat_name, use_container_width=True, type="primary" if is_current else "secondary"):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- MAIN PAGE LAYOUT ---
current_chat = get_current_chat()
if not current_chat:
    st.error("Something went wrong. Please start a new chat from the sidebar.")
    st.stop()

col1, col2, col3 = st.columns([0.35, 0.35, 0.3])

with col1:
    st.header("Chat & Analysis")
    for msg in current_chat["history"]:
        with st.chat_message(name=msg["role"], avatar="🧑‍⚖️" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Analyze your legal text..."):
        handle_user_input("text", prompt)

    with st.popover("📤 Upload Document", use_container_width=True):
        pdf_key = f"pdf_{st.session_state.current_chat_id}"
        st.file_uploader(
            "📄 Upload PDF", type=['pdf'], key=pdf_key,
            on_change=process_uploaded_file, args=("pdf", pdf_key)
        )
        
        img_key = f"img_{st.session_state.current_chat_id}"
        st.file_uploader(
            "🖼️ Upload Image", type=['png', 'jpg', 'jpeg'], key=img_key,
            on_change=process_uploaded_file, args=("image", img_key)
        )

# --- COLUMN 2 & 3: Analysis Dashboard ---
analysis = current_chat.get("analysis")

with col2:
    st.header("Analysis Dashboard")
    if not analysis:
        st.info("Your analysis results will appear here after you submit a document.")
    elif "error" in analysis:
        st.error(f"Analysis Failed: {analysis['error']}")
    else:
        with st.container(border=True):
            st.success("**Plain English Summary**")
            st.write(analysis.get("simplified_text", "Not available."))
        
        with st.container(border=True):
            st.info("**Jargon Buster: Key Terms**")
            for item in analysis.get("jargon_definitions", []):
                st.markdown(f"**{item.get('term', 'N/A')}:** {item.get('definition', 'N/A')}")

with col3:
    st.header("Risk & Questions")
    if analysis and "error" not in analysis:
        with st.container(border=True):
            risk_score = analysis.get("risk_score", 0)
            bar_color = "#D9534F" # Red
            if risk_score <= 4: bar_color = '#63B76C' # Green
            elif risk_score <= 7: bar_color = '#FFC107' # Yellow

            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=risk_score,
                title={'text': "Potential Risk Level"},
                gauge={
                    'axis': {'range': [0, 10], 'tickwidth': 1},
                    'bar': {'color': bar_color},
                    'steps': [
                        {'range': [0, 4], 'color': '#3a593e'},
                        {'range': [4, 7], 'color': '#755d0a'},
                        {'range': [7, 10], 'color': '#6e2b29'}],
                }))
            fig.update_layout(height=200, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.warning("**Questions for Your Lawyer**")
            questions = analysis.get("questions_for_lawyer", [])
            if questions:
                for q in questions:
                    st.markdown(f"- *{q}*")
            else:
                st.write("No specific questions were generated.")
    else:
        st.info("Risk metrics and questions for your lawyer will appear here.")
