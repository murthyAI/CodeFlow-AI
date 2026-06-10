import streamlit as st
import sqlite3
import random
import time
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- PRODUCTION GRADE HIGH-END TELEGRAM WEB3 APP UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=700;900&family=Urbanist:wght=600;800;900&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at 50% 15%, #0b1f0b 0%, #010401 60%, #000000 100%); }
    
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    .premium-header-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.01) 100%);
        border-radius: 22px; padding: 12px 16px; border: 1px solid rgba(76, 175, 80, 0.35);
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6); margin-bottom: 15px;
    }
    .profile-img-frame { width: 42px; height: 42px; border-radius: 50%; border: 2px solid #ffd700; background: #111; text-align: center; line-height: 38px; font-size: 20px; }
    .dashboard-stats-grid { display: flex; gap: 8px; margin-bottom: 15px; }
    .dashboard-stat-unit { background: rgba(10,10,10,0.9); border: 1px solid #1c1c1c; border-radius: 14px; padding: 10px; flex: 1; text-align: center; }
    .dashboard-stat-val { font-size: 0.9rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron'; }
    .dashboard-stat-lbl { font-size: 0.55rem; color: #777; font-weight: bold; }
    .grand-token-display { text-align: center; margin: 10px 0; }
    .grand-token-val { font-size: 3.5rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron'; text-shadow: 0 0 25px rgba(255,215,0,0.5); }
    .premium-interactive-coin-node {
        width: 180px; height: 180px; border-radius: 50%; margin: 15px auto;
        background: radial-gradient(circle, #2e7d32 10%, #1b5e20 80%);
        border: 6px solid #ffd700; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 0 45px rgba(76, 175, 80, 0.7), inset 0 0 20px rgba(0,0,0,0.8);
        font-size: 85px; user-select: none;
    }
    .action-module-row-card {
        background: rgba(12,12,12,0.95); border: 1px solid #222; border-radius: 16px; padding: 15px;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }
    .module-card-headline { font-weight: 800; font-size: 0.95rem; color: #fff; }
    .module-card-cost-index { color: #ffd700; font-weight: 900; font-family: 'Orbitron'; font-size: 0.9rem; }
    .monetization-ad-banner {
        background: linear-gradient(90deg, rgba(255,215,0,0.08) 0%, rgba(76,175,80,0.08) 100%);
        border: 2px dashed rgba(255,215,0,0.4); border-radius: 14px;
        padding: 15px; text-align: center; margin-top: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        cursor: pointer; display: block; text-decoration: none; color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE LOGISTICS SYSTEM ---
conn = sqlite3.connect("village_v14_final.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER, last_claim TEXT)")
conn.commit()

USER_ID = "Murthy_Grand_Tycoon"
row = db.execute("SELECT coins, pph, level, last_claim FROM users WHERE id = ?", (USER_ID,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 257605, 900, 1, '')", (USER_ID,))
    conn.commit()
    coins, pph, level, last_claim = 257605, 900, 1, ""
else:
    coins, pph, level, last_claim = row

# --- ADVANCED LEVELS LOGIC (10 TIERS) ---
COINS_PER_LEVEL = 100000  
MAX_SYSTEM_LEVELS = 10
calculated_level = 1 + (coins // COINS_PER_LEVEL)
level = min(calculated_level, MAX_SYSTEM_LEVELS)
next_target = level * COINS_PER_LEVEL
points_needed = max(0, next_target - coins)
progress_bar_val = min(int(((coins % COINS_PER_LEVEL) / COINS_PER_LEVEL) * 100), 100)

# --- AIRDROP COUNTDOWN ---
launch_target_date = datetime(2026, 9, 10)  
current_time_now = datetime.now()
days_remaining = max(0, (launch_target_date - current_time_now).days)

# --- HEADER INTERFACE ---
st.markdown(f"""
    <div class="premium-header-card">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="profile-img-frame">👨‍🌾</div>
            <div>
                <div style="font-weight:900; font-size:14px; letter-spacing:0.3px;">{USER_ID}</div>
                <div style="color:#4caf50; font-size:10px; font-weight:bold;">LEVEL {level}/{MAX_SYSTEM_LEVELS} • GRAND LANDLORD</div>
            </div>
        </div>
        <div style="text-align:right;">
            <span style="font-size:8px; font-weight:bold; color:#aaa;">AIRDROP: SEP 10, 2026</span><br>
            <b style="color:#ffd700; font-family:'Orbitron'; font-size:12px;">⏳ {days_remaining} DAYS LEFT</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- METRIC PERFORMANCE BLOCK ROW ---
st.markdown(f"""
    <div class="dashboard-stats-grid">
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">PROFIT / HOUR</div><div class="dashboard-stat-val">⚡ +{pph:,}</div></div>
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">TOTAL TIERS</div><div class="dashboard-stat-val">⭐ 10 LEVELS</div></div>
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">MULTIPLIER</div><div class="dashboard-stat-val">x{level}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="grand-token-display"><div class="grand-token-val">🪙 {coins:,}</div></div>', unsafe_allow_html=True)

# --- NAVIGATION ---
active_panel = st.segmented_control("Nav", ["🎯 MINE", "🚀 BOOST", "📜 QUESTS", "🏆 FRENZ", "💎 DROP"], selection_mode="single", default="🎯 MINE", label_visibility="collapsed")
st.divider()
current_date_stamp = datetime.now().strftime("%Y-%m-%d")

if active_panel == "🎯 MINE":
    if level < MAX_SYSTEM_LEVELS:
        # PURE ENGLISH TRANSLATION - NO TELUGU ANYWHERE
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; font-size:11px; color:#81c784; margin-bottom:4px; font-weight:900;'>
                <span>RANK METRIC: {coins:,} / {next_target:,}</span>
                <span style='color:#ffd700;'>🚜 NEED FOR NEXT LEVEL: {points_needed:,} POINTS</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:11px; color:#ffd700; font-weight:900; text-align:center;'>🏆 ALL LEVELS MAXED OUT!</div>", unsafe_allow_html=True)
        
    st.progress(progress_bar_val / 100)
    st.markdown('<div class="premium-interactive-coin-node">🚜</div>', unsafe_allow_html=True)
    
    if st.button("⚡ TAP TRACTOR TO HARVEST COINS ⚡", key="harvest_v14", use_container_width=True):
        coins += (40 * level)
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
        conn.commit()
        st.toast(f"🪙 +{40 * level} Coins Harvested!", icon="🚜")
        st.rerun()

elif active_panel == "🚀 BOOST":
    st.markdown("### 🚀 Premium Ecosystem Mystery Crate")
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.12) 0%, rgba(0,0,0,0.7) 100%); border: 2px dashed #ffd700; border-radius: 20px; padding: 22px; text-align: center; box-shadow: 0 0 25px rgba(255,215,0,0.25); margin-bottom: 20px;">
            <h1 style="font-size: 65px; margin: 0;">🎁</h1>
            <h3 style="color:#ffd700; margin-top:10px; font-family:'Orbitron';">GOLD CRATE REVEAL</h3>
            <p style="font-size:0.75rem; color:#ccc;">Costs 1,000 coins. Instant randomized drops of 2,000, 5,000, or 15,000 tokens!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔓 Crack Premium Mystery Box (1,000 Coins)", key="crate_v14", use_container_width=True):
        if coins >= 1000:
            coins -= 1000
            won_prize = random.choice([2000, 5000, 15000])
            coins += won_prize
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            with st.spinner("Decoding Mystery Box..."):
                time.sleep(1)
            st.balloons()
            st.success(f"🎉 Crate opened! Reward: 🪙 +{won_prize:,} Coins!")
            st.rerun()
        else:
            st.error("❌ Insufficient tokens!")

elif active_panel == "📜 QUESTS":
    st.markdown("### 📜 Automated Daily Task Center")
    if last_claim == current_date_stamp:
        st.warning("🔒 Already claimed today!")
        st.button("Claim Daily Reward (+5,000)", disabled=True)
    else:
        if st.button("Claim Daily Reward (+5,000)", use_container_width=True):
            coins += 5000
            db.execute("UPDATE users SET coins = ?, last_claim = ? WHERE id = ?", (coins, current_date_stamp, USER_ID))
            conn.commit()
            st.toast("5,000 Milestone Tokens credited!", icon="🎁")
            st.rerun()

elif active_panel == "🏆 FRENZ":
    st.markdown(f"### 🏆 Global Leaderboard")
    st.write(f"⭐ **{USER_ID} (YOU)** - {coins:,}")

elif active_panel == "💎 DROP":
    st.markdown("### 💎 Web3 Snapshot Distribution")
    st.button("🔗 Bind TON Wallet Address (Locked)", disabled=True)

# --- AD BANNER ---
st.markdown("""
    <a href="https://www.google.com" target="_blank" class="monetization-ad-banner">
        <span style="font-size: 0.65rem; color: #ffd700; font-weight: bold; letter-spacing: 1px; display: block; margin-bottom: 2px;">💰 SPONSORED PROMO AD ZONE (CLICK TO EARN) 💰</span>
        <p style="font-size: 0.85rem; color: #fff; margin: 0; font-weight: bold;">🌾 Upgrade Your Crop Yields with Village Mining AI Partners! Click here! 🌾</p>
    </a>
""", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
