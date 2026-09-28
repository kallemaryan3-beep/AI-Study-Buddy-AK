import streamlit as st
from google import genai

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# GOOGLE LOGIN
# =========================================================

if not st.user.is_logged_in:
    st.title("📚 Study Buddy")
    st.subheader("Welcome!")

    st.write("Sign in with Google to use Study Buddy.")

    if st.button("🔵 Sign in with Google", use_container_width=True):
        st.login()

    st.stop()

# =========================================================
# GOOGLE USER
# =========================================================

name = st.user.get("name", "Student")
email = st.user.get("email", "")
email_verified = st.user.get("email_verified", False)

if not email or not email_verified:
    st.error("❌ Your Google account could not be verified.")
    st.stop()

# =========================================================
# GEMINI
# =========================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception as e:
    st.error("❌ Gemini could not be started.")
    st.code(str(e))
    st.stop()

MODEL = "gemini-2.5-flash"


def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response and response.text:
            return response.text

        return "Gemini did not return a response."

    except Exception as e:
        st.error("❌ Gemini error:")
        st.code(str(e))
        return None


# =========================================================
# HEADER
# =========================================================

st.title("📚 Study Buddy")

st.write(f"Welcome, **{name}**! 👋")
st.caption(f"Signed in as: {email}")

if st.button("🚪 Sign out"):
    st.logout()

st.divider()

# =========================================================
# NOTES
# =========================================================

st.header("📖 Your Notes")

notes = st.text_area(
    "Paste your notes here",
    height=300,
    placeholder="Paste your class notes here..."
)

# =========================================================
# STUDY OPTIONS
# =========================================================

st.header("🎓 What do you want to make?")

option = st.selectbox(
    "Choose a study tool",
    [
        "📝 Quiz",
        "🧠 Flashcards",
        "📚 Study Guide",
        "💡 Explain My Notes"
    ]
)

# =========================================================
# GENERATE
# =========================================================

if st.button("✨ Generate", use_container_width=True):

    if not notes.strip():
        st.warning("⚠️ Please paste your notes first.")
        st.stop()

    # -----------------------------------------------------
    # QUIZ
    # -----------------------------------------------------

    if option == "📝 Quiz":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Create a 10-question multiple-choice quiz using ONLY
the student's notes.

Each question must have:

A. answer
B. answer
C. answer
D. answer

After each question, show:

Correct Answer:
Explanation:

Make the questions useful for studying.

Do not make up information that is not in the notes.

NOTES:
{notes}
"""

    # -----------------------------------------------------
    # FLASHCARDS
    # -----------------------------------------------------

    elif option == "🧠 Flashcards":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Create 15 flashcards from the student's notes.

Use this format:

### Flashcard 1

**Question:** question

**Answer:** answer

Focus on important vocabulary, definitions,
concepts, facts, people, dates, and processes.

Keep answers clear and easy to memorize.

Only use information from the notes.

NOTES:
{notes}
"""

    # -----------------------------------------------------
    # STUDY GUIDE
    # -----------------------------------------------------

    elif option == "📚 Study Guide":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Turn the student's notes into a clear study guide.

Include:

# Main Topics

# Important Vocabulary

# Key Facts

# Important Concepts

# Things to Remember

# Quick Review

Explain difficult ideas in simple language.

Only use information supported by the notes.

NOTES:
{notes}
"""

    # -----------------------------------------------------
    # EXPLAIN NOTES
    # -----------------------------------------------------

    else:

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Explain the student's notes in simple language.

For each major topic:

- Explain what it means.
- Explain the important idea.
- Define difficult vocabulary.
- Give a simple example when useful.
- Explain what the student should remember.

Make the explanation easy for a student to understand.

Do not invent information that is not supported by the notes.

NOTES:
{notes}
"""

    # =====================================================
    # GEMINI RESPONSE
    # =====================================================

    st.divider()
    st.header("✨ Your Study Material")

    with st.spinner("🤖 Study Buddy is working..."):

        result = ask_gemini(prompt)

    if result:
        st.markdown(result)
