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
# OLD MONEY UI STYLING
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&display=swap');

#MainMenu, footer, header {visibility: hidden;}

.stApp {
    background-color: #F6F1E9;
    font-family: 'Cormorant Garamond', serif;
}

.block-container {
    max-width: 720px;
    padding-top: 3rem;
}

h1, h2, h3 {
    color: #3A2F2F;
    text-align: center;
    letter-spacing: 0.4px;
}

p, label {
    color: #5B4F4F;
    font-size: 17px;
}

.card {
    background: #FBF8F3;
    border-radius: 18px;
    padding: 36px;
    box-shadow: 0 18px 35px rgba(0,0,0,0.06);
    margin-bottom: 30px;
}

.stButton > button {
    background-color: #3A2F2F;
    color: #FBF8F3;
    border-radius: 26px;
    padding: 0.8rem 1.4rem;
    font-size: 16px;
    border: none;
}

.stButton > button:hover {
    background-color: #2A2121;
    transform: scale(1.04);
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
# GIFT DATABASE (AI SCORING BASE)
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
    },
    {
        "name": "Abstract Art Print",
        "budget": "₹500–₹1000",
        "style": ["Artistic", "Modern"],
        "type": ["Decorative"],
        "occasion": ["Birthday", "Festival"],
        "recipient": ["Friend", "Self"],
        "reason": "Adds personality without being loud."
    },
    {
        "name": "Personalized Photo Frame Set",
        "budget": "₹1000–₹2000",
        "style": ["Luxury", "Vintage"],
        "type": ["Emotional"],
        "occasion": ["Anniversary"],
        "recipient": ["Partner"],
        "reason": "Romantic and premium."
    },
    {
        "name": "Customized Gift Box",
        "budget": "₹2000+",
        "style": ["Luxury"],
        "type": ["Emotional", "Usable"],
        "occasion": ["Birthday", "Anniversary"],
        "recipient": ["Partner", "Parent"],
        "reason": "High-end, curated experience."
    }
]

# -------------------------------------------------
# AI-STYLE SCORING ENGINE
# -------------------------------------------------
def generate_recommendation(answers):
    best_score = -1
    best_gift = None

    for gift in GIFTS:
        score = 0

        if answers["budget"] == gift["budget"]:
            score += 4
        if answers["style"] in gift["style"]:
            score += 3
        if answers["type"] in gift["type"]:
            score += 3
        if answers["occasion"] in gift["occasion"]:
            score += 2
        if answers["recipient"] in gift["recipient"]:
            score += 2

        if score > best_score:
            best_score = score
            best_gift = gift

    if best_gift:
        return best_gift["name"], best_gift["reason"]

    return "Personalized Gift Card", "A flexible choice when preferences vary."

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
        ["Partner", "Friend", "Parent", "Pet", "Self"])
    a["occasion"] = st.selectbox("What’s the occasion?",
        ["Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Just because", "Other"])
    a["budget"] = st.selectbox("Your budget range?",
        ["under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000+"])
    a["type"] = st.selectbox("What kind of gift feels right?",
        ["Decorative", "Usable", "Emotional"])
    a["style"] = st.selectbox("Preferred style?",
        ["Minimal", "Artistic", "Cute", "Luxury", "Modern",
         "Vintage", "Bohemian", "Rustic", "Traditional"])

    if st.button("Get Recommendation", use_container_width=True):
        st.session_state.page = "result"

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# RESULT SCREEN
# -------------------------------------------------
def result_screen():
    product, reason = generate_recommendation(st.session_state.answers)

    st.markdown(f"""
    <div class="card">
        <h2>Your Personalized Gift</h2>
        <h3>{product}</h3>
        <p>{reason}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Start Over"):
        st.session_state.page = "landing"
        st.session_state.answers = {}

# -------------------------------------------------
# ROUTER (ALWAYS LAST)
# -------------------------------------------------
if st.session_state.page == "landing":
    landing_screen()
elif st.session_state.page == "chat":
    chat_screen()
elif st.session_state.page == "result":
    result_screen()
    st.markdown(
        "<p style='text-align:center; font-size:12px; color:gray;'>"
        "No signup. No payment. Just recommendations."      
        "</p>",
        unsafe_allow_html=True
    )