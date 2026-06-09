import streamlit as st
import sqlite3
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- ADVANCED EXTRAORDINARY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at center, #1a2e1a 0%, #000000 100%); }
    
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.05);
        padding: 15px; border-radius: 20px; border: 1px solid #4caf50; margin-bottom: 20px;
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.5rem; font-weight: 700; color: #ffd700; }
    .stat-label { font-size: 0.8rem; color: #888; }

    .main-coin-display {
        text-align: center; font-size: 4rem; font-weight: 800; color: #ffd700;
        margin: 20px 0; text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
    }
    
    .progress-bar-bg { background: #222; border-radius: 10px; height: 10px; width: 100%; margin: 10px 0; }
    .progress-bar-fill { background: #4caf50; height: 100%; border-radius: 10px; width: 45%; } /* Simulated Level 1 */

    .upgrade-card {
        background: #111; padding: 15px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- DB & LOGIC ---
conn = sqlite3.connect("village_pro.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER)")
conn.commit()

user_id = "Murthy_Tycoon_1" # Simulated session
row = db.execute("SELECT coins, pph, level FROM users WHERE id = ?", (user_id,)).fetchone()
if not row:
    db.execute("INSERT INTO users VALUES (?, 1000, 500, 1)", (user_id,))
    conn.commit()
    coins, pph, level = 1000, 500, 1
else:
    coins, pph, level = row

# --- UI CONTENT ---

# Top Stats (PPH and Level)
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-label">PROFIT PER HOUR</div><div class="stat-val">+{pph:,}</div></div>
        <div class="stat-box"><div class="stat-label">VILLAGE LEVEL</div><div class="stat-val">{level}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-coin-display">🪙 {coins:,}</div>', unsafe_allow_html=True)

# Level Progress
st.markdown('<div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>', unsafe_allow_html=True)
st.caption(f"Level {level} Tycoon • Next Level at 50,000 Coins")

# Mining Area
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=180)
    if st.button("🚜 HARVEST (TAP) 🚜", use_container_width=True):
        coins += (10 * level)
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
        conn.commit()
        st.rerun()

st.divider()

# Navigation Tabs
t1, t2, t3, t4 = st.tabs(["🛒 Shop", "📋 Tasks", "🏆 Rank", "💰 Wallet"])

with t1:
    st.markdown("### Upgrade your Village")
    st.markdown("""
        <div class="upgrade-card"><div><b>Premium Seeds</b><br><small>+200 PPH</small></div><div style="color:#ffd700">Cost: 5,000</div></div>
        <div class="upgrade-card"><div><b>Automatic Irrigation</b><br><small>+1,000 PPH</small></div><div style="color:#ffd700">Cost: 25,000</div></div>
        <div class="upgrade-card"><div><b>AI Tractor</b><br><small>+5,000 PPH</small></div><div style="color:#ffd700">Cost: 100,000</div></div>
    """, unsafe_allow_html=True)
    if st.button("Buy Premium Seeds"): st.warning("Need more coins!")

with t2:
    st.markdown("### Daily Quests")
    st.checkbox("Daily Check-in (Day 1: +5,000 Coins)", value=True, disabled=True)
    st.button("📺 Watch Video (+10k Coins)")

with t3:
    st.markdown("### Global Leaderboard")
    st.write("🥇 **Murthy_Tycoon_1** (You) - #1,204")
    st.write("... loading real-time data ...")

with t4:
    st.markdown("### Airdrop Preparedness")
    st.success("Wallet Connection opening soon for TON Ecosystem!")
    st.button("🔗 Connect Wallet (Coming Soon)")

st.divider()
st.markdown('<p style="text-align:center; color:#555; font-size:0.7rem;">Village Mining AI v2.0 • Extraordinary Edition</p>', unsafe_allow_html=True)
