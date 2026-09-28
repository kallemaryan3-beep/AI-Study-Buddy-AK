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
# GOOGLE LOGIN
# =========================================================

if not st.user.is_logged_in:

    st.title("📚 Study Buddy")

    st.subheader("Welcome to Study Buddy!")

    st.write(
        "Sign in with Google to access your study tools."
    )

    if st.button(
        "🔵 Sign in with Google",
        use_container_width=True
    ):
        st.login()

    st.stop()


# =========================================================
# GOOGLE ACCOUNT
# =========================================================

name = st.user.get(
    "name",
    "Student"
)

email = st.user.get(
    "email",
    ""
)

email_verified = st.user.get(
    "email_verified",
    False
)


if not email:
    st.error(
        "❌ Google did not provide an email address."
    )
    st.stop()


if not email_verified:
    st.error(
        "❌ Google could not verify this account."
    )
    st.stop()


# =========================================================
# GEMINI SETUP
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except KeyError:

    st.error(
        "❌ GEMINI_API_KEY was not found."
    )

    st.info(
        "Go to Streamlit Cloud → Manage app → "
        "Settings → Secrets and add your Gemini API key."
    )

    st.stop()


try:

    client = genai.Client(
        api_key=api_key
    )

except Exception as e:

    st.error(
        "❌ Could not connect to Gemini."
    )

    st.code(str(e))

    st.stop()


# New Gemini model
MODEL = "gemini-3.8-flash"


# =========================================================
# GEMINI FUNCTION
# =========================================================

def ask_gemini(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response is None:
            st.error(
                "❌ Gemini returned no response."
            )
            return None

        if not response.text:
            st.error(
                "❌ Gemini returned an empty response."
            )
            return None

        return response.text

    except Exception as e:

        st.error(
            "❌ Gemini error"
        )

        st.code(
            str(e)
        )

        return None


# =========================================================
# HEADER
# =========================================================

st.title("📚 Study Buddy")

st.write(
    f"Welcome, **{name}**! 👋"
)

st.caption(
    f"Signed in as: {email}"
)


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
    placeholder=(
        "Paste your class notes here..."
    )
)


# =========================================================
# STUDY TOOLS
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
# GENERATE BUTTON
# =========================================================

if st.button(
    "✨ Generate",
    use_container_width=True
):

    if not notes.strip():

        st.warning(
            "⚠️ Please paste your notes first."
        )

        st.stop()


    # =====================================================
    # QUIZ
    # =====================================================

    if option == "📝 Quiz":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Create a 10-question multiple-choice quiz using ONLY
the information in the student's notes.

For every question:

1. Write the question.
2. Give four choices:
   A.
   B.
   C.
   D.
3. Give the correct answer.
4. Give a short explanation.

Make the questions useful for studying.

Do not invent information that is not contained
in the student's notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # FLASHCARDS
    # =====================================================

    elif option == "🧠 Flashcards":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Create 15 flashcards from the student's notes.

Use this format:

### Flashcard 1

**Question:** ...

**Answer:** ...

Create flashcards about:

- Important vocabulary
- Definitions
- Important facts
- Key concepts
- People
- Dates
- Processes

Keep the answers short and easy to memorize.

Only use information from the student's notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # STUDY GUIDE
    # =====================================================

    elif option == "📚 Study Guide":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Turn the student's notes into a clear and organized
study guide.

Use these sections:

# 📌 Main Topics

# 📖 Important Vocabulary

# ⭐ Key Facts

# 🧠 Important Concepts

# ❗ Things to Remember

# 📝 Quick Review

Explain difficult ideas using simple language.

Only use information supported by the student's notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # EXPLAIN NOTES
    # =====================================================

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

Do not invent information that is not supported
by the student's notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # GENERATE
    # =====================================================

    st.divider()

    st.header("✨ Your Study Material")

    with st.spinner(
        "🤖 Study Buddy is working..."
    ):

        result = ask_gemini(
            prompt
        )


    if result:

        st.markdown(
            result
        )
