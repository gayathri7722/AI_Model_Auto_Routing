
import os
import streamlit as st
import requests
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Gayathri's AI Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "api_status" not in st.session_state:
    st.session_state.api_status = None

# --------------------------------------------------
# CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #F5F1E7;
    color: #173D32;
}

[data-testid="stSidebar"] {
    background-color: #173D32;
}

[data-testid="stSidebar"] * {
    color: #F5F1E7 !important;
}

.main-title {
    color: #173D32;
    font-size: 38px;
    font-weight: 800;
    text-align: center;
}

.subtitle {
    color: #65756C;
    text-align: center;
    font-size: 16px;
}

.section-title {
    color: #173D32;
    font-size: 25px;
    font-weight: 700;
}

div.stButton > button {
    background-color: #347A60;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #245B46;
    color: white;
    border: none;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #D8DED5;
    padding: 18px;
    border-radius: 12px;
}

.response-box {
    background-color: #FFFFFF;
    border-left: 5px solid #347A60;
    padding: 20px;
    border-radius: 10px;
    color: #173D32;
}

.info-box {
    background-color: #E8EDE5;
    padding: 18px;
    border-radius: 10px;
    color: #173D32;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("# 🤖 Gayathri's")
    st.markdown("## AI STUDIO")
    st.caption("Think Smart. Route Smarter. ✨")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 AI Home",
            "💬 AI Playground",
            "📜 Request History",
            "📊 AI Analytics"
        ]
    )

    st.divider()

    st.markdown("### 🧠 AI System")

    if st.session_state.api_status is True:
        st.success("API Connected")
    elif st.session_state.api_status is False:
        st.error("API Disconnected")
    else:
        st.info("Connection not checked")

    if st.button("⚡ Check API Connection", use_container_width=True):
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            st.session_state.api_status = True
            st.success("FastAPI is running!")
        except requests.RequestException:
            st.session_state.api_status = False
            st.error("Unable to connect. Start the backend.")

    st.divider()

    st.caption("Built with Python, Streamlit, FastAPI & Groq")
    st.caption("✨ Created by Gayathri")

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "🏠 AI Home":

    st.markdown(
        '<div class="main-title">🤖 Welcome to Gayathri\'s AI Studio!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Intelligent question analysis and automatic AI model selection.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("## ✨ Think Smart. Route Smarter.")

    st.markdown("""
    <div class="info-box">
        <h3>🧠 Intelligent AI Model Auto-Routing System</h3>
        <p>
        Enter your question and let the system analyze its complexity.
        Based on the analysis, it automatically selects a suitable AI model
        and generates a response.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Questions",
            len(st.session_state.history)
        )

    with col2:
        complex_count = sum(
            1 for item in st.session_state.history
            if item["complexity"].lower() == "complex"
        )
        st.metric("Complex Questions", complex_count)

    with col3:
        st.metric("AI Models", "2")

    st.divider()

    st.markdown("### ⚙️ How the System Works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("#### 1. 📝 Input")
        st.write("Enter your question into the AI Playground.")

    with step2:
        st.markdown("#### 2. 🧠 Analyze")
        st.write("The classifier evaluates the question complexity.")

    with step3:
        st.markdown("#### 3. ⚡ Route")
        st.write("The router selects an AI model and generates an answer.")

    st.divider()

    st.markdown("### 🚀 Ready to Explore?")

    st.write(
        "Visit the AI Playground to ask your first question."
    )

# --------------------------------------------------
# AI PLAYGROUND
# --------------------------------------------------

elif page == "💬 AI Playground":

    st.markdown(
        '<div class="main-title">💬 AI Playground</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Ask anything. Let intelligent routing choose the model.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 📝 Enter Your Question")

    with st.form("question_form"):

        question = st.text_area(
            "Your Question",
            placeholder="Example: Explain machine learning with real-world examples...",
            height=150
        )

        submit = st.form_submit_button(
            "⚡ Analyze & Generate Response",
            use_container_width=True
        )

    if submit:

        if not question.strip():
            st.warning("Please enter a question first.")

        else:

            try:
                with st.spinner(
                    "🧠 Analyzing your question and selecting the best AI model..."
                ):

                    response = requests.post(
                        f"{API_URL}/ask",
                        json={"question": question.strip()},
                        timeout=180
                    )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.api_status = True

                    st.success("✨ Your AI response is ready!")

                    st.divider()

                    st.markdown("### 📊 Question Analysis")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Complexity",
                            result.get("complexity", "N/A").upper()
                        )

                    with col2:
                        st.metric(
                            "Complexity Score",
                            result.get("complexity_score", "N/A")
                        )

                    with col3:
                        st.metric(
                            "Confidence",
                            f'{result.get("confidence", 0)}%'
                        )

                    st.markdown("### ⚡ Selected AI Model")

                    st.code(
                        result.get("selected_model", "Not available"),
                        language="text"
                    )

                    st.markdown("### 🔍 Classification Reason")

                    st.info(
                        result.get("reason", "No reason provided.")
                    )

                    st.markdown("### 💡 AI Generated Answer")

                    answer = result.get(
                        "answer",
                        "No answer was returned."
                    )

                    st.markdown(
                        '<div class="response-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown(answer)

                    st.markdown("</div>", unsafe_allow_html=True)

                    # Save result in session history
                    st.session_state.history.append({
                        "question": question.strip(),
                        "complexity": result.get("complexity", "N/A"),
                        "score": result.get("complexity_score", 0),
                        "confidence": result.get("confidence", 0),
                        "model": result.get("selected_model", "N/A"),
                        "reason": result.get("reason", ""),
                        "answer": answer,
                        "time": datetime.now().strftime(
                            "%d-%m-%Y %I:%M %p"
                        )
                    })

                else:
                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    try:
                        st.write(response.json())
                    except ValueError:
                        st.write(response.text)

            except requests.exceptions.Timeout:
                st.error(
                    "The request took too long. Please try again."
                )

            except requests.exceptions.ConnectionError:
                st.session_state.api_status = False

                st.error(
                    "Cannot connect to FastAPI. "
                    "Please start your backend server first."
                )

            except requests.RequestException as error:
                st.error(f"Request failed: {error}")

            except ValueError:
                st.error("The API returned an invalid response.")

# --------------------------------------------------
# REQUEST HISTORY
# --------------------------------------------------

elif page == "📜 Request History":

    st.markdown(
        '<div class="main-title">📜 Request History</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Review your previously analyzed questions.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    if not st.session_state.history:

        st.info(
            "No questions have been analyzed yet. "
            "Visit the AI Playground to get started."
        )

    else:

        st.markdown(
            f"### Total Requests: {len(st.session_state.history)}"
        )

        for index, item in enumerate(
            reversed(st.session_state.history),
            start=1
        ):

            with st.expander(
                f"Question {len(st.session_state.history) - index + 1}: "
                f"{item['question'][:70]}"
            ):

                st.markdown("**Question:**")
                st.write(item["question"])

                col1, col2 = st.columns(2)

                with col1:
                    st.write(
                        f"**Complexity:** {item['complexity'].upper()}"
                    )
                    st.write(f"**Score:** {item['score']}")

                with col2:
                    st.write(f"**Model:** {item['model']}")
                    st.write(f"**Confidence:** {item['confidence']}%")

                st.caption(f"Time: {item['time']}")

                st.markdown("**AI Response:**")
                st.markdown(item["answer"])

        st.divider()

        if st.button("🗑️ Clear Request History"):
            st.session_state.history = []
            st.rerun()

# --------------------------------------------------
# ANALYTICS PAGE
# --------------------------------------------------

elif page == "📊 AI Analytics":

    st.markdown(
        '<div class="main-title">📊 AI Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Insights into your AI routing activity.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    history = st.session_state.history

    if not history:

        st.info(
            "Analytics will appear after you analyze some questions."
        )

    else:

        total = len(history)

        simple = sum(
            1 for item in history
            if item["complexity"].lower() == "simple"
        )

        medium = sum(
            1 for item in history
            if item["complexity"].lower() == "medium"
        )

        complex_count = sum(
            1 for item in history
            if item["complexity"].lower() == "complex"
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Questions", total)
        col2.metric("Simple", simple)
        col3.metric("Medium", medium)
        col4.metric("Complex", complex_count)

        st.divider()

        st.markdown("### 📈 Question Complexity Distribution")

        complexity_data = {
            "Complexity": ["Simple", "Medium", "Complex"],
            "Questions": [simple, medium, complex_count]
        }

        st.bar_chart(
            complexity_data,
            x="Complexity",
            y="Questions"
        )

        st.divider()

        st.markdown("### ⚡ AI Model Usage")

        model_counts = {}

        for item in history:
            model = item["model"]

            model_counts[model] = (
                model_counts.get(model, 0) + 1
            )

        st.bar_chart(model_counts)

        st.divider()

        st.markdown("### 🧠 Average Classification Confidence")

        average_confidence = sum(
            item["confidence"] for item in history
        ) / total

        st.metric(
            "Average Confidence",
            f"{average_confidence:.2f}%"
        )

        st.divider()

        st.markdown("### 📋 Recent Activity")

        for item in reversed(history[-5:]):

            st.write(
                f"**{item['complexity'].upper()}** — "
                f"{item['question'][:100]}"
            )

            st.caption(
                f"Model: {item['model']} | {item['time']}"
            )

            st.divider()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        color:#65756C;
        padding:25px;
        font-size:14px;
    ">
        🤖 Gayathri's AI Studio
        <br>
        Think Smart. Route Smarter. ✨
        <br>
        Built with Python | Streamlit | FastAPI | Groq
    </div>
    """,
    unsafe_allow_html=True
)
