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
# SESSION STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "answers" not in st.session_state:
    st.session_state.answers = {}

# -------------------------------------------------
# GIFT DATABASE (CLEAN & SCALABLE)
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
# RECOMMENDATION ENGINE (CLEAN & SMART)
# -------------------------------------------------
def generate_recommendation(answers):
    matches = []

    for gift in GIFTS:
        if (
            gift["budget"] == answers["budget"]
            and gift["style"] == answers["style"]
            and gift["type"] == answers["type"]
            and answers["occasion"] in gift["occasions"]
            and answers["recipient"] in gift["recipients"]
        ):
            matches.append(gift)

    # If we found a perfect match
    if matches:
        gift = matches[0]
        return gift["name"], gift["reason"]

    # Fallback logic (partial matches)
    for gift in GIFTS:
        if gift["budget"] == answers["budget"]:
            return gift["name"], "This option fits your budget and overall preferences."

    return "Personalized Gift Card", "A flexible choice when preferences vary."

# -------------------------------------------------
# LANDING SCREEN
# -------------------------------------------------
def landing_screen():
    st.markdown("<h1 style='text-align:center;'>Find the Perfect Personalized Gift 🎁</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>Answer a few questions. Get matched in under 2 minutes.</p>", unsafe_allow_html=True)

    if st.button("🎁 Find a Personalized Gift", use_container_width=True):
        st.session_state.page = "chat"

# -------------------------------------------------
# QUESTION FLOW
# -------------------------------------------------
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
        ["Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"]
    )

    if st.button("Get Recommendation", use_container_width=True):
        st.session_state.page = "result"

# -------------------------------------------------
# RESULT SCREEN
# -------------------------------------------------
def result_screen():
    product, reason = generate_recommendation(st.session_state.answers)

    st.header("🎉 Your Personalized Gift Recommendation")
    st.subheader(product)
    st.write(reason)

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
