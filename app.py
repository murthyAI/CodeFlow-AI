import streamlit as st

# Page configuration
st.set_page_config(page_title="CyberTap AI - Mining Game", page_icon="🪙", layout="centered")

# Custom CSS for beautiful styling and animations
st.markdown("""
    <style>
    .main-title { text-align: center; color: #FFD700; font-size: 3rem; font-weight: bold; margin-bottom: 10px; }
    .subtitle { text-align: center; color: #888; font-size: 1.2rem; margin-bottom: 30px; }
    .score-box { text-align: center; background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; font-size: 2.5rem; font-weight: bold; color: #FFD700; margin-bottom: 20px; }
    .ad-box { background-color: #2d2d2d; border: 1px dashed #555; padding: 15px; text-align: center; border-radius: 10px; color: #aaa; font-size: 0.9rem; margin-top: 30px; }
    .share-box { background-color: #152238; border: 1px solid #007bff; padding: 15px; border-radius: 10px; margin-top: 20px; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🪙 CYBER-TAP AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Next-Generation Tap-to-Earn Mining Platform</div>", unsafe_allow_html=True)

# Initialize Session States for Score
if 'coins' not in st.session_state:
    st.session_state.coins = 0

# Display Current Balance
st.markdown(f"<div class='score-box'>💰 {st.session_state.coins} Coins</div>", unsafe_allow_html=True)

# --- CORE FEATURE 1: THE MINING TAP BUTTON ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 TAP TO MINE 🚀", use_container_width=True):
        st.session_state.coins += 10
        st.rerun()

st.divider()

# --- CORE FEATURE 2: SHARE & REFERRAL SYSTEM ---
st.markdown("### 👥 Invite Friends & Earn")
st.markdown("<div class='share-box'><b>🎁 Bonus:</b> Share with your friends and get <b>+5,000 Coins</b> for each referral!</div>", unsafe_allow_html=True)

referral_link = "https://t.me/CyberTapAIBot?start=user_123456"
st.text_input("Copy your unique referral link:", value=referral_link, disabled=True)

if st.button("📢 Share on WhatsApp", use_container_width=True):
    whatsapp_url = f"https://api.whatsapp.com/send?text=Join%20the%20next%20big%20crypto%20game%20CyberTap%20AI%20and%20start%20mining%20now!%20{referral_link}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">Open WhatsApp to Invite</button></a>', unsafe_allow_html=True)

# --- CORE FEATURE 3: ADVERTISEMENTS PLACEHOLDER ---
st.markdown("<div class='ad-box'>📺 <b>Sponsored Advertisement Box</b><br>Ads from Telegram/Google networks will stream here. (Revenue generates per view/click)</div>", unsafe_allow_html=True)
