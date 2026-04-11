import streamlit as st
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Personalized Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# -------------------------------------------------
# STYLING
# -------------------------------------------------
st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}

html, body, .stApp {
    background-color: #F6F1E9 !important;
    font-family: 'Georgia', 'Times New Roman', serif !important;
}

.block-container {
    max-width: 720px;
    padding-top: 3rem;
}

h1, h2, h3 {
    color: #3A2F2F !important;
    text-align: center;
    font-family: 'Georgia', serif !important;
}

.stSelectbox label, .stTextInput label, p {
    color: #5B4F4F !important;
    font-size: 17px !important;
    font-family: 'Georgia', serif !important;
}

.card {
    background: #FBF8F3;
    border-radius: 18px;
    padding: 36px;
    box-shadow: 0 18px 35px rgba(0,0,0,0.06);
    margin-bottom: 30px;
}

.stButton > button {
    background-color: #3A2F2F !important;
    color: #FBF8F3 !important;
    border-radius: 28px !important;
    padding: 0.8rem 1.4rem !important;
    font-size: 16px !important;
    border: none !important;
    width: 100%;
    font-family: 'Georgia', serif !important;
}

.stButton > button:hover {
    background-color: #2A2121 !important;
    transform: scale(1.04);
}

.stButton > button:disabled {
    background-color: #C9B99A !important;
    color: #F6F1E9 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

.stSelectbox > div > div {
    background-color: #FBF8F3 !important;
    border-color: #C9B99A !important;
    color: #3A2F2F !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "loading"

if "loaded" not in st.session_state:
    st.session_state.loaded = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------------------------
# LOADING SCREEN
# -------------------------------------------------
def loading_screen():
    if not st.session_state.loaded:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <div style="font-size:64px;">🎁</div>
            <h2>Preparing your gift experience</h2>
            <p>Thoughtful things take a moment…</p>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1.5)

        st.session_state.loaded = True
        st.session_state.page = "landing"
        st.rerun()

# -------------------------------------------------
# LANDING SCREEN
# -------------------------------------------------
def landing_screen():
    st.markdown("""
    <div class="card">
        <h1>Find the Perfect Personalized Gift 🎁</h1>
        <p style="text-align:center;">
            Answer a few questions. Get matched in under 2 minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎁 Find a Personalized Gift", use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()

# -------------------------------------------------
# CHAT SCREEN
# -------------------------------------------------
def chat_screen():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Let's find the right gift")

    a = st.session_state.answers

    a["recipient"] = st.selectbox(
        "Who is this gift for?",
        ["-- Select --", "Partner", "Friend", "Parent", "Pet", "Self"]
    )

    a["occasion"] = st.selectbox(
        "What's the occasion?",
        ["-- Select --", "Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Just because", "Other"]
    )

    a["budget"] = st.selectbox(
        "Your budget range?",
        ["-- Select --", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000+"]
    )

    a["type"] = st.selectbox(
        "What kind of gift feels right?",
        ["-- Select --", "Decorative", "Usable", "Emotional"]
    )

    a["style"] = st.selectbox(
        "Preferred style?",
        ["-- Select --", "Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"]
    )

    # ✅ BOOLEAN CHECK — all fields must be answered (not "-- Select --")
    all_answered = all(
        v != "-- Select --" and v != "" and v is not None
        for v in [a.get("recipient"), a.get("occasion"), a.get("budget"), a.get("type"), a.get("style")]
    )

    # Show warning if not all answered
    if not all_answered:
        st.warning("⚠️ Please answer all questions to continue.")

    # Button is disabled until all answered
    if st.button("Get Recommendation ✨", use_container_width=True, disabled=not all_answered):
        st.session_state.page = "result"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# RECOMMENDATION LOGIC
# -------------------------------------------------
def generate_recommendation(budget, style, occasion, recipient):

    if budget == "under ₹500":
        if style == "Minimal":
            if occasion in ["Birthday", "Just because"]:
                return "Minimal Ceramic Mug", "Simple, useful, and clutter-free."
            if occasion == "Memory / Keepsake":
                return "Single Photo Print", "A small but meaningful memory."
        if style == "Cute" and recipient in ["Friend", "Partner"]:
            return "Cute Keychain or Mini Plush", "Fun, light, and affordable."
        if style == "Traditional":
            return "Incense Sticks + Holder", "Culturally meaningful and calming."

    elif budget == "₹500–₹1000":
        if style == "Minimal":
            return "Framed Minimal Photo Print", "Clean design with emotional value."
        if style == "Artistic":
            return "Abstract Art Print", "Adds personality without being loud."

    elif budget == "₹1000–₹2000":
        if style == "Luxury":
            return "Personalized Photo Frame Set", "Romantic and premium."

    elif budget == "₹2000+":
        return "Customized Gift Box", "High-end, curated experience."

    return "Personalized Gift Card", "A flexible choice when preferences vary."

# -------------------------------------------------
# RESULT SCREEN
# -------------------------------------------------
def result_screen():
    a = st.session_state.answers

    product, reason = generate_recommendation(
        a["budget"], a["style"], a["occasion"], a["recipient"]
    )

    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <div style="font-size:56px;">🎁</div>
        <h2>Your Personalized Gift</h2>
        <h3>{product}</h3>
        <p style="margin-top:12px;">{reason}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Start Over", use_container_width=True):
        st.session_state.page = "landing"
        st.session_state.answers = {}
        st.rerun()

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if st.session_state.page == "loading":
    loading_screen()
elif st.session_state.page == "landing":
    landing_screen()
elif st.session_state.page == "chat":
    chat_screen()
elif st.session_state.page == "result":
    result_screen()
