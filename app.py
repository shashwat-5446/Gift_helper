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

/* Confetti canvas fixed overlay */
#confetti-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# ── Confetti Script ──
CONFETTI_JS = """
<canvas id="confetti-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const colors = ['#1C1510','#C9B99A','#F3EEE6','#E8C47A','#D4956A','#A0C878','#7AB8D4','#D47AB0'];
    const pieces = [];
    const count = 160;

    for (let i = 0; i < count; i++) {
        pieces.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height - canvas.height,
            w: Math.random() * 10 + 5,
            h: Math.random() * 6 + 3,
            color: colors[Math.floor(Math.random() * colors.length)],
            speed: Math.random() * 4 + 2,
            angle: Math.random() * 360,
            spin: (Math.random() - 0.5) * 6,
            drift: (Math.random() - 0.5) * 1.5,
            opacity: 1
        });
    }

    let frame = 0;
    const maxFrames = 200;

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        frame++;

        pieces.forEach(p => {
            p.y += p.speed;
            p.x += p.drift;
            p.angle += p.spin;
            if (frame > 120) p.opacity -= 0.015;

            ctx.save();
            ctx.globalAlpha = Math.max(0, p.opacity);
            ctx.translate(p.x + p.w / 2, p.y + p.h / 2);
            ctx.rotate((p.angle * Math.PI) / 180);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
            ctx.restore();
        });

        if (frame < maxFrames) {
            requestAnimationFrame(draw);
        } else {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
    }

    draw();
})();
</script>
"""

