import streamlit as st
from google import genai


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# GEMINI SETUP
# =========================================================

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key
    )

except Exception:
    st.error("❌ Gemini API key is missing.")
    st.info(
        "Go to Streamlit Cloud → Manage app → Settings → Secrets "
        "and add GEMINI_API_KEY."
    )
    st.stop()


MODEL = "gemini-2.5-flash"


def ask_gemini(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text


# =========================================================
# GOOGLE LOGIN
# =========================================================

if not st.user.is_logged_in:

    st.title("📚 Study Buddy")

    st.subheader("Welcome to Study Buddy!")

    st.write(
        "Sign in with your Google account to start studying."
    )

    st.info(
        "Google will verify your account and provide your name "
        "and email automatically."
    )

    if st.button(
        "🔵 Sign in with Google",
        use_container_width=True
    ):
        st.login()

    st.stop()


# =========================================================
# GET GOOGLE ACCOUNT
# =========================================================

name = getattr(st.user, "name", None)
email = getattr(st.user, "email", None)
email_verified = getattr(
    st.user,
    "email_verified",
    False
)


# =========================================================
# VERIFY GOOGLE ACCOUNT
# =========================================================

if not email or not email_verified:

    st.error(
        "❌ Your Google account could not be verified."
    )

    if st.button("Try again"):
        st.logout()

    st.stop()


# =========================================================
# HEADER
# =========================================================

st.title("📚 Study Buddy")

st.write(
    f"Welcome, **{name}**! 👋"
)

st.caption(
    f"Signed in with: {email}"
)


if st.button("🚪 Sign out"):
    st.logout()


st.divider()


# =========================================================
# NOTES INPUT
# =========================================================

st.header("📖 Your Notes")

notes = st.text_area(
    "Paste your notes here",
    height=300,
    placeholder=(
        "Paste your class notes here and Study Buddy "
        "will turn them into study material..."
    )
)


# =========================================================
# STUDY TOOL
# =========================================================

st.header("🎓 Choose a Study Tool")

option = st.selectbox(
    "What would you like Study Buddy to create?",
    [
        "📝 Quiz",
        "🧠 Flashcards",
        "📚 Study Guide",
        "💡 Explain My Notes"
    ]
)


# =========================================================
# QUIZ
# =========================================================

def create_quiz(notes):

    return f"""
You are Study Buddy, an AI school study assistant.

Create a quiz using ONLY the information in the notes.

Create 10 multiple-choice questions.

For every question:

1. Write the question.
2. Give four answer choices:
   A.
   B.
   C.
   D.
3. Clearly state the correct answer.
4. Give a short explanation of the answer.

Make the questions test understanding rather than just copying
sentences from the notes.

Do not make up facts that aren't supported by the notes.

NOTES:

{notes}
"""


# =========================================================
# FLASHCARDS
# =========================================================

def create_flashcards(notes):

    return f"""
You are Study Buddy, an AI school study assistant.

Create 15 useful flashcards from the student's notes.

Use this format:

### Flashcard 1

**Question:** ...
**Answer:** ...

Keep the answers short and easy to memorize.

Focus on:
- Important vocabulary
- Important people
- Important dates
- Definitions
- Key concepts
- Important facts

Only use information found in the notes.

NOTES:

{notes}
"""


# =========================================================
# STUDY GUIDE
# =========================================================

def create_study_guide(notes):

    return f"""
You are Study Buddy, an AI school study assistant.

Turn the student's notes into a complete but easy-to-read
study guide.

Organize it using:

# 📌 Main Topics

# 📖 Important Vocabulary

# ⭐ Key Facts

# 🧠 Important Concepts

# ❗ Things to Remember

# 📝 Quick Review

Explain difficult ideas in simple language.

Only use information supported by the student's notes.

NOTES:

{notes}
"""


# =========================================================
# EXPLAIN NOTES
# =========================================================

def explain_notes(notes):

    return f"""
You are Study Buddy, an AI school study assistant.

Explain the student's notes so that a student can understand
them easily.

For every major topic:

- Explain what it means.
- Explain the important idea.
- Define difficult vocabulary.
- Give a simple example when helpful.
- Point out what the student should remember.

Use simple language without removing important information.

Do not add unsupported information.

NOTES:

{notes}
"""


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button(
    "✨ Generate",
    use_container_width=True
):

    if not notes.strip():

        st.warning(
            "⚠️ Please paste your notes before generating."
        )

        st.stop()


    # Choose prompt

    if option == "📝 Quiz":

        prompt = create_quiz(notes)

    elif option == "🧠 Flashcards":

        prompt = create_flashcards(notes)

    elif option == "📚 Study Guide":

        prompt = create_study_guide(notes)

    else:

        prompt = explain_notes(notes)


    # Generate response

    with st.spinner(
        "🤖 Study Buddy is creating your study material..."
    ):

        try:

            result = ask_gemini(prompt)

            st.divider()

            st.header("✨ Your Study Material")

            st.markdown(result)

        except Exception as e:

            st.error(
                "❌ Something went wrong while using Gemini."
            )

            st.caption(
                "Check your Gemini API key and try again."
            )
