import streamlit as st
import sqlite3
import time
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Village Mining AI - Tap to Earn", page_icon="🌾", layout="centered")

# --- DATABASE SETUP ---
conn = sqlite3.connect("village_users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        coins INTEGER DEFAULT 0,
        last_login TEXT
    )
""")
conn.commit()

# Mock user for testing (In Telegram, this comes from Telegram URL)
# To test on web, we use a default user 'murthy_user'
if 'user_id' not in st.session_state:
    st.session_state.user_id = "murthy_user"

user_id = st.session_state.user_id

# Fetch or Create User Profile from DB
cursor.execute("SELECT coins, last_login FROM users WHERE user_id = ?", (user_id,))
row = cursor.execute("SELECT coins, last_login FROM users WHERE user_id = ?", (user_id,)).fetchone()

if row is None:
    cursor.execute("INSERT INTO users (user_id, coins, last_login) VALUES (?, ?, ?)", (user_id, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    current_coins = 0
    last_login_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
else:
    current_coins, last_login_str = row

# --- CORE FEATURE: OFFLINE FARMING (PASSIVE INCOME) ---
# Calculate hours passed since last visit
last_login_dt = datetime.strptime(last_login_str, "%Y-%m-%d %H:%M:%S")
time_diff = datetime.now() - last_login_dt
hours_passed = time_diff.total_seconds() / 3600

# Cap the offline farming to maximum 3 hours (As per Hamster/X-Empire model)
if hours_passed > 3:
    hours_passed = 3

# Earn 500 coins per hour when offline
offline_earnings = int(hours_passed * 500)

if offline_earnings > 0:
    current_coins += offline_earnings
    # Immediately update the DB so it doesn't loop
    cursor.execute("UPDATE users SET coins = ?, last_login = ? WHERE user_id = ?", (current_coins, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    st.success(f"🚜 Welcome back! Your village farmers mined 🪙 {offline_earnings} Coins while you were away! (Max 3 hours)")

# Update last login time for current session
cursor.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
conn.commit()

# Beautiful CSS Custom Styling
st.markdown("""
    <style>
    .main-title { text-align: center; color: #4CAF50; font-size: 3rem; font-weight: bold; margin-bottom: 10px; }
    .subtitle { text-align: center; color: #888; font-size: 1.2rem; margin-bottom: 30px; }
    .score-box { text-align: center; background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 2px solid #4CAF50; font-size: 2.5rem; font-weight: bold; color: #FFD700; margin-bottom: 20px; }
    .ad-box { background-color: #2d2d2d; border: 1px dashed #555; padding: 15px; text-align: center; border-radius: 10px; color: #aaa; font-size: 0.9rem; margin-top: 30px; }
    .share-box { background-color: #1a2e1a; border: 1px solid #4CAF50; padding: 15px; border-radius: 10px; margin-top: 20px; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# App Content UI
st.markdown("<div class='main-title'>🌾 VILLAGE MINING AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Build Your Digital Village - Offline Farming Active ✅</div>", unsafe_allow_html=True)

# Display Real-time Coins from Database
st.markdown(f"<div class='score-box'>🪙 {current_coins} Coins</div>", unsafe_allow_html=True)

# --- MINING TAP BUTTON ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚜 TAP TO GROW VILLAGE 🚜", use_container_width=True):
        new_balance = current_coins + 10
        cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()
        st.rerun()

st.divider()

# --- SHARE & REFERRAL SYSTEM ---
st.markdown("### 👥 Invite Friends & Earn")
st.markdown("<div class='share-box'><b>🎁 Bonus:</b> Invite your friends to build their village and get <b>+5,000 Coins</b> instantly!</div>", unsafe_allow_html=True)

referral_link = "https://t.me/VillageMiningAIBot?start=user_123456"
st.text_input("Copy your unique referral link:", value=referral_link, disabled=True)

if st.button("📢 Share on WhatsApp", use_container_width=True):
    whatsapp_url = f"https://api.whatsapp.com/send?text=Join%20the%20amazing%20Village%20Mining%20AI%20game%2C%20build%20your%20village%20and%20start%20earning%20now!%20{referral_link}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">Open WhatsApp to Invite</button></a>', unsafe_allow_html=True)

# --- ADVERTISEMENTS PLACEHOLDER ---
st.markdown("<div class='ad-box'>📺 <b>Sponsored Advertisement Box</b><br>Ads from Telegram/Google networks will stream here. (Revenue generates per view/click)</div>", unsafe_allow_html=True)