# ── Session State ──
for key, default in {
    "page": "loading",
    "loaded": False,
    "answers": {},
    "wishlist": [],
    "recommendations": [],
    "show_confetti": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Recommendation Logic (no API key needed) ──
def generate_recommendations(a):
    budget   = a.get("budget")
    style    = a.get("style")
    delivery = a.get("delivery")

    all_gifts = [
        {"name": "Minimal Ceramic Mug", "reason": "Simple, useful, clutter-free — a daily reminder.", "why": "Perfect for someone who appreciates understated beauty in everyday objects.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=minimal+ceramic+mug", "flipkart": "https://www.flipkart.com/search?q=minimal+ceramic+mug"},
        {"name": "Single Photo Print", "reason": "A small but deeply meaningful keepsake.", "why": "Turns a shared memory into something they can see every day.", "price": "under ₹500", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=photo+print", "flipkart": "https://www.flipkart.com/search?q=photo+print"},
        {"name": "Cute Keychain / Mini Plush", "reason": "Fun, light, and always affordable.", "why": "A little smile every time they reach for their keys.", "price": "under ₹500", "style": "Cute", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=cute+keychain", "flipkart": "https://www.flipkart.com/search?q=cute+keychain"},
        {"name": "Incense Sticks + Holder", "reason": "Culturally rooted and calming.", "why": "A sensory gift that transforms any space into a sanctuary.", "price": "under ₹500", "style": "Traditional", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=incense+sticks+holder", "flipkart": "https://www.flipkart.com/search?q=incense+holder"},
        {"name": "Spotify Premium Gift Card", "reason": "Music for every mood, delivered instantly.", "why": "Unlocks a world of music with zero friction — always useful.", "price": "under ₹500", "style": "Modern", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=spotify+gift+card", "flipkart": "https://www.flipkart.com/search?q=spotify+gift+card"},
        {"name": "Framed Minimal Photo Print", "reason": "Clean design with deep emotional value.", "why": "A memory they can hang on their wall and see every morning.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=framed+photo+print", "flipkart": "https://www.flipkart.com/search?q=framed+photo+print"},
        {"name": "Abstract Art Print", "reason": "Adds personality without being loud.", "why": "A conversation starter that reflects their artistic soul.", "price": "₹500–₹1000", "style": "Artistic", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=abstract+art+print", "flipkart": "https://www.flipkart.com/search?q=abstract+art+print"},
        {"name": "Scented Candle Set", "reason": "Universally loved, instantly relaxing.", "why": "Turns any evening into a luxurious ritual.", "price": "₹500–₹1000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=scented+candle+set", "flipkart": "https://www.flipkart.com/search?q=scented+candle+set"},
        {"name": "Bohemian Wind Chime", "reason": "Adds charm and positive energy.", "why": "A free-spirited gift that sings with the breeze.", "price": "₹500–₹1000", "style": "Bohemian", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=wind+chime", "flipkart": "https://www.flipkart.com/search?q=wind+chime"},
        {"name": "Rustic Wooden Photo Frame", "reason": "Warm, timeless, and personal.", "why": "Natural wood grain makes every photo feel like a heirloom.", "price": "₹500–₹1000", "style": "Rustic", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=wooden+photo+frame", "flipkart": "https://www.flipkart.com/search?q=wooden+photo+frame"},
        {"name": "Netflix / OTT Gift Card", "reason": "Entertainment they'll genuinely use.", "why": "Weeks of movies and shows — the gift that keeps giving.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=ott+gift+card", "flipkart": "https://www.flipkart.com/search?q=netflix+gift+card"},
        {"name": "Amazon Gift Card", "reason": "They choose exactly what they want.", "why": "The most honest gift — total freedom to pick their perfect thing.", "price": "₹500–₹1000", "style": "Minimal", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=amazon+gift+card", "flipkart": "https://www.flipkart.com/search?q=amazon+gift+card"},
        {"name": "Movie Date Night Voucher", "reason": "Create a memory, not just a thing.", "why": "An experience you share together — more valuable than any object.", "price": "₹500–₹1000", "style": "Modern", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=bookmyshow+gift+card", "flipkart": "https://www.flipkart.com/search?q=movie+voucher"},
        {"name": "Personalized Photo Frame Set", "reason": "Romantic, premium, and lasting.", "why": "Multiple frames tell a story — your story, beautifully displayed.", "price": "₹1000–₹2000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=personalized+photo+frame", "flipkart": "https://www.flipkart.com/search?q=personalized+photo+frame"},
        {"name": "Handmade Jewellery Box", "reason": "Elegant, personal, and heirloom-worthy.", "why": "Every piece of jewellery they own gets a beautiful new home.", "price": "₹1000–₹2000", "style": "Vintage", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=jewellery+box", "flipkart": "https://www.flipkart.com/search?q=jewellery+box"},
        {"name": "Leather Wallet", "reason": "Classic, practical, and long-lasting.", "why": "Something they use every single day — and think of you every time.", "price": "₹1000–₹2000", "style": "Modern", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=leather+wallet", "flipkart": "https://www.flipkart.com/search?q=leather+wallet"},
        {"name": "Online Course Voucher", "reason": "A gift that compounds — knowledge.", "why": "Invest in their passion or career — a truly thoughtful gesture.", "price": "₹1000–₹2000", "style": "Minimal", "delivery": "Digital / Online", "amazon": "https://www.amazon.in/s?k=udemy+gift+card", "flipkart": "https://www.flipkart.com/search?q=online+course+voucher"},
        {"name": "Cooking / Art Class Voucher", "reason": "Fun, skill-building, unforgettable.", "why": "They walk away with a new skill and a story to tell.", "price": "₹1000–₹2000", "style": "Artistic", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=art+class+voucher", "flipkart": "https://www.flipkart.com/search?q=cooking+class+voucher"},
        {"name": "Customized Gift Box", "reason": "High-end, curated, and completely personal.", "why": "A full unboxing experience — every item chosen with love.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=customized+gift+box", "flipkart": "https://www.flipkart.com/search?q=customized+gift+box"},
        {"name": "Spa / Wellness Voucher", "reason": "The gift of rest — truly luxurious.", "why": "Everyone deserves a day of pure pampering — this makes it happen.", "price": "₹2000–₹5000", "style": "Luxury", "delivery": "Experience / Activity", "amazon": "https://www.amazon.in/s?k=spa+gift+voucher", "flipkart": "https://www.flipkart.com/search?q=spa+voucher"},
        {"name": "Premium Watch", "reason": "Timeless, sophisticated, and memorable.", "why": "A statement piece they'll wear for decades and always treasure.", "price": "₹5000+", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=premium+watch+gift", "flipkart": "https://www.flipkart.com/search?q=premium+watch"},
        {"name": "Personalized Jewellery", "reason": "Wearable, deeply personal, forever meaningful.", "why": "Their name, date, or symbol — carried with them always.", "price": "₹5000+", "style": "Luxury", "delivery": "Physical gift", "amazon": "https://www.amazon.in/s?k=personalized+jewellery", "flipkart": "https://www.flipkart.com/search?q=personalized+jewellery"},
    ]

    filtered = [g for g in all_gifts if g["price"] == budget and g["delivery"] == delivery]
    style_match = [g for g in filtered if g["style"] == style]
    results = style_match if style_match else filtered

    return results[:3] if results else [
        {"name": "Personalized Gift Card", "reason": "A flexible, thoughtful choice.", "why": "When in doubt, let them choose — it's always the right call.", "price": budget, "style": style, "delivery": delivery, "amazon": "https://www.amazon.in/s?k=gift+card", "flipkart": "https://www.flipkart.com/search?q=gift+card"}
    ]

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
            Answer a few questions and get thoughtfully matched gift ideas — with links to buy instantly.
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
    <div class="step-label">Tell us about the gift</div>
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{progress}%"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Who is this for?</h2>", unsafe_allow_html=True)

    a["recipient"] = st.selectbox("Recipient", ["— select —", "Partner", "Friend", "Parent", "Sibling", "Colleague", "Pet", "Self"])
    a["closeness"]  = st.selectbox("How close are you?", ["— select —", "Very close", "Close friend", "Acquaintance", "Formal / Professional"])
    a["age_group"]  = st.selectbox("Their age group", ["— select —", "Kid (under 12)", "Teen (13–17)", "Young Adult (18–30)", "Adult (31–50)", "Senior (50+)"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Occasion & budget</h2>", unsafe_allow_html=True)

    a["occasion"] = st.selectbox("Occasion", ["— select —", "Birthday", "Anniversary", "Memory / Keepsake", "Festival", "Graduation", "Housewarming", "Just because", "Other"])
    a["budget"]   = st.selectbox("Budget", ["— select —", "under ₹500", "₹500–₹1000", "₹1000–₹2000", "₹2000–₹5000", "₹5000+"])
    a["delivery"] = st.selectbox("How to give it?", ["— select —", "Physical gift", "Digital / Online", "Experience / Activity"])

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin-bottom:24px;'>Style & vibe</h2>", unsafe_allow_html=True)

    a["type"]  = st.selectbox("Gift type", ["— select —", "Decorative", "Usable", "Emotional", "Fun / Playful", "Educational"])
    a["style"] = st.selectbox("Aesthetic style", ["— select —", "Minimal", "Artistic", "Cute", "Luxury", "Modern", "Vintage", "Bohemian", "Rustic", "Traditional"])

    st.markdown('</div>', unsafe_allow_html=True)

    all_answered = all(a.get(f) and a.get(f) != "— select —" for f in fields)

    if not all_answered:
        st.warning(f"⚑  {len(fields) - filled} question(s) remaining")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Get Recommendations →", use_container_width=True, disabled=not all_answered):
            st.session_state.recommendations = generate_recommendations(a)
            st.session_state.show_confetti = True  # 🎉 trigger confetti
            st.session_state.page = "result"
            st.rerun()
    with col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

# ── Results ──
def result_screen():
    recs = st.session_state.recommendations

    # 🎉 Fire confetti once when results first appear
    if st.session_state.get("show_confetti", False):
        st.components.v1.html(CONFETTI_JS, height=0)
        st.session_state.show_confetti = False

    st.markdown("""
    <div style="text-align:center; margin-bottom:28px;">
        <span class="hero-emoji">🎉</span>
        <h1 style="margin-bottom:8px;">Your matches</h1>
        <p style="color:#A89880; font-size:15px;">Curated just for your answers</p>
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("↺ Start over", use_container_width=True):
            st.session_state.page = "landing"
            st.session_state.answers = {}
            st.session_state.recommendations = []
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
elif st.session_state.page == "result":
    result_screen()
elif st.session_state.page == "wishlist":
    wishlist_screen()
