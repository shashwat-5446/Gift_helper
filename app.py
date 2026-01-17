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
# OLD MONEY UI STYLING (CREAM + CLASSIC SERIF)
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
    border-radius: 28px;
    padding: 0.8rem 1.4rem;
    font-size: 16px;
    border: none;
    transition: 0.3s ease;
}

.stButton > button:hover {
    background-color: #2A2121;
    transform: scale(1.04);
}

.stSelectbox > div {
    border-radius: 10px;
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
        <div style="font-size:64px;">🎁</div>
        <h2>Preparing your gift experience</h2>
        <p>Thoughtful things take a moment…</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading..."):
        time.sleep(2)

    st.session_state.page = "landing"
    st.rerun()

# -------------------------------------------------
# LANDING SCREEN
# -------------------------------------------------
def landing_screen():
    st.markdown("""
    <div class="card">
        <h1>Find the Perfect Personalized Gift</h1>
        <p style="text-align:center;">
            Answer a few questions. Get matched in under 2 minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎁 Find a Personalized Gift"
, use_container_width=True):
        st.session_state.page = "chat"
        st.rerun()

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -----------------------------
# LANDING SCREEN
# -----------------------------
def landing_screen():
    st.markdown("<h1 style='text-align:center;'>Find the Perfect Personalized Gift 🎁</h1>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center; color:gray;'>"
        "Answer a few questions. Get matched in under 2 minutes."
        "</p>",
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
    st.header("Let’s find the right gift")

    st.session_state.answers["recipient"] = st.selectbox(
        "Who is this gift for?",
        ["Partner", "Friend", "Parent", "Pet", "Self"]
    )

    st.session_state.answers["occasion"] = st.selectbox(
        "What’s the occasion?",
       ["Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Just because", "Other"]
    )
    st.session_state.answers["budget"] = st.selectbox(
        "Your budget range?",
        ["under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000+"]
    )

    st.session_state.answers["type"] = st.selectbox(
        "What kind of gift feels right?",
        ["Decorative", "Usable", "Emotional"]
    )

    st.session_state.answers["style"] = st.selectbox(
        "Preferred style?",
      ["Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian" ,"Rustic" , "Traditional" ]
    )

    st.session_state.answers["photo"] = st.file_uploader(
        "Upload a photo (optional)",
        type=["jpg", "jpeg", "png"]
    )

    if st.button("Get Recommendation", use_container_width=True):
        st.session_state.page = "result"

# -----------------------------
# SIMPLE RECOMMENDATION LOGIC
# -----------------------------
def generate_recommendation(budget, style, occasion, recipient):

    # -----------------------------
    # UNDER ₹500
    # -----------------------------
    if budget == "under ₹500":

        if style == "Minimal":
            if occasion in ["Birthday", "Just because"]:
                return "Minimal Ceramic Mug", "Simple, useful, and clutter-free."
            if occasion == "Memory / Keepsake":
                return "Single Photo Print", "A small but meaningful memory."

        if style == "Cute":
            if recipient in ["Friend", "Partner"]:
                return "Cute Keychain or Mini Plush", "Fun, light, and affordable."

        if style == "Traditional":
            return "Incense Sticks + Holder", "Culturally meaningful and calming."

    # -----------------------------
    # ₹500 – ₹1000
    # -----------------------------
    elif budget == "₹500–₹1000":

        if style == "Minimal":
            if occasion in ["Birthday", "Anniversary", "Just because"]:
                return "Framed Minimal Photo Print", "Clean design with emotional value."
            if recipient == "Self":
                return "Hardcover Minimal Journal", "Perfect for personal reflection."

        if style == "Artistic":
            return "Abstract Art Print", "Adds personality without being loud."

        if style == "Luxury":
            return "Metal Pen or Desk Accessory", "Premium feel within budget."

        if style == "Modern":
            return "Ambient LED Desk Lamp", "Sleek and functional décor."

    # -----------------------------
    # ₹1000 – ₹2000
    # -----------------------------
    elif budget == "₹1000–₹2000":

        if style == "Minimal":
            return "Indoor Plant in Ceramic Pot", "Elegant, living décor."

        if style == "Luxury":
            if recipient == "Partner":
                return "Personalized Photo Frame Set", "Romantic and premium."

        if style == "Vintage":
            return "Vintage-Style Desk Clock", "Classic charm with utility."

        if style == "Bohemian":
            return "Macramé Wall Hanging", "Artistic and free-spirited décor."

    # -----------------------------
    # ₹2000+
    # -----------------------------
    elif budget == "₹2000+":

        if style == "Luxury":
            return "Customized Gift Box", "High-end, curated experience."

        if style == "Traditional":
            return "Brass Décor or Idol", "Timeless and culturally rich."

        if style == "Modern":
            return "Smart Desk Accessory", "Functional with a tech-forward feel."

    # -----------------------------
    # FALLBACK
    # -----------------------------
    return "Personalized Gift Card", "A flexible choice when preferences vary."

# -----------------------------
# RESULT SCREEN
# -----------------------------
def result_screen():
    st.header("🎉 Your Personalized Gift Recommendation")

    product, reason = generate_recommendation(st.session_state.answers)

    st.subheader(product)
    st.write(reason)

    st.markdown("### Why this works:")
    st.write(
        f"- Great for **{st.session_state.answers['occasion']}**\n"
        f"- Fits a **{st.session_state.answers['style']}** style\n"
        f"- Matches your **{st.session_state.answers['budget']}** budget"
    )

    st.markdown("---")

    st.info("Next step: We’ll connect you with trusted customizers (coming next).")

    if st.button("Start Over"):
        st.session_state.page = "landing"
        st.session_state.answers = {}

# -----------------------------
# PAGE ROUTER
# -----------------------------
if st.session_state.page == "landing":
    landing_screen()
elif st.session_state.page == "chat":
    chat_screen()
elif st.session_state.page == "result":
    result_screen()
