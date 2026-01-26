import streamlit as st

# -------------------------------------------------
# PAGE CONFIG (MUST BE FIRST)
# -------------------------------------------------
st.set_page_config(
    page_title="Personalized Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# -------------------------------------------------
# UI STYLING (STREAMLIT-SAFE + DEVICE CONSISTENT)
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');

#MainMenu, footer, header {visibility: hidden;}

/* FORCE LIGHT THEME EVERYWHERE */
html, body, [class*="css"] {
    color: #3A2F2F !important;
    font-family: 'Cormorant Garamond', serif;
}

/* APP BACKGROUND */
.stApp {
    background-color: #F6F1E9;
}

/* CONTAINER */
.block-container {
    max-width: 720px;
    padding-top: 3rem;
}

/* HEADINGS – STRONG VISUAL HIERARCHY */
h1 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 44px !important;
    font-weight: 600;
    letter-spacing: 0.6px;
    line-height: 1.2;
}

h2 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 32px !important;
    font-weight: 500;
    line-height: 1.3;
}

h3 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 24px !important;
    font-weight: 500;
}
/* HEADINGS – STRONG VISUAL HIERARCHY */
h1 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 44px !important;
    font-weight: 600;
    letter-spacing: 0.6px;
    line-height: 1.2;
}

h2 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 32px !important;
    font-weight: 500;
    line-height: 1.3;
}

h3 {
    color: #3A2F2F !important;
    text-align: center;
    font-size: 24px !important;
    font-weight: 500;
}


/* TEXT + LABELS */
p, label, span {
    color: #5B4F4F !important;
    font-size: 17px;
}

/* INPUT TEXT */
input, textarea, select {
    color: #3A2F2F !important;
    background-color: #FBF8F3 !important;
}

/* SELECTBOX LABEL FIX */
.stSelectbox label {
    color: #3A2F2F !important;
}

/* CARD */
.card {
    background: #FBF8F3;
    border-radius: 18px;
    padding: 36px;
    box-shadow: 0 18px 35px rgba(0,0,0,0.06);
    margin-bottom: 30px;
}

/* BUTTON BASE */
div.stButton > button {
    border-radius: 26px;
    padding: 0.9rem 1.4rem;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.25s ease-in-out;
}

/* ENABLED BUTTON */
div.stButton > button:not([disabled]) {
    background-color: #2E7D32;
    color: white;
}

/* HOVER */
div.stButton > button:not([disabled]):hover {
    background-color: #256628;
    transform: scale(1.05);
}

/* DISABLED BUTTON */
div.stButton > button[disabled] {
    background-color: #BDB4AF;
    color: white;
    cursor: not-allowed;
    opacity: 0.8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------------------------
# GIFT DATABASE
# -------------------------------------------------
GIFTS = [
    {
        "name": "Minimal Ceramic Mug",
        "budget": "under ₹500",
        "style": ["Minimal"],
        "type": ["Usable"],
        "occasion": ["Birthday", "Just because"],
        "recipient": ["Friend", "Partner", "Self"],
        "reason": "Simple, useful, and clutter-free."
    },
    {
        "name": "Single Photo Print",
        "budget": "under ₹500",
        "style": ["Minimal"],
        "type": ["Emotional"],
        "occasion": ["Memory / Keepsake"],
        "recipient": ["Partner", "Parent"],
        "reason": "A small but meaningful memory."
    },
    {
        "name": "Framed Minimal Photo Print",
        "budget": "₹500–₹1000",
        "style": ["Minimal", "Luxury"],
        "type": ["Emotional"],
        "occasion": ["Birthday", "Anniversary"],
        "recipient": ["Partner", "Friend", "Parent"],
        "reason": "Clean design with emotional value."
    }
]

# -------------------------------------------------
# SCORING ENGINE
# -------------------------------------------------
def generate_recommendation(answers):
    best_score = -1
    best_gift = None

    for gift in GIFTS:
        score = 0
        if answers["budget"] == gift["budget"]: score += 4
        if answers["style"] in gift["style"]: score += 3
        if answers["type"] in gift["type"]: score += 3
        if answers["occasion"] in gift["occasion"]: score += 2
        if answers["recipient"] in gift["recipient"]: score += 2

        if score > best_score:
            best_score = score
            best_gift = gift

    return best_gift["name"], best_gift["reason"]

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

# -------------------------------------------------
# CHAT SCREEN
# -------------------------------------------------
def chat_screen():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Let’s find the right gift")

    a = st.session_state.answers

    a["recipient"] = st.selectbox("Who is this gift for?",
        ["Select one", "Partner", "Friend", "Parent", "Self"])

    a["occasion"] = st.selectbox("What’s the occasion?",
        ["Select one", "Birthday", "Anniversary", "Memory / Keepsake", "Just because"])

    a["budget"] = st.selectbox("Your budget range?",
        ["Select one", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000+"])

    a["type"] = st.selectbox("What kind of gift feels right?",
        ["Select one", "Decorative", "Usable", "Emotional"])

    a["style"] = st.selectbox("Preferred style?",
        ["Select one", "Minimal", "Luxury", "Artistic", "Vintage", "Modern"])

    filled = sum(v != "Select one" for v in a.values())
    total = 5
    all_selected = filled == total

    st.progress(filled / total)

    if st.button("Get My Recommendation",
                 use_container_width=True,
                 disabled=not all_selected):
        st.session_state.page = "result"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# RESULT SCREEN
# -------------------------------------------------
def result_screen():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Your Personalized Gift 🎁")

    gift_name, gift_reason = generate_recommendation(st.session_state.answers)

    st.markdown(f"""
    <p style="text-align:center; font-size:20px; font-weight:bold;">
        {gift_name}
    </p>
    <p style="text-align:center;">
        {gift_reason}
    </p>
    """, unsafe_allow_html=True)

    if st.button("← Find Another Gift", use_container_width=True):
        st.session_state.page = "chat"

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if st.session_state.page == "landing":
    landing_screen()
elif st.session_state.page == "chat":
    chat_screen()
elif st.session_state.page == "result":
    result_screen()
