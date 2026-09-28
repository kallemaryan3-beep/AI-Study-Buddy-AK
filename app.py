import streamlit as st
from google import genai

# =========================
# GEMINI
# =========================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-2.5-flash"


def ask_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


# =========================
# LOGIN
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("📚 Study Buddy")

    st.subheader("Welcome to Study Buddy!")

    name = st.text_input(
        "Your name",
        placeholder="Enter your name"
    )

    gmail = st.text_input(
        "Your Gmail",
        placeholder="example@gmail.com"
    )

    if st.button("Continue", use_container_width=True):

        name = name.strip()
        gmail = gmail.strip().lower()

        if not name:
            st.error("Please enter your name.")
            st.stop()

        if not gmail:
            st.error("Please enter your Gmail.")
            st.stop()

        if not gmail.endswith("@gmail.com"):
            st.error("❌ Wrong Gmail. Please enter a Gmail address ending in @gmail.com.")
            st.stop()

        # Save login information
        st.session_state.name = name
        st.session_state.gmail = gmail
        st.session_state.logged_in = True

        st.rerun()

    st.stop()


# =========================
# MAIN APP
# =========================

st.title("📚 Study Buddy")

st.write(
    f"Welcome, **{st.session_state.name}**! 👋"
)

st.caption(
    f"Signed in as: {st.session_state.gmail}"
)

if st.button("Log out"):
    st.session_state.logged_in = False
    st.rerun()

st.divider()


# =========================
# NOTES
# =========================

st.header("📖 Your Notes")

notes = st.text_area(
    "Paste your notes below",
    height=250,
    placeholder="Paste your class notes here..."
)


# =========================
# STUDY OPTIONS
# =========================

st.header("What do you want to make?")

option = st.selectbox(
    "Choose a study tool",
    [
        "📝 Quiz",
        "🧠 Flashcards",
        "📚 Study Guide",
        "💡 Explain My Notes"
    ]
)


# =========================
# GENERATE
# =========================

if st.button("✨ Generate", use_container_width=True):

    if not notes.strip():
        st.warning("Please enter your notes first.")
        st.stop()

    if option == "📝 Quiz":

        prompt = f"""
You are Study Buddy, an AI school study assistant.

Create a 10-question multiple-choice quiz using ONLY
the information in the student's notes.

For every question:
- Give 4 answer choices.
- Clearly identify the correct answer.
- Give a short explanation.

Make the questions useful for studying.

NOTES:
{notes}
"""

    elif option == "🧠 Flashcards":

        prompt = f"""
You are Study Buddy, an AI school study assistant.

Create 15 useful flashcards from these notes.

Use this format:

Card 1
Question: ...
Answer: ...

Keep answers short and easy to study.

Only use information from the notes.

NOTES:
{notes}
"""

    elif option == "📚 Study Guide":

        prompt = f"""
You are Study Buddy, an AI school study assistant.

Turn these notes into a well-organized study guide.

Include:

# Main Topics

# Important Vocabulary

# Key Facts

# Important Concepts

# Things to Remember

# Quick Review

Explain everything clearly and make it easy for a student
to study.

Only use information supported by the notes.

NOTES:
{notes}
"""

    else:

        prompt = f"""
You are Study Buddy, an AI school study assistant.

Explain the student's notes in simple language.

For each major topic:
- Explain what it means.
- Explain the important idea.
- Define difficult vocabulary.
- Give a simple example when useful.
- Point out important facts to remember.

Make the explanation easy for a student to understand.

Do not add unsupported information.

NOTES:
{notes}
"""

    with st.spinner("🤖 Study Buddy is creating your study material..."):

        try:
            result = ask_gemini(prompt)

            st.divider()
            st.header("✨ Your Study Material")

            st.markdown(result)

        except Exception as e:

            st.error(
                "Something went wrong while generating your study material."
            )

            st.caption(str(e))
