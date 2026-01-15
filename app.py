import streamlit as st
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Personalized Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS (PAINT BRUSH STYLE)
# -----------------------------
st.markdown("""
<style>
/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(135deg, #fdf6f0, #ffeef6);
    font-family: 'Poppins', sans-serif;
}

/* Center container */
.block-container {
    padding-top: 3rem;
}

/* Paint brush cards */
.paint-card {
    background: linear-gradient(135deg, #ffd6e0, #cce6ff);
    border-radius: 60% 40% 55% 45%;
    padding: 30px;
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    text-align: center;
}

/* Headings */
h1, h2, h3 {
    text-align: center;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff9aa2, #ffb7b2);
    border: none;
    border-radius: 30px;
    padding: 0.75rem;
    font-size: 16px;
    color: white;
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, #ff758f, #ff9a9e);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State Init
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "loading"

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# LOADING SCREEN
# -----------------------------
def loading_screen():
    st.markdown(
        """
        <div class="paint-card">
            <div style="font-size:80px;">🎁</div>
            <h2>Preparing your gift experience...</h2>
            <p style="color:gray;">Just a moment ✨</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(2)
    st.session_state.page = "landing"
    st.rerun()

# -----------------------------
# LANDING SCREEN
# -----------------------------
def landing_screen():
    st.markdown(
        """
        <div class="paint-card">
            <h1>Find the Perfect Personalized Gift 🎁</h1>
            <p style="color:gray;">
                Answer a few questions. Get matched in under 2 minutes.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🎁 Find a Personalized Gift", use_container_width=True):
        st.session_state.page = "chat"

    st.markdown(
        "<p style='text-align:center; font-size:12px; color:gray;'>"
        "No signup. No payment. Just recommendations."
        "</p>",
        unsafe_allow_html=True
    )

# -----------------------------
# CHAT / QUESTION FLOW
# -----------------------------
def chat_screen():
    st.markdown("<h2>Let’s find the right gift 🎨</h2>", unsafe_allow_html=True)

    st.session_state.answers["recipient"] = st.selectbox(
        "Who is this gift for?",
        ["Partner", "Friend", "Parent", "Pet", "Self"]
    )

    st.session_state.answers["occasion"] = st.selectbox(
        "What’s the occasion?",
        ["Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Just because"]
    )

    st.session_state.answers["budget"] = st.selectbox(
        "Your budget range?",
        ["₹500–₹1000", "₹1000–₹2000", "₹2000+"]
    )

    st.session_state.answers["type"] = st.selectbox(
        "What kind of gift feels right?",
        ["Decorative", "Usable", "Emotional"]
    )

    st.session_state.answers["style"] = st.selectbox(
        "Preferred style?",
        ["Minimal", "Artistic", "Cute", "Luxury"]
    )

    st.session_state.answers["photo"] = st.file_uploader(
        "Upload a photo (optional)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("Get Recommendation", use_container_width=True):
        st.session_state.page = "result"

# -----------------------------
# RECOMMENDATION LOGIC
# -----------------------------
def generate_recommendation(answers):
    if answers["type"] == "Emotional":
        return "Personalized Photo Frame", (
            "Photo frames are timeless and emotional, perfect for preserving memories."
        )

    if answers["type"] == "Usable":
        return "Custom Photo Mug", (
            "A photo mug is practical and personal — something they’ll use every day."
        )

    return "Custom Poster or Canvas Print", (
        "Decorative posters and canvas prints add personality to any space."
    )

# -----------------------------
# RESULT SCREEN
# -----------------------------
def result_screen():
    product, reason = generate_recommendation(st.session_state.answers)

    st.markdown(
        f"""
        <div class="paint-card">
            <h2>🎉 Your Personalized Gift</h2>
            <h3>{product}</h3>
            <p>{reason}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Why this works:")
    st.write(
        f"- Great for **{st.session_state.answers['occasion']}**\n"
        f"- Fits a **{st.session_state.answers['style']}** style\n"
        f"- Matches your **{st.session_state.answers['budget']}** budget"
    )

    if st.button("Start Over"):
        st.session_state.page = "landing"
        st.session_state.answers = {}

# -----------------------------
# PAGE ROUTER
# -----------------------------
if st.session_state.page == "loading":
    loading_screen()
elif st.session_state.page == "landing":
    landing_screen()
elif st.session_state.page == "chat":
    chat_screen()
elif st.session_state.page == "result":
    result_screen()

