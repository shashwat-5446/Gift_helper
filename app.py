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
# ARTISTIC UI STYLING (COLORFUL + CURSIVE)
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Playfair+Display:wght@400;600&display=swap');

/* Hide Streamlit defaults */
#MainMenu, footer, header {visibility: hidden;}

/* Artistic gradient background */
.stApp {
    background: linear-gradient(135deg, #fde2e4, #e2f0ff, #fef6d8);
    font-family: 'Playfair Display', serif;
}

/* Container */
.block-container {
    padding-top: 3rem;
    max-width: 720px;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Pacifico', cursive;
    color: #3A2F2F;
    text-align: center;
}

/* Text */
p, label {
    color: #5E4B4B;
    font-size: 16px;
}

/* Card (paint style) */
.card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 45px 30px 45px 30px;
    padding: 36px;
    box-shadow: 0 25px 45px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff758f, #ff9a9e);
    color: white;
    border-radius: 40px;
    padding: 0.8rem 1.4rem;
    font-size: 16px;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.07);
    background: linear-gradient(135deg, #ff5c8a, #ff7a7a);
}

/* Inputs */
.stSelectbox > div {
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "loading"

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------------------------
# LOADING SCREEN
# -------------------------------------------------
def loading_screen():
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:80px;">🎁</div>
        <h2>Preparing your gift experience</h2>
        <p>A little magic is on the way…</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Curating something special for you..."):
        time.sleep(2)

    st.session_state.page = "landing"
    st.rerun()

# -------------------------------------------------
# GIFT DATABASE
# -------------------------------------------------
GIFTS = [
    {
        "name": "Minimal Ceramic Mug",
        "budget": "under ₹500",
        "style": "Minimal",
        "type": "Usable",
        "occasions": ["Birthday", "Just because"],
        "recipients": ["Friend", "Partner", "Self"],
        "reason": "Simple, practical, and clutter-free."
    },
    {
        "name": "Single Photo Print",
        "budget": "under ₹500",
        "style": "Minimal",
        "type": "Emotional",
        "occasions": ["Memory / Keepsake"],
        "recipients": ["Partner", "Parent"],
        "reason": "A small but meaningful memory."
    },
    {
        "name": "Framed Minimal Photo Print",
        "budget": "₹500–₹1000",
        "style": "Minimal",
        "type": "Emotional",
        "occasions": ["Birthday", "Anniversary"],
        "recipients": ["Partner", "Friend", "Parent"],
        "reason": "Clean design with emotional value."
    },
    {
        "name": "Artistic Watercolor Portrait",
        "budget": "₹1000–₹2000",
        "style": "Artistic",
        "type": "Emotional",
        "occasions": ["Birthday", "Memory / Keepsake"],
        "recipients": ["Partner", "Friend", "Parent"],
        "reason": "A unique and heartfelt keepsake."
    }
]
