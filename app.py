import streamlit as st
import sqlite3
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- ADVANCED EXTRAORDINARY CSS WITH INTERACTIVE GLOW ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at center, #0f2310 0%, #000000 100%); }
    
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.03);
        padding: 15px; border-radius: 20px; border: 1px solid #4caf50; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.6rem; font-weight: 700; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.3); }
    .stat-label { font-size: 0.75rem; color: #aaa; letter-spacing: 1px; }

    .main-coin-display {
        text-align: center; font-size: 4.5rem; font-weight: 800; color: #ffd700;
        margin: 15px 0; text-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }
    
    .progress-bar-bg { background: #222; border-radius: 10px; height: 12px; width: 100%; margin: 10px 0; overflow:hidden; }
    .progress-bar-fill { background: linear-gradient(90deg, #4caf50, #81c784); height: 100%; border-radius: 10px; }

    .upgrade-card {
        background: rgba(20,20,20,0.8); padding: 18px; border-radius: 15px; border: 1px solid #2e7d32; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .upgrade-title { font-size: 1.1rem; font-weight: 700; color: #fff; }
    .upgrade-desc { font-size: 0.85rem; color: #81c784; }
    .upgrade-cost { font-size: 1.1rem; font-weight: 700; color: #ffd700; }
    </style>
""", unsafe_allow_html=True)

# --- REAL-TIME DATABASE ENGINE ---
conn = sqlite3.connect("village_empire.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER)")
conn.commit()

user_id = "Murthy_Tycoon_Main"
row = db.execute("SELECT coins, pph, level FROM users WHERE id = ?", (user_id,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 1000, 0, 1)", (user_id,))
    conn.commit()
    coins, pph, level = 1000, 0, 1
else:
    coins, pph, level = row

# Calculate level dynamically based on total capacity
calculated_level = 1 + (coins // 10000)
if calculated_level != level:
    level = calculated_level
    db.execute("UPDATE users SET level = ? WHERE id = ?", (level, user_id))
    conn.commit()

# --- INTERACTIVE APP INTERFACE ---

st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-label">PROFIT PER HOUR</div><div class="stat-val">+{pph:,}</div></div>
        <div class="stat-box"><div class="stat-label">VILLAGE LEVEL</div><div class="stat-val">{level}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-coin-display">🪙 {coins:,}</div>', unsafe_allow_html=True)

# Operational Level Progress Bar
progress_percent = min(100, int((coins % 10000) / 100))
st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {progress_percent}%;"></div></div>', unsafe_allow_html=True)
st.caption(f"Level {level} Tycoon • Progress to Next Level: {progress_percent}%")

# Main Interactive Harvest Button Area
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=160)
    if st.button("🚜 HARVEST RICE (TAP) 🚜", use_container_width=True):
        coins += (10 * level)
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
        conn.commit()
        st.rerun()

st.divider()

# Interactive Menu Tabs
t1, t2, t3, t4 = st.tabs(["🛒 Upgrade Shop", "📋 Quests", "🏆 Leaderboard", "💰 Drop"])

with t1:
    st.markdown("### Accelerate Production")
    
    # Item 1: Premium Seeds
    st.markdown("""
        <div class="upgrade-card">
            <div><div class="upgrade-title">Premium Hybrid Seeds</div><div class="upgrade-desc">+100 Profit Per Hour</div></div>
            <div class="upgrade-cost">🪙 500</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Purchase Seeds", use_container_width=True):
        if coins >= 500:
            coins -= 500
            pph += 100
            db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, user_id))
            conn.commit()
            st.toast("Seeds successfully planted!", icon="🌱")
            st.rerun()
        else:
            st.error("Insufficient coin balances for this upgrade.")

    # Item 2: Automatic Irrigation
    st.markdown("""
        <div class="upgrade-card">
            <div><div class="upgrade-title">Solar Irrigation Pumps</div><div class="upgrade-desc">+500 Profit Per Hour</div></div>
            <div class="upgrade-cost">🪙 2,500</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Install Irrigation", use_container_width=True):
        if coins >= 2500:
            coins -= 2500
            pph += 500
            db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, user_id))
            conn.commit()
            st.toast("Irrigation grids online!", icon="⚡")
            st.rerun()
        else:
            st.error("Insufficient coin balances for this upgrade.")

with t2:
    st.markdown("### Daily Campaigns")
    st.info("Complete assignments to build your reserves quickly.")
    st.checkbox("Daily Check-in Verification (Day 1 Claimed: +5,000 Coins)", value=True, disabled=True)
    if st.button("▶️ Stream Sponsored Stream (+1,000 Coins)"):
        coins += 1000
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
        conn.commit()
        st.toast("Ad interaction credit added!", icon="🪙")
        st.rerun()

with t3:
    st.markdown("### Global Ranks")
    st.write("🥇 **Tycoon_King** - 15,403,000 Coins")
    st.write("🥈 **FarmMaster** - 12,110,500 Coins")
    st.write("🥉 **RiceLord** - 9,850,000 Coins")
    st.write(f"⭐ **{user_id}** (You) - {coins:,} Coins")

with t4:
    st.markdown("### Blockchain Ecosystem Readiness")
    st.success("Allocation calculations will balance against Level and Profit Per Hour statistics.")
    st.button("🔗 Link TON Wallet (Mainnet Coming Soon)", disabled=True)

st.divider()
st.markdown('<p style="text-align:center; color:#4caf50; font-size:0.75rem; font-weight:bold;">VILLAGE MINING AI v3.0 • PLATINUM EDITION</p>', unsafe_allow_html=True)
