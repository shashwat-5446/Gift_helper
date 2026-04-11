import streamlit as st
import time

st.set_page_config(
    page_title="Giftapper",
    page_icon="🎁",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

#MainMenu, footer, header { visibility: hidden; }

html, body, .stApp {
    background-color: #FDFAF5 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container {
    max-width: 680px !important;
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
}

/* ── Typography ── */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #1C1510 !important;
    font-weight: 400 !important;
    letter-spacing: -0.3px;
}

p, li, label, div {
    font-family: 'DM Sans', sans-serif !important;
    color: #4A3F35 !important;
}

/* ── Cards ── */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 40px 44px;
    border: 1px solid #EDE8DF;
    margin-bottom: 20px;
}

.card-sm {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px 28px;
    border: 1px solid #EDE8DF;
    margin-bottom: 14px;
    transition: box-shadow 0.2s ease;
}

.card-sm:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
}

.gift-number {
    display: inline-block;
    background: #1C1510;
    color: #FDFAF5 !important;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    line-height: 28px;
    text-align: center;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 10px;
}

.tag {
    display: inline-block;
    background: #F3EEE6;
    color: #6B5A4E !important;
    border-radius: 30px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px 3px 3px 0;
    letter-spacing: 0.2px;
}

.progress-bar-bg {
    background: #EDE8DF;
    border-radius: 10px;
    height: 4px;
    margin-bottom: 28px;
}

.progress-bar-fill {
    background: #1C1510;
    border-radius: 10px;
    height: 4px;
    transition: width 0.4s ease;
}

.step-label {
    font-size: 12px;
    color: #A89880 !important;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.hero-emoji {
    font-size: 52px;
    margin-bottom: 12px;
    display: block;
}

