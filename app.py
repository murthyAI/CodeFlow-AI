import streamlit as st
import sqlite3
import time
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- STYLED CSS FOR EXTRAORDINARY UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Urbanist', sans-serif;
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1b5e20, #4caf50);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    .coin-balance {
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffd700;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
    
    .mining-section {
        text-align: center;
        padding: 40px 20px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 30px;
        border: 1px solid #2e7d32;
        margin-bottom: 30px;
    }
    
    .tractor-btn {
        background: none;
        border: none;
        cursor: pointer;
        transition: transform 0.1s ease-in-out;
    }
    
    .tractor-btn:active {
        transform: scale(0.9);
    }

    .task-card {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #ffd700;
        margin-bottom: 10px;
    }

    .ad-placeholder {
        background: #262730;
        border: 1px dashed #4caf50;
        padding: 20px;
        text-align: center;
        border-radius: 15px;
        color: #888;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE LOGIC ---
conn = sqlite3.connect("village_mining.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, coins INTEGER, last_mining TEXT)")
conn.commit()

# Current User Simulation (Integrated with Telegram later)
user_id = "User_777" 
row = db.execute("SELECT coins, last_mining FROM users WHERE user_id = ?", (user_id,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    coins, last_mining = 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
else:
    coins, last_mining = row

# --- OFFLINE FARMING CALCULATION ---
last_dt = datetime.strptime(last_mining, "%Y-%m-%d %H:%M:%S")
diff = (datetime.now() - last_dt).total_seconds() / 3600
if diff > 3: diff = 3 # Cap at 3 hours
offline_bonus = int(diff * 1000) # 1000 coins per hour

if offline_bonus > 50: # Only show if significant
    coins += offline_bonus
    db.execute("UPDATE users SET coins = ?, last_mining = ? WHERE user_id = ?", (coins, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    st.toast(f"🚜 Your Farmers mined {offline_bonus} coins while you were away!", icon="🌾")

# --- UI LAYOUT ---
st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0; font-size: 1.5rem; color: #e8f5e9;">VILLAGE MINING AI</h1>
        <div class="coin-balance">🪙 {coins:,}</div>
        <p style="margin:0; color: #a5d6a7;">Global Tycoon Rank: #1,204</p>
    </div>
""", unsafe_allow_html=True)

# Central Mining Area
st.markdown('<div class="mining-section">', unsafe_allow_html=True)
st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=150) # Tractor Icon
if st.button("🚜 HARVEST RICE (TAP) 🚜", use_container_width=True):
    coins += 10
    db.execute("UPDATE users SET coins = ?, last_mining = ? WHERE user_id = ?", (coins, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
    conn.commit()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Tabs for Tasks and Referrals
tab1, tab2, tab3 = st.tabs(["📋 Tasks", "🤝 Refer", "🏆 Leaders"])

with tab1:
    st.markdown("### Daily Missions")
    st.markdown('<div class="task-card"><b>Watch Video Ad:</b> Get +5,000 Coins 🪙<br><small>Click to earn rewards</small></div>', unsafe_allow_html=True)
    if st.button("▶️ Watch Ad"): st.success("Feature connecting to Ad Network...")

    st.markdown('<div class="task-card"><b>Follow on X:</b> Get +10,000 Coins 🪙</div>', unsafe_allow_html=True)
    st.markdown('<div class="task-card"><b>Join Telegram:</b> Get +20,000 Coins 🪙</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### Invite & Multiply")
    st.info("Share your link and earn 10% of your friends' lifetime earnings!")
    st.text_input("Referral Link", value=f"https://t.me/VillageMiningAIBot?start={user_id}", disabled=True)
    st.button("📢 Share to WhatsApp")

with tab3:
    st.markdown("### Global Leaderboard")
    st.write("1. 👑 Tycoon_King - 15.4M Coins")
    st.write("2. 🚜 FarmMaster - 12.1M Coins")
    st.write("3. 🌾 RiceLord - 9.8M Coins")

st.divider()

# Ads Section
st.markdown('<div class="ad-placeholder">📺 SPONSORED CONTENT<br>Monetization active. Revenue flowing from Telegram Ads Network.</div>', unsafe_allow_html=True)
