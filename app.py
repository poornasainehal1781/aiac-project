import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# ---------------------------
# PAGE SETTINGS
# ---------------------------
st.set_page_config(page_title="Prompt2Program", page_icon="💻", layout="wide")

# ---------------------------
# SESSION STATE FOR HISTORY
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# CUSTOM CSS (ONLY UI CHANGE)
# ---------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #cbd5e1;
        margin-bottom: 30px;
    }

    .card {
        background: rgba(255, 255, 255, 0.06);
        padding: 20px;
        border-radius: 18px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        color: white;
        font-size: 17px;
        font-weight: bold;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.03);
        background: linear-gradient(90deg, #0891b2, #2563eb);
    }

    .history-box {
        background: rgba(255,255,255,0.04);
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 10px;
        border-left: 4px solid #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.title("📂 Navigation")
    page = st.radio("Go to", ["🏠 Home", "🕘 History", "ℹ️ About"])

    st.markdown("---")
    st.markdown("### 💡 Features")
    st.markdown("- AI Code Generator")
    st.markdown("- Explanation")
    st.markdown("- Sample Output")
    st.markdown("- Prompt History")
    st.markdown("- Modern UI")

# ---------------------------
# HOME PAGE
# ---------------------------
if page == "🏠 Home":
    st.markdown('<p class="main-title">💻 Prompt2Program</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI-Based Code Generator with Explanation</p>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # ---------------------------
    # USER INPUTS
    # ---------------------------
    api_key = os.getenv("OPENROUTER_API_KEY")
    prompt = st.text_area("Enter your coding prompt", placeholder="Example: Write a Python palindrome checker")
    language = st.selectbox("Select Programming Language", ["Python", "Java", "C", "C++", "JavaScript"])

    # ---------------------------
    # BUTTON ACTION
    # ---------------------------
    if st.button("🚀 Generate Code"):

        if not api_key:
            st.error("Please configure your OPENROUTER_API_KEY in the .env file.")
        elif not prompt:
            st.error("Please enter a coding prompt.")
        else:
            try:
                # OpenRouter Client
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                )

                # Better AI prompt
                full_prompt = f"""
You are an AI coding assistant.

The user may have spelling mistakes. Understand the intent correctly and generate the best possible answer.

Task:
Generate {language} code for this request:
"{prompt}"

Give the response exactly in this format:

CODE:
<only code here>

EXPLANATION:
<simple beginner-friendly explanation>

OUTPUT:
<sample output>

Rules:
- Generate proper working code
- Keep explanation simple
- Handle spelling mistakes in user prompt
- If user asks random code, generate best matching code
"""

                # AI Response
                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful AI coding assistant."},
                        {"role": "user", "content": full_prompt}
                    ]
                )

                output = response.choices[0].message.content

                # ---------------------------
                # SPLIT OUTPUT
                # ---------------------------
                try:
                    code_part = output.split("EXPLANATION:")[0].replace("CODE:", "").strip()
                    explanation_part = output.split("EXPLANATION:")[1].split("OUTPUT:")[0].strip()
                    output_part = output.split("OUTPUT:")[1].strip()
                except:
                    code_part = output
                    explanation_part = "Explanation not found."
                    output_part = "Output not found."

                # ---------------------------
                # SAVE HISTORY
                # ---------------------------
                st.session_state.history.insert(0, {
                    "prompt": prompt,
                    "language": language,
                    "code": code_part,
                    "explanation": explanation_part,
                    "output": output_part
                })

                # ---------------------------
                # DISPLAY
                # ---------------------------
                st.success("Code generated successfully!")

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("## 💻 Generated Code")
                    st.code(code_part, language=language.lower())

                with col2:
                    st.markdown("## 📘 Explanation")
                    st.write(explanation_part)

                st.markdown("## 🔍 Sample Output")
                st.code(output_part)

            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# HISTORY PAGE
# ---------------------------
elif page == "🕘 History":
    st.markdown('<p class="main-title">🕘 Prompt History</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Previously generated prompts and codes</p>', unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        st.info("No history available yet. Generate some code first.")
    else:
        for i, item in enumerate(st.session_state.history):
            with st.expander(f"{i+1}. {item['prompt']} ({item['language']})"):
                st.markdown("### 💻 Code")
                st.code(item["code"], language=item["language"].lower())

                st.markdown("### 📘 Explanation")
                st.write(item["explanation"])

                st.markdown("### 🔍 Output")
                st.code(item["output"])

# ---------------------------
# ABOUT PAGE
# ---------------------------
elif page == "ℹ️ About":
    st.markdown('<p class="main-title">ℹ️ About Project</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Prompt2Program Project Information</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📌 Project Name:</h3>
        <p><b>Prompt2Program</b> – AI-Based Code Generator with Explanation</p>

        <h3>🎯 Objective:</h3>
        <p>This project generates programming code from user prompts using AI.</p>

        <h3>🛠️ Technologies Used:</h3>
        <ul>
            <li>Python</li>
            <li>Streamlit</li>
            <li>OpenRouter API</li>
            <li>OpenAI SDK</li>
        </ul>

        <h3>✨ Features:</h3>
        <ul>
            <li>Generate code in multiple languages</li>
            <li>Provide beginner-friendly explanation</li>
            <li>Show sample output</li>
            <li>Maintain prompt history</li>
            <li>Modern web interface</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)