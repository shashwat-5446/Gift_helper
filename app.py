import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Personalized Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# -----------------------------
# Session State Init
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

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
# SIMPLE RECOMMENDATION LOGIC
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
