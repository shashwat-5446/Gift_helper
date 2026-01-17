import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Personalized Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# -------------------------------------------------
# MODERN UI STYLING (WARM IVORY + GARAMOND)
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&display=swap');

/* Hide Streamlit defaults */
#MainMenu, footer, header {visibility: hidden;}

/* App background */
.stApp {
    background-color: #F7F3EB; /* warm ivory */
    font-family: 'EB Garamond', serif;
}

/* Center container */
.block-container {
    padding-top: 3rem;
    max-width: 700px;
}

/* Headings */
h1, h2, h3 {
    font-family: 'EB Garamond', serif;
    color: #2E2A26;
    text-align: center;
}

/* Paragraphs */
p, label {
    color: #5E5A55;
    font-size: 16px;
}

/* Card style */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* Buttons */
.stButton > button {
    background: #2E2A26;
    color: #FFFFFF;
    border-radius: 30px;
    padding: 0.75rem 1.2rem;
    font-size: 16px;
    border: none;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #1F1C19;
    transform: scale(1.05);
}

/* Select boxes */
.stSelectbox > div {
    border-radius: 10px;
}

/* Info box */
.stAlert {
    border-radius: 12px;
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
        "name": "Hardcover Minimal Journal",
        "budget": "₹500–₹1000",
        "style": "Minimal",
        "type": "Usable",
        "occasions": ["Just because"],
        "recipients": ["Self"],
        "reason": "Perfect for reflection and creativity."
    },
    {
        "name": "Abstract Art Print",
        "budget": "₹500–₹1000",
        "style": "Artistic",
        "type": "Decorative",
        "occasions": ["Birthday", "Festival"],
        "recipients": ["Friend", "Self"],
        "reason": "Adds personality without being loud."
    },
    {
        "name": "Indoor Plant in Ceramic Pot",
        "budget": "₹1000–₹2000",
        "style": "Minimal",
        "type": "Decorative",
        "occasions": ["Festival", "Just because"],
        "recipients": ["Parent", "Friend", "Self"],
        "reason": "Elegant living décor that fits any space."
    },
    {
        "name": "Customized Gift Box",
        "budget": "₹2000+",
        "style": "Luxury",
        "type": "Emotional",
        "occasions": ["Birthday", "Anniversary"],
        "recipients": ["Partner"],
        "reason": "A premium, curated gifting experience."
    }
]

# -------------------------------------------------
# RECOMMENDATION ENGINE
# -------------------------------------------------
def generate_recommendation(answers):
    for gift in GIFTS:
        if (
            gift["budget"] == answers["budget"]
            and gift["style"] == answers["style"]
            and gift["type"] == answers["type"]
            and answers["occasion"] in gift["occasions"]
            and answers["recipient"] in gift["recipients"]
        ):
            return gift["name"], gift["reason"]

    for gift in GIFTS:
        if gift["budget"] == answers["budget"]:
            return gift["name"], "This option fits your budget and overall preferences."

    return "Personalized Gift Card", "A flexible choice when preferences vary."

# -------------------------------------------------
# SCREENS
# -------------------------------------------------
def landing_screen():
    st.markdown("""
    <div class="card">
        <h1>Find the Perfect Personalized Gift 🎁</h1>
        <p style="text-align:center;">
            Answer a few thoughtful questions and get matched in under 2 minutes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎁 Find a Personalized Gift", use_container_width=True):
        st.session_state.page = "chat"

def chat_screen():
    st.markdown('<div class="card">', unsafe_allow_html=True)
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
        ["Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"]
    )

    if st.button("Get Recommendation", use_container_width=True):
        st.session_state.page = "result"

    st.markdown('</div>', unsafe_allow_html=True)

def result_screen():
    product, reason = generate_recommendation(st.session_state.answers)

    st.markdown(f"""
    <div class="card">
        <h2>🎉 Your Personalized Gift</h2>
        <h3>{product}</h3>
        <p>{reason}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Why this works:")
    st.write(
        f"- Great for **{st.session_state.answers['occasion']}**\n"
        f"- Fits a **{st.session_state.answers['style']}** style\n"
        f"- Matches your **{st.session_state.answers['budget']}** budget"
    )

    if st.button("Start Over"):
        st.session_state.page = "landing"
        st.session_state.answers = {}

# -------------------------------------------------
# ROUTER
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