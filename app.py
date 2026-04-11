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

.gift-card {
    background: #FBF8F3;
    border-radius: 14px;
    padding: 24px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    margin-bottom: 16px;
    border-left: 4px solid #3A2F2F;
}

.tag {
    display: inline-block;
    background-color: #3A2F2F;
    color: #FBF8F3;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 13px;
    margin: 4px 2px;
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
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

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

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎁 Find a Gift", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
    with col2:
        if st.button("❤️ My Wishlist", use_container_width=True):
            st.session_state.page = "wishlist"
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
        ["-- Select --", "Partner", "Friend", "Parent", "Sibling", "Colleague", "Pet", "Self"]
    )

    a["closeness"] = st.selectbox(
        "How close are you to them?",
        ["-- Select --", "Very close", "Close friend", "Acquaintance", "Formal / Professional"]
    )

    a["age_group"] = st.selectbox(
        "What is their age group?",
        ["-- Select --", "Kid (under 12)", "Teen (13–17)", "Young Adult (18–30)", "Adult (31–50)", "Senior (50+)"]
    )

    a["occasion"] = st.selectbox(
        "What's the occasion?",
        ["-- Select --", "Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Graduation", "Housewarming", "Just because", "Other"]
    )

    a["budget"] = st.selectbox(
        "Your budget range?",
        ["-- Select --", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000–₹5000", "₹5000+"]
    )

    a["delivery"] = st.selectbox(
        "How do you want to give it?",
        ["-- Select --", "Physical gift", "Digital / Online", "Experience / Activity"]
    )

    a["type"] = st.selectbox(
        "What kind of gift feels right?",
        ["-- Select --", "Decorative", "Usable", "Emotional", "Fun / Playful", "Educational"]
    )

    a["style"] = st.selectbox(
        "Preferred style?",
        ["-- Select --", "Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"]
    )

    # BOOLEAN CHECK
    all_answered = all(
        v != "-- Select --" and v != "" and v is not None
        for v in [
            a.get("recipient"), a.get("closeness"), a.get("age_group"),
            a.get("occasion"), a.get("budget"), a.get("delivery"),
            a.get("type"), a.get("style")
        ]
    )

    if not all_answered:
        st.warning("⚠️ Please answer all questions to continue.")

    if st.button("Get Recommendations ✨", use_container_width=True, disabled=not all_answered):
        st.session_state.page = "result"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# RECOMMENDATION LOGIC — returns list of dicts
# -------------------------------------------------
def generate_recommendations(a):
    budget   = a.get("budget")
    style    = a.get("style")
    occasion = a.get("occasion")
    recipient= a.get("recipient")
    age      = a.get("age_group")
    delivery = a.get("delivery")
    closeness= a.get("closeness")
    gtype    = a.get("type")

    all_gifts = [
        # Physical / Usable
        {"name": "Minimal Ceramic Mug", "reason": "Simple, useful, and clutter-free.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=minimal+ceramic+mug", "amazon": "https://www.amazon.in/s?k=minimal+ceramic+mug"},
        {"name": "Single Photo Print", "reason": "A small but meaningful memory.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=photo+print", "amazon": "https://www.amazon.in/s?k=photo+print"},
        {"name": "Cute Keychain or Mini Plush", "reason": "Fun, light, and affordable.", "price": "under ₹500", "style": "Cute", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=cute+keychain", "amazon": "https://www.amazon.in/s?k=cute+keychain"},
        {"name": "Incense Sticks + Holder", "reason": "Culturally meaningful and calming.", "price": "under ₹500", "style": "Traditional", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=incense+sticks+holder", "amazon": "https://www.amazon.in/s?k=incense+sticks+holder"},
        {"name": "Framed Minimal Photo Print", "reason": "Clean design with emotional value.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=framed+photo+print", "amazon": "https://www.amazon.in/s?k=framed+photo+print"},
        {"name": "Abstract Art Print", "reason": "Adds personality without being loud.", "price": "₹500–₹1000", "style": "Artistic", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=abstract+art+print", "amazon": "https://www.amazon.in/s?k=abstract+art+print"},
        {"name": "Scented Candle Set", "reason": "Relaxing and universally loved.", "price": "₹500–₹1000", "style": "Luxury", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=scented+candle+set", "amazon": "https://www.amazon.in/s?k=scented+candle+set"},
        {"name": "Personalized Photo Frame Set", "reason": "Romantic and premium.", "price": "₹1000–₹2000", "style": "Luxury", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=personalized+photo+frame", "amazon": "https://www.amazon.in/s?k=personalized+photo+frame"},
        {"name": "Handmade Jewellery Box", "reason": "Elegant and personal.", "price": "₹1000–₹2000", "style": "Vintage", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=handmade+jewellery+box", "amazon": "https://www.amazon.in/s?k=handmade+jewellery+box"},
        {"name": "Customized Gift Box", "reason": "High-end, curated experience.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=customized+gift+box", "amazon": "https://www.amazon.in/s?k=customized+gift+box"},
        {"name": "Leather Wallet", "reason": "Classic and practical for any adult.", "price": "₹1000–₹2000", "style": "Modern", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=leather+wallet", "amazon": "https://www.amazon.in/s?k=leather+wallet"},
        {"name": "Bohemian Wind Chime", "reason": "Adds charm and positive energy.", "price": "₹500–₹1000", "style": "Bohemian", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=bohemian+wind+chime", "amazon": "https://www.amazon.in/s?k=bohemian+wind+chime"},
        {"name": "Rustic Wooden Photo Frame", "reason": "Warm, timeless, and personal.", "price": "₹500–₹1000", "style": "Rustic", "delivery": "Physical gift", "flipkart": "https://www.flipkart.com/search?q=rustic+wooden+photo+frame", "amazon": "https://www.amazon.in/s?k=rustic+wooden+photo+frame"},
        # Digital
        {"name": "Netflix / OTT Gift Card", "reason": "Entertainment they'll actually use.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Digital / Online", "flipkart": "https://www.flipkart.com/search?q=netflix+gift+card", "amazon": "https://www.amazon.in/s?k=netflix+gift+card"},
        {"name": "Online Course Voucher", "reason": "A gift that keeps giving — knowledge.", "price": "₹1000–₹2000", "style": "Minimal", "delivery": "Digital / Online", "flipkart": "https://www.flipkart.com/search?q=online+course+voucher", "amazon": "https://www.amazon.in/s?k=udemy+gift+card"},
        {"name": "Spotify Premium Gift Card", "reason": "Music for every mood.", "price": "under ₹500", "style": "Modern", "delivery": "Digital / Online", "flipkart": "https://www.flipkart.com/search?q=spotify+gift+card", "amazon": "https://www.amazon.in/s?k=spotify+gift+card"},
        {"name": "Amazon Gift Card", "reason": "They pick exactly what they want.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Digital / Online", "flipkart": "https://www.flipkart.com/search?q=amazon+gift+card", "amazon": "https://www.amazon.in/s?k=amazon+gift+card"},
        # Experience
        {"name": "Spa / Wellness Voucher", "reason": "A relaxing experience they deserve.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Experience / Activity", "flipkart": "https://www.flipkart.com/search?q=spa+voucher", "amazon": "https://www.amazon.in/s?k=spa+gift+voucher"},
        {"name": "Movie Date Night Voucher", "reason": "Create a memory, not just a thing.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Experience / Activity", "flipkart": "https://www.flipkart.com/search?q=movie+voucher", "amazon": "https://www.amazon.in/s?k=bookmyshow+gift+card"},
        {"name": "Cooking / Art Class Voucher", "reason": "Fun, skill-building, and memorable.", "price": "₹1000–₹2000", "style": "Artistic", "delivery": "Experience / Activity", "flipkart": "https://www.flipkart.com/search?q=cooking+class+voucher", "amazon": "https://www.amazon.in/s?k=art+class+gift+voucher"},
    ]

    # Filter by budget and delivery type first
    filtered = [g for g in all_gifts if g["price"] == budget and g["delivery"] == delivery]

    # Then try to match style
    style_match = [g for g in filtered if g["style"] == style]

    # Return style matches if found, otherwise return all filtered, limit to 3
    results = style_match if style_match else filtered
    return results[:3] if results else [
        {"name": "Personalized Gift Card", "reason": "A flexible choice when preferences vary.", "price": budget, "style": style, "delivery": delivery, "flipkart": "https://www.flipkart.com/search?q=gift+card", "amazon": "https://www.amazon.in/s?k=gift+card"}
    ]

# -------------------------------------------------
# RESULT SCREEN
# -------------------------------------------------
def result_screen():
    a = st.session_state.answers
    recommendations = generate_recommendations(a)

    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:48px;">🎁</div>
        <h2>Your Gift Recommendations</h2>
        <p>Based on your answers, here are the best matches:</p>
    </div>
    """, unsafe_allow_html=True)

    for i, gift in enumerate(recommendations):
        st.markdown(f"""
        <div class="gift-card">
            <h3 style="text-align:left; margin-bottom:8px;">🎀 {gift['name']}</h3>
            <p style="margin-bottom:10px;">{gift['reason']}</p>
            <span class="tag">💰 {gift['price']}</span>
            <span class="tag">🎨 {gift['style']}</span>
            <span class="tag">📦 {gift['delivery']}</span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.link_button("🛒 Amazon", gift["amazon"], use_container_width=True)
        with col2:
            st.link_button("🛍️ Flipkart", gift["flipkart"], use_container_width=True)
        with col3:
            if st.button(f"❤️ Save", key=f"save_{i}", use_container_width=True):
                if gift["name"] not in [w["name"] for w in st.session_state.wishlist]:
                    st.session_state.wishlist.append(gift)
                    st.success(f"Added to wishlist!")
                else:
                    st.info("Already in wishlist!")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.page = "landing"
            st.session_state.answers = {}
            st.rerun()
    with col2:
        if st.button("❤️ View Wishlist", use_container_width=True):
            st.session_state.page = "wishlist"
            st.rerun()

# -------------------------------------------------
# WISHLIST SCREEN
# -------------------------------------------------
def wishlist_screen():
    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:48px;">❤️</div>
        <h2>My Wishlist</h2>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.wishlist:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <p>Your wishlist is empty. Find some gifts first! 🎁</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, gift in enumerate(st.session_state.wishlist):
            st.markdown(f"""
            <div class="gift-card">
                <h3 style="text-align:left; margin-bottom:8px;">🎀 {gift['name']}</h3>
                <p style="margin-bottom:10px;">{gift['reason']}</p>
                <span class="tag">💰 {gift['price']}</span>
                <span class="tag">🎨 {gift['style']}</span>
                <span class="tag">📦 {gift['delivery']}</span>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🛒 Amazon", gift["amazon"], use_container_width=True)
            with col2:
                st.link_button("🛍️ Flipkart", gift["flipkart"], use_container_width=True)
            with col3:
                if st.button(f"🗑️ Remove", key=f"remove_{i}", use_container_width=True):
                    st.session_state.wishlist.pop(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Home", use_container_width=True):
        st.session_state.page = "landing"
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
elif st.session_state.page == "wishlist":
    wishlist_screen()