.divider {
    border: none;
    border-top: 1px solid #EDE8DF;
    margin: 20px 0;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #1C1510 !important;
    color: #FDFAF5 !important;
    border-radius: 50px !important;
    padding: 0.75rem 1.6rem !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    letter-spacing: 0.2px !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

.stButton > button:disabled {
    background-color: #D6CEBF !important;
    color: #A89880 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

/* ── Secondary button ── */
div[data-testid="column"]:last-child .stButton > button,
.btn-secondary .stButton > button {
    background-color: transparent !important;
    color: #1C1510 !important;
    border: 1.5px solid #1C1510 !important;
}

div[data-testid="column"]:last-child .stButton > button:hover {
    background-color: #F3EEE6 !important;
    opacity: 1 !important;
}

/* ── Selects ── */
.stSelectbox label {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #1C1510 !important;
    margin-bottom: 4px !important;
}

.stSelectbox > div > div {
    background-color: #F9F6F0 !important;
    border: 1.5px solid #EDE8DF !important;
    border-radius: 12px !important;
    color: #1C1510 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #1C1510 !important;
}

/* ── Warning ── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
    background: #FDF3E3 !important;
    color: #7A5C2E !important;
}

/* ── Link buttons ── */
.stLinkButton > a {
    background-color: #F3EEE6 !important;
    color: #1C1510 !important;
    border-radius: 50px !important;
    padding: 0.55rem 1rem !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    text-decoration: none !important;
    transition: background 0.2s ease !important;
}

.stLinkButton > a:hover {
    background-color: #E8E0D3 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──
if "page" not in st.session_state:
    st.session_state.page = "loading"
if "loaded" not in st.session_state:
    st.session_state.loaded = False
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []

# ── Loading ──
def loading_screen():
    if not st.session_state.loaded:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 60px 44px;">
            <span class="hero-emoji">🎁</span>
            <h2 style="margin-bottom:10px;">Giftapper</h2>
            <p style="color:#A89880; font-size:15px;">Preparing your gift experience…</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)
        st.session_state.loaded = True
        st.session_state.page = "landing"
        st.rerun()

# ── Landing ──
def landing_screen():
    st.markdown("""
    <div class="card" style="text-align:center; padding: 56px 44px;">
        <span class="hero-emoji">🎁</span>
        <h1 style="font-size:2rem; margin-bottom:12px;">Find the perfect gift</h1>
        <p style="color:#A89880; font-size:16px; line-height:1.7; max-width:380px; margin:0 auto 28px;">
            Answer 8 quick questions and get thoughtfully matched gift ideas — with links to buy instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✦ Find a Gift", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
    with col2:
        if st.button(f"❤ Wishlist ({len(st.session_state.wishlist)})", use_container_width=True):
            st.session_state.page = "wishlist"
            st.rerun()

# ── Chat ──
def chat_screen():
    a = st.session_state.answers

    fields = ["recipient", "closeness", "age_group", "occasion", "budget", "delivery", "type", "style"]
    filled = sum(1 for f in fields if a.get(f) and a.get(f) != "— select —")
    progress = int((filled / len(fields)) * 100)

    st.markdown(f"""
    <div class="step-label">Step 1 of 1 — Tell us about the gift</div>
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{progress}%"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Who is this for?</h2>", unsafe_allow_html=True)

    a["recipient"] = st.selectbox("Recipient", ["— select —", "Partner", "Friend", "Parent", "Sibling", "Colleague", "Pet", "Self"])
    a["closeness"] = st.selectbox("How close are you?", ["— select —", "Very close", "Close friend", "Acquaintance", "Formal / Professional"])
    a["age_group"] = st.selectbox("Their age group", ["— select —", "Kid (under 12)", "Teen (13–17)", "Young Adult (18–30)", "Adult (31–50)", "Senior (50+)"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>The occasion & budget</h2>", unsafe_allow_html=True)

    a["occasion"] = st.selectbox("Occasion", ["— select —", "Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Graduation", "Housewarming", "Just because", "Other"])
    a["budget"] = st.selectbox("Budget", ["— select —", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000–₹5000", "₹5000+"])
    a["delivery"] = st.selectbox("How to give it?", ["— select —", "Physical gift", "Digital / Online", "Experience / Activity"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Style & vibe</h2>", unsafe_allow_html=True)

    a["type"] = st.selectbox("Gift type", ["— select —", "Decorative", "Usable", "Emotional", "Fun / Playful", "Educational"])
    a["style"] = st.selectbox("Aesthetic style", ["— select —", "Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"])

    st.markdown('</div>', unsafe_allow_html=True)

    all_answered = all(
        a.get(f) and a.get(f) != "— select —"
        for f in fields
    )

    if not all_answered:
        st.warning(f"⚑  {len(fields) - filled} question(s) remaining")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Get Recommendations →", use_container_width=True, disabled=not all_answered):
            st.session_state.page = "result"
            st.rerun()
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

# ── Recommendations ──
def generate_recommendations(a):
    budget = a.get("budget")
    style  = a.get("style")
    delivery = a.get("delivery")

    all_gifts = [
        {"name": "Minimal Ceramic Mug", "reason": "Simple, useful, clutter-free — a daily reminder.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=minimal+ceramic+mug", "flipkart": "https://www.flipkart.com/search?q=minimal+ceramic+mug"},
        {"name": "Single Photo Print", "reason": "A small but deeply meaningful keepsake.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=photo+print", "flipkart": "https://www.flipkart.com/search?q=photo+print"},
        {"name": "Cute Keychain / Mini Plush", "reason": "Fun, light, and always affordable.", "price": "under ₹500", "style": "Cute", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=cute+keychain", "flipkart": "https://www.flipkart.com/search?q=cute+keychain"},
        {"name": "Incense Sticks + Holder", "reason": "Culturally rooted and calming.", "price": "under ₹500", "style": "Traditional", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=incense+sticks+holder", "flipkart": "https://www.flipkart.com/search?q=incense+holder"},
        {"name": "Spotify Premium Gift Card", "reason": "Music for every mood, delivered instantly.", "price": "under ₹500", "style": "Modern", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=spotify+gift+card", "flipkart": "https://www.flipkart.com/search?q=spotify+gift+card"},
        {"name": "Framed Minimal Photo Print", "reason": "Clean design with deep emotional value.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=framed+photo+print", "flipkart": "https://www.flipkart.com/search?q=framed+photo+print"},
        {"name": "Abstract Art Print", "reason": "Adds personality without being loud.", "price": "₹500–₹1000", "style": "Artistic", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=abstract+art+print", "flipkart": "https://www.flipkart.com/search?q=abstract+art+print"},
        {"name": "Scented Candle Set", "reason": "Universally loved, instantly relaxing.", "price": "₹500–₹1000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=scented+candle+set", "flipkart": "https://www.flipkart.com/search?q=scented+candle+set"},
        {"name": "Bohemian Wind Chime", "reason": "Adds charm and positive energy to any space.", "price": "₹500–₹1000", "style": "Bohemian", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=wind+chime", "flipkart": "https://www.flipkart.com/search?q=wind+chime"},
        {"name": "Rustic Wooden Photo Frame", "reason": "Warm, timeless, and personal.", "price": "₹500–₹1000", "style": "Rustic", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=wooden+photo+frame", "flipkart": "https://www.flipkart.com/search?q=wooden+photo+frame"},
        {"name": "Netflix / OTT Gift Card", "reason": "Entertainment they'll genuinely use.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=ott+gift+card", "flipkart": "https://www.flipkart.com/search?q=netflix+gift+card"},
        {"name": "Amazon Gift Card", "reason": "They choose exactly what they want.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=amazon+gift+card", "flipkart": "https://www.flipkart.com/search?q=amazon+gift+card"},
        {"name": "Movie Date Night Voucher", "reason": "Create a memory, not just a thing.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=bookmyshow+gift+card", "flipkart": "https://www.flipkart.com/search?q=movie+voucher"},
        {"name": "Personalized Photo Frame Set", "reason": "Romantic, premium, and lasting.", "price": "₹1000–₹2000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=personalized+photo+frame", "flipkart": "https://www.flipkart.com/search?q=personalized+photo+frame"},
        {"name": "Handmade Jewellery Box", "reason": "Elegant, personal, and heirloom-worthy.", "price": "₹1000–₹2000", "style": "Vintage", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=jewellery+box", "flipkart": "https://www.flipkart.com/search?q=jewellery+box"},
        {"name": "Leather Wallet", "reason": "Classic, practical, and long-lasting.", "price": "₹1000–₹2000", "style": "Modern", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=leather+wallet", "flipkart": "https://www.flipkart.com/search?q=leather+wallet"},
        {"name": "Online Course Voucher", "reason": "A gift that compounds — knowledge.", "price": "₹1000–₹2000", "style": "Minimal", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=udemy+gift+card", "flipkart": "https://www.flipkart.com/search?q=online+course+voucher"},
        {"name": "Cooking / Art Class Voucher", "reason": "Fun, skill-building, unforgettable.", "price": "₹1000–₹2000", "style": "Artistic", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=art+class+voucher", "flipkart": "https://www.flipkart.com/search?q=cooking+class+voucher"},
        {"name": "Customized Gift Box", "reason": "High-end, curated, and completely personal.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=customized+gift+box", "flipkart": "https://www.flipkart.com/search?q=customized+gift+box"},
        {"name": "Spa / Wellness Voucher", "reason": "The gift of rest — truly luxurious.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=spa+gift+voucher", "flipkart": "https://www.flipkart.com/search?q=spa+voucher"},
        {"name": "Premium Watch", "reason": "Timeless, sophisticated, and memorable.", "price": "₹5000+", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=premium+watch+gift", "flipkart": "https://www.flipkart.com/search?q=premium+watch"},
        {"name": "Personalized Jewellery", "reason": "Wearable, deeply personal, forever meaningful.", "price": "₹5000+", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=personalized+jewellery", "flipkart": "https://www.flipkart.com/search?q=personalized+jewellery"},
    ]

    filtered = [g for g in all_gifts if g["price"] == budget and g["delivery"] == delivery]
    style_match = [g for g in filtered if g["style"] == style]
    results = style_match if style_match else filtered

    return results[:3] if results else [
        {"name": "Personalized Gift Card", "reason": "A flexible, thoughtful choice.", "price": budget, "style": style, "delivery": delivery, "amazon": "https://www.amazon.in/s?k=gift+card", "flipkart": "https://www.flipkart.com/search?q=gift+card"}
    ]

# ── Results ──
def result_screen():
    a = st.session_state.answers
    recs = generate_recommendations(a)

    st.markdown("""
    <div style="text-align:center; margin-bottom:28px;">
        <span class="hero-emoji">✦</span>
        <h1 style="margin-bottom:8px;">Your matches</h1>
        <p style="color:#A89880; font-size:15px;">Curated just for your answers</p>
    </div>
    """, unsafe_allow_html=True)

    for i, gift in enumerate(recs):
        st.markdown(f"""
        <div class="card-sm">
            <div class="gift-number">{i+1}</div>
            <h3 style="margin: 0 0 6px; font-size:1.15rem;">{gift['name']}</h3>
            <p style="color:#7A6A5E; font-size:14px; margin-bottom:12px; line-height:1.6;">{gift['reason']}</p>
            <span class="tag">💰 {gift['price']}</span>
            <span class="tag">🎨 {gift['style']}</span>
            <span class="tag">📦 {gift['delivery']}</span>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.link_button("🛒 Amazon", gift["amazon"], use_container_width=True)
        with col2:
            st.link_button("🛍 Flipkart", gift["flipkart"], use_container_width=True)
        with col3:
            already_saved = gift["name"] in [w["name"] for w in st.session_state.wishlist]
            label = "✓ Saved" if already_saved else "❤ Save"
            if st.button(label, key=f"save_{i}", use_container_width=True, disabled=already_saved):
                st.session_state.wishlist.append(gift)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Start over", use_container_width=True):
            st.session_state.page = "landing"
            st.session_state.answers = {}
            st.rerun()
    with col2:
        if st.button(f"❤ Wishlist ({len(st.session_state.wishlist)})", use_container_width=True):
            st.session_state.page = "wishlist"
            st.rerun()

# ── Wishlist ──
def wishlist_screen():
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:28px;">
        <span class="hero-emoji">❤</span>
        <h1 style="margin-bottom:8px;">My Wishlist</h1>
        <p style="color:#A89880; font-size:15px;">{len(st.session_state.wishlist)} saved gift(s)</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.wishlist:
        st.markdown("""
        <div class="card" style="text-align:center; padding:48px;">
            <p style="color:#A89880; font-size:15px;">Nothing saved yet — go find some gifts! 🎁</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, gift in enumerate(st.session_state.wishlist):
            st.markdown(f"""
            <div class="card-sm">
                <h3 style="margin: 0 0 6px; font-size:1.1rem;">{gift['name']}</h3>
                <p style="color:#7A6A5E; font-size:14px; margin-bottom:10px;">{gift['reason']}</p>
                <span class="tag">💰 {gift['price']}</span>
                <span class="tag">🎨 {gift['style']}</span>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.link_button("🛒 Amazon", gift["amazon"], use_container_width=True)
            with col2:
                st.link_button("🛍 Flipkart", gift["flipkart"], use_container_width=True)
            with col3:
                if st.button("🗑 Remove", key=f"remove_{i}", use_container_width=True):
                    st.session_state.wishlist.pop(i)
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        if st.button("✦ Find more gifts", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ── Router ──
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
