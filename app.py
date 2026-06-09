import streamlit as st
import sqlite3
import random
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- ULTIMATE PREMIUM CSS (HAMSTER KOMBAT STYLE) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Urbanist:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000; color: #fff; }
    .stApp { background: radial-gradient(circle at 50% 20%, #1a3c1a 0%, #000 100%); }
    
    /* Block Streamlit Elements */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* Header Card */
    .header-card {
        background: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 15px;
        display: flex; align-items: center; justify-content: space-between;
        border: 1px solid #2e7d32; margin-bottom: 10px;
    }
    .profile-img { width: 45px; height: 45px; border-radius: 50%; border: 2px solid #ffd700; background: #222; text-align: center; line-height: 42px; font-size: 22px; }

    /* Stats Box */
    .stat-row { display: flex; gap: 8px; margin-bottom: 15px; }
    .stat-box { background: #111; border: 1px solid #333; border-radius: 12px; padding: 8px; flex: 1; text-align: center; }
    .stat-val { font-size: 0.85rem; font-weight: bold; color: #ffd700; font-family: 'Orbitron'; }
    .stat-lbl { font-size: 0.55rem; color: #888; }

    /* Big Balance */
    .balance-container { text-align: center; margin: 20px 0; }
    .balance-val { font-size: 3.5rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron'; text-shadow: 0 0 20px rgba(255,215,0,0.4); }

    /* TAPPER AREA */
    .tapper-zone {
        display: flex; justify-content: center; align-items: center;
        background: radial-gradient(circle, rgba(76,175,80,0.2) 0%, rgba(0,0,0,0) 70%);
        height: 220px; position: relative; margin-top: 15px;
    }
    
    /* Premium Item Cards */
    .premium-item-card {
        background: rgba(15,15,15,0.85); border: 1px solid #222; border-radius: 16px; padding: 14px;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
    }
    .item-title { font-weight: bold; font-size: 0.95rem; color: #fff; }
    .item-desc { font-size: 0.7rem; color: #888; }
    .item-cost { color: #ffd700; font-weight: 800; font-family: 'Orbitron'; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
conn = sqlite3.connect("village_v70_final.db", check_same_thread=False)
db = conn.cursor()
# Added last_claim column to track dynamic date-stamps
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER, last_claim TEXT)")
conn.commit()

USER_ID = "Murthy_Grand_Tycoon"
row = db.execute("SELECT coins, pph, level, last_claim FROM users WHERE id = ?", (USER_ID,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 45000, 500, 1, '')", (USER_ID,))
    conn.commit()
    coins, pph, level, last_claim = 45000, 500, 1, ""
else:
    coins, pph, level, last_claim = row

# --- LEVEL SYSTEM ---
COINS_PER_LEVEL = 10000
level = 1 + (coins // COINS_PER_LEVEL)
next_target = level * COINS_PER_LEVEL
progress = min(int(((coins % COINS_PER_LEVEL) / COINS_PER_LEVEL) * 100), 100)

# --- TOP PROFILE HEADER ---
st.markdown(f"""
    <div class="header-card">
        <div style="display:flex; align-items:center; gap:10px;">
            <div class="profile-img">👨‍🌾</div>
            <div>
                <div style="font-weight:bold; font-size:14px;">{USER_ID}</div>
                <div style="color:#4caf50; font-size:10px;">LEVEL {level} • GRAND TYCOON</div>
            </div>
        </div>
        <div style="text-align:right; color:#888; font-size:10px;">AIRDROP<br><b style="color:#ffd700;">SEASON 1</b></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box"><div class="stat-lbl">PROFIT / HOUR</div><div class="stat-val">+{pph:,}</div></div>
        <div class="stat-box"><div class="stat-lbl">MY RANK</div><div class="stat-val">#1,042</div></div>
        <div class="stat-box"><div class="stat-lbl">MULTIPLIER</div><div class="stat-val">x{level}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- COIN MATRIX ---
st.markdown(f'<div class="balance-container"><div class="balance-val">🪙 {coins:,}</div></div>', unsafe_allow_html=True)

# --- NATIVE NAVIGATION COMPONENT ---
menu = st.segmented_control("Navigation", ["🎯 MINE", "🚀 BOOST", "📜 EARN QUESTS", "🏆 FRENZ", "💎 AIRDROP"], selection_mode="single", default="🎯 MINE", label_visibility="collapsed")

st.divider()

current_today = datetime.now().strftime("%Y-%m-%d")

if menu == "🎯 MINE":
    st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:12px; color:#81c784;'><b>Level {level}</b> <b>Target: {next_target:,}</b></div>", unsafe_allow_html=True)
    st.progress(progress / 100)
    
    st.markdown('<div class="tapper-zone">', unsafe_allow_html=True)
    if st.button("🚜 CLICK TO HARVEST RICE", key="tap", use_container_width=True):
        coins += (15 * level)
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
        conn.commit()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🚀 BOOST":
    st.markdown("### 🎁 Mystery Reward Box")
    if st.button("Unlock Golden Box (1,000 Coins)", use_container_width=True):
        if coins >= 1000:
            coins -= 1000
            won = random.choice([2000, 5000, 15000])
            coins += won
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.balloons()
            st.success(f"🎉 Premium crate cracked! You found 🪙 {won:,} Coins!")
            st.rerun()
        else:
            st.error("❌ Insufficient coins!")

elif menu == "📜 EARN QUESTS":
    st.markdown("### 📜 Daily Task Center")
    
    st.markdown("""
        <div class="premium-item-card">
            <div>
                <div class="item-title">🎁 Attendance Streak Multiplier</div>
                <div class="item-desc">Claim your web3 distribution setup bonus</div>
            </div>
            <div class="item-cost" style="color:#4caf50;">+5,000</div>
        </div>
    """, unsafe_allow_html=True)
    
    # DYNAMIC TIME-LOCK SYSTEM CHECK
    if last_claim == current_today:
        st.warning("🔒 Already claimed today! Come back tomorrow for your next check-in streak.")
        st.button("Claim Daily Reward (+5,000)", disabled=True, use_container_width=True)
    else:
        if st.button("Claim Daily Reward (+5,000)", use_container_width=True):
            coins += 5000
            # Lock the claim process for today
            db.execute("UPDATE users SET coins = ?, last_claim = ? WHERE id = ?", (coins, current_today, USER_ID))
            conn.commit()
            st.toast("5,000 Streak Coins credited successfully!", icon="🎁")
            st.rerun()

elif menu == "🏆 FRENZ":
    st.markdown("### 🏆 Worldwide Ranking Ecosystem")
    st.markdown(f"""
        <div class="premium-item-card"><div><b>🥇 Tycoon_King</b></div><div class="item-cost">15,403,000</div></div>
        <div class="premium-item-card"><div><b>🥈 FarmMaster_AI</b></div><div class="item-cost">12,110,500</div></div>
        <div class="premium-item-card" style="border: 1px solid #ffd700; background:rgba(255,215,0,0.05);"><div><b>⭐ {USER_ID} (YOU)</b></div><div class="item-cost">{coins:,}</div></div>
    """, unsafe_allow_html=True)

elif menu == "💎 AIRDROP":
    st.markdown("### 💎 Web3 Token Snapshot")
    st.info("Ecosystem snapshot algorithm checks total Profit Per Hour metrics dynamic balances.")
    st.button("🔗 Connect TON Wallet Address (Soon)", disabled=True, use_container_width=True)

# Fixed footer bottom gap padding
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
