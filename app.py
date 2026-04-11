import streamlit as st
import time
import requests
import json

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
}

.ai-badge {
    display: inline-block;
    background: #1C1510;
    color: #FDFAF5 !important;
    border-radius: 30px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 16px;
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

.why-box {
    background: #F9F6F0;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 10px;
    font-size: 13px;
    color: #7A6A5E !important;
    line-height: 1.6;
    border-left: 3px solid #C9B99A;
}

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

.stButton > button:disabled {
    background-color: #D6CEBF !important;
    color: #A89880 !important;
    cursor: not-allowed !important;
    transform: none !important;
}

.stSelectbox label, .stTextInput label, .stTextArea label {
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
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #F9F6F0 !important;
    border: 1.5px solid #EDE8DF !important;
    border-radius: 12px !important;
    color: #1C1510 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stAlert {
    border-radius: 12px !important;
    border: none !important;
    background: #FDF3E3 !important;
    color: #7A5C2E !important;
}

.stLinkButton > a {
    background-color: #F3EEE6 !important;
    color: #1C1510 !important;
    border-radius: 50px !important;
    padding: 0.55rem 1rem !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: none !important;
    text-decoration: none !important;
}

.stLinkButton > a:hover {
    background-color: #E8E0D3 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──
for key, default in {
    "page": "loading",
    "loaded": False,
    "answers": {},
    "wishlist": [],
    "recommendations": [],
    "api_key": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Claude API Call ──
def get_ai_recommendations(a, api_key):
    prompt = f"""You are a thoughtful gift curator. Based on the details below, suggest exactly 3 unique, specific gift ideas.

Recipient: {a['recipient']}
Closeness: {a['closeness']}
Age Group: {a['age_group']}
Occasion: {a['occasion']}
Budget: {a['budget']}
Delivery: {a['delivery']}
Gift Type: {a['type']}
Style: {a['style']}
Personal Note: {a.get('note', 'None provided')}

Respond ONLY with a valid JSON array. No explanation, no markdown, no backticks. Example format:
[
  {{
    "name": "Gift Name",
    "reason": "One sentence why this is perfect for them.",
    "why": "Two sentences of deeper reasoning — what makes this special for this specific person and occasion.",
    "search_query": "short search query for amazon"
  }}
]

Rules:
- Be specific and creative, not generic
- Match the budget {a['budget']} strictly
- Match the delivery type: {a['delivery']}
- Consider the personal note if provided
- Keep reason under 15 words
- Keep why under 30 words"""

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data = response.json()
    text = data["content"][0]["text"].strip()
    gifts = json.loads(text)

    for g in gifts:
        q = g["search_query"].replace(" ", "+")
        g["amazon"] = f"https://www.amazon.in/s?k={q}"
        g["flipkart"] = f"https://www.flipkart.com/search?q={q}"
        g["price"] = a["budget"]
        g["style"] = a["style"]
        g["delivery"] = a["delivery"]

    return gifts

# ── Loading ──
def loading_screen():
    if not st.session_state.loaded:
        st.markdown("""
        <div class="card" style="text-align:center; padding:60px 44px;">
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
    <div class="card" style="text-align:center; padding:56px 44px;">
        <span class="hero-emoji">🎁</span>
        <h1 style="font-size:2rem; margin-bottom:12px;">Find the perfect gift</h1>
        <p style="color:#A89880; font-size:16px; line-height:1.7; max-width:380px; margin:0 auto 8px;">
            Answer a few questions and get AI-powered gift recommendations — instantly.
        </p>
        <div class="ai-badge">✦ Powered by Claude AI</div>
    </div>
    """, unsafe_allow_html=True)

    # API Key input
    with st.expander("🔑 Enter your Anthropic API Key"):
        st.session_state.api_key = st.text_input(
            "API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="sk-ant-...",
            label_visibility="collapsed"
        )
        st.markdown("<p style='font-size:12px; color:#A89880;'>Get your key at console.anthropic.com — it's never stored.</p>", unsafe_allow_html=True)

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
    <div class="step-label">Tell us about the gift</div>
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
    st.markdown("<h2 style='margin-bottom:24px;'>Occasion & budget</h2>", unsafe_allow_html=True)

    a["occasion"] = st.selectbox("Occasion", ["— select —", "Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Graduation", "Housewarming", "Just because", "Other"])
    a["budget"] = st.selectbox("Budget", ["— select —", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000–₹5000", "₹5000+"])
    a["delivery"] = st.selectbox("How to give it?", ["— select —", "Physical gift", "Digital / Online", "Experience / Activity"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Style & vibe</h2>", unsafe_allow_html=True)

    a["type"] = st.selectbox("Gift type", ["— select —", "Decorative", "Usable", "Emotional", "Fun / Playful", "Educational"])
    a["style"] = st.selectbox("Aesthetic style", ["— select —", "Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:12px;'>Anything extra? (optional)</h2>", unsafe_allow_html=True)
    a["note"] = st.text_area(
        "Personal note",
        placeholder="e.g. She loves hiking and coffee, he's really into chess lately…",
        label_visibility="collapsed",
        height=90
    )

    st.markdown('</div>', unsafe_allow_html=True)

    all_answered = all(a.get(f) and a.get(f) != "— select —" for f in fields)

    if not all_answered:
        st.warning(f"⚑  {len(fields) - filled} question(s) remaining")

    if not st.session_state.api_key:
        st.warning("🔑 Add your Anthropic API key on the home screen to get AI recommendations.")

    col1, col2 = st.columns([2, 1])
    with col1:
        ready = all_answered and bool(st.session_state.api_key)
        if st.button("✦ Get AI Recommendations →", use_container_width=True, disabled=not ready):
            st.session_state.page = "loading_ai"
            st.rerun()
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

# ── AI Loading ──
def ai_loading_screen():
    st.markdown("""
    <div class="card" style="text-align:center; padding:60px 44px;">
        <span class="hero-emoji">✦</span>
        <h2 style="margin-bottom:10px;">Finding your gifts…</h2>
        <p style="color:#A89880; font-size:15px;">Claude is thinking of the perfect matches</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        recs = get_ai_recommendations(st.session_state.answers, st.session_state.api_key)
        st.session_state.recommendations = recs
        st.session_state.page = "result"
        st.rerun()
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
        if st.button("← Try again"):
            st.session_state.page = "chat"
            st.rerun()

# ── Results ──
def result_screen():
    recs = st.session_state.recommendations

    st.markdown("""
    <div style="text-align:center; margin-bottom:28px;">
        <span class="hero-emoji">✦</span>
        <h1 style="margin-bottom:8px;">Your AI matches</h1>
        <p style="color:#A89880; font-size:15px;">Handpicked by Claude just for you</p>
    </div>
    """, unsafe_allow_html=True)

    for i, gift in enumerate(recs):
        st.markdown(f"""
        <div class="card-sm">
            <div class="gift-number">{i+1}</div>
            <h3 style="margin:0 0 6px; font-size:1.15rem;">{gift['name']}</h3>
            <p style="color:#7A6A5E; font-size:14px; margin-bottom:8px; line-height:1.6;">{gift['reason']}</p>
            <div class="why-box">💡 {gift.get('why', '')}</div>
            <div style="margin-top:12px;">
                <span class="tag">💰 {gift['price']}</span>
                <span class="tag">🎨 {gift['style']}</span>
                <span class="tag">📦 {gift['delivery']}</span>
            </div>
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
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("↺ Start over", use_container_width=True):
            st.session_state.page = "landing"
            st.session_state.answers = {}
            st.session_state.recommendations = []
            st.rerun()
    with col2:
        if st.button("✦ Regenerate", use_container_width=True):
            st.session_state.page = "loading_ai"
            st.rerun()
    with col3:
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
            <p style="color:#A89880; font-size:15px;">Nothing saved yet — find some gifts first! 🎁</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, gift in enumerate(st.session_state.wishlist):
            st.markdown(f"""
            <div class="card-sm">
                <h3 style="margin:0 0 6px; font-size:1.1rem;">{gift['name']}</h3>
                <p style="color:#7A6A5E; font-size:14px; margin-bottom:8px;">{gift['reason']}</p>
                {f'<div class="why-box">💡 {gift["why"]}</div>' if gift.get("why") else ""}
                <div style="margin-top:10px;">
                    <span class="tag">💰 {gift['price']}</span>
                    <span class="tag">🎨 {gift['style']}</span>
                </div>
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
elif st.session_state.page == "loading_ai":
    ai_loading_screen()
elif st.session_state.page == "result":
    result_screen()
elif st.session_state.page == "wishlist":
    wishlist_screen()
