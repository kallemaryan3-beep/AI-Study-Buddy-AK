```python
import streamlit as st
from google import genai


# =========================================================
# PAGE CONFIG
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

    st.write(
        "Sign in with Google to use Study Buddy."
    )

    if st.button(
        "🔵 Sign in with Google",
        use_container_width=True
    ):
        st.login()

    st.stop()


# =========================================================
# GOOGLE USER INFORMATION
# =========================================================

name = st.user.get("name", "Student")
email = st.user.get("email", "")
email_verified = st.user.get(
    "email_verified",
    False
)


if not email:
    st.error("❌ Google did not provide an email address.")
    st.logout()
    st.stop()


# =========================================================
# GEMINI API KEY
# =========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except KeyError:

    st.error("❌ Gemini API key was not found.")

    st.info(
        "Go to Streamlit Cloud → Manage app → Settings → "
        "Secrets and add GEMINI_API_KEY."
    )

    st.stop()


# =========================================================
# CONNECT TO GEMINI
# =========================================================

try:

    client = genai.Client(
        api_key=api_key
    )

except Exception as e:

    st.error("❌ Could not connect to Gemini.")

    st.code(str(e))

    st.stop()


MODEL = "gemini-2.5-flash"


# =========================================================
# GEMINI FUNCTION
# =========================================================

def ask_gemini(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if not response or not response.text:

            return "Gemini did not return an answer."

        return response.text

    except Exception as e:

        st.error("❌ Gemini error")

        st.code(str(e))

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
# GENERATE
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

Create a 10-question multiple-choice quiz based ONLY
on the student's notes below.

For every question:

- Give four choices: A, B, C, and D.
- Clearly identify the correct answer.
- Give a short explanation.

Make the questions test understanding.

Do not invent information that is not in the notes.

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

Focus on important:

- Vocabulary
- Definitions
- Concepts
- Facts
- People
- Dates
- Processes

Keep answers short and easy to study.

Only use information from the notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # STUDY GUIDE
    # =====================================================

    elif option == "📚 Study Guide":

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Turn the student's notes into a clear study guide.

Use these sections:

# 📌 Main Topics

# 📖 Important Vocabulary

# ⭐ Key Facts

# 🧠 Important Concepts

# ❗ Things to Remember

# 📝 Quick Review

Explain difficult ideas in simple language.

Only use information supported by the notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # EXPLAIN NOTES
    # =====================================================

    else:

        prompt = f"""
You are Study Buddy, a helpful school study assistant.

Explain these notes in a way that is easy for a student
to understand.

For each major topic:

- Explain what it means.
- Explain the important idea.
- Define difficult vocabulary.
- Give a simple example when useful.
- Explain what the student should remember.

Use simple language while keeping the important information.

Do not invent information that is not supported by the notes.

STUDENT NOTES:

{notes}
"""


    # =====================================================
    # GENERATE WITH GEMINI
    # =====================================================

    st.divider()

    st.header("✨ Your Study Material")

    with st.spinner(
        "🤖 Study Buddy is working..."
    ):

        result = ask_gemini(prompt)

    if result:

        st.markdown(result)
```

### 2. Replace your `requirements.txt`

Use exactly:

```text
streamlit>=1.42.0
google-genai>=1.0.0
Authlib>=1.3.2
```

### 3. Check your Streamlit Secrets

Your Secrets should contain:

```toml
GEMINI_API_KEY = "YOUR_REAL_GEMINI_API_KEY"

[auth]
redirect_uri = "https://ai-study-buddy-ak.streamlit.app/oauth2callback"
cookie_secret = "YOUR_RANDOM_SECRET"
client_id = "YOUR_GOOGLE_CLIENT_ID"
client_secret = "YOUR_GOOGLE_CLIENT_SECRET"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

**Don't put the actual keys in GitHub or send them to me.**

### 4. Commit both files

In GitHub:

**`app.py` → Edit → replace everything → Commit changes**

Then:

**`requirements.txt` → Edit → replace everything → Commit changes**

Streamlit should redeploy.

### 5. Test Gemini

After Google login, put this into the notes box:

```text
The mitochondria produces ATP and is known as the powerhouse of the cell.
```

Select **📝 Quiz** and click **Generate**.

If Gemini still fails, this version will show the **actual Gemini error** on the screen instead of just saying "Something went wrong." That error will tell us exactly what needs fixing.
