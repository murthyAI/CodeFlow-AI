import streamlit as st
import sqlite3
import random
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- DELUXE VISUAL ENGINE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at center, #0f2310 0%, #000000 100%); }
    
    /* Stats Row */
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.03);
        padding: 15px; border-radius: 20px; border: 1px solid #4caf50; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.6rem; font-weight: 700; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.3); }
    .stat-label { font-size: 0.75rem; color: #aaa; letter-spacing: 1px; }

    /* Animations */
    @keyframes boxShaking { 0% { transform: rotate(0deg); } 25% { transform: rotate(5deg); } 50% { transform: rotate(-5deg); } 75% { transform: rotate(5deg); } 100% { transform: rotate(0deg); } }
    @keyframes glowExpand { 0% { box-shadow: 0 0 10px #ffd700; } 50% { box-shadow: 0 0 40px #ffd700; } 100% { box-shadow: 0 0 10px #ffd700; } }
    @keyframes coinFloat { 0% { transform: translateY(0) scale(1); opacity: 1; } 100% { transform: translateY(-100px) scale(1.5); opacity: 0; } }

    .gift-box-idle {
        width: 150px; margin: 0 auto; display: block;
        filter: drop-shadow(0 0 15px rgba(255, 215, 0, 0.5));
        animation: boxShaking 1.5s infinite ease-in-out;
    }
    
    .gift-box-opening {
        width: 160px; margin: 0 auto; display: block;
        filter: drop-shadow(0 0 30px #ffd700);
        animation: boxShaking 0.2s infinite;
    }

    .deluxe-reward-container {
        background: radial-gradient(circle, rgba(255, 215, 0, 0.2) 0%, rgba(0,0,0,0) 80%);
        padding: 30px; border-radius: 30px; border: 2px solid #ffd700;
        text-align: center; margin: 20px 0; box-shadow: 0 0 50px rgba(255, 215, 0, 0.4);
    }
    
    .stRadio > div { flex-direction: row; justify-content: space-around; }
    .stRadio label { background: transparent !important; color: #4caf50 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DB ENGINE ---
conn = sqlite3.connect("village_v37_deluxe.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER)")
conn.commit()

user_id = "Murthy_Deluxe_Tycoon"
row = db.execute("SELECT coins, pph, level FROM users WHERE id = ?", (user_id,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 5000, 0, 1)", (user_id,))
    conn.commit()
    coins, pph, level = 5000, 0, 1
else:
    coins, pph, level = row

# Calculations
stage = 1 + (coins // 10000)
db.execute("UPDATE users SET level = ? WHERE id = ?", (stage, user_id))
conn.commit()

# --- UI INTERFACE ---
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-label">PROFIT PER HOUR</div><div class="stat-val">+{pph:,}</div></div>
        <div class="stat-box"><div class="stat-label">LEVEL</div><div class="stat-val">{stage}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center; font-size:4rem; font-weight:800; color:#ffd700;">🪙 {coins:,}</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=120)
    if st.button("🚜 HARVEST 🚜", use_container_width=True):
        coins += (10 * stage)
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
        conn.commit()
        st.rerun()

st.divider()

# Navigation
active_mod = st.radio("Menu", ["🛒 Shop", "🎁 Mystery Box", "📋 Quests", "🏆 Ranks", "💰 Airdrop"], horizontal=True, label_visibility="collapsed")
st.divider()

if active_mod == "🎁 Mystery Box":
    st.markdown("<h3 style='text-align:center;'>Golden Crate Reveal</h3>", unsafe_allow_html=True)
    
    if 'opening' not in st.session_state: st.session_state.opening = False

    if not st.session_state.opening:
        # Idle Pulsing Box (Image form function call result)
        st.markdown('<img src="http://googleusercontent.com/image_collection/image_retrieval/12921852151188288944" class="gift-box-idle">', unsafe_allow_html=True)
        if st.button("Unlock Deluxe Crate (🪙 1,000)", use_container_width=True):
            if coins >= 1000:
                coins -= 1000
                st.session_state.opening = True
                db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
                conn.commit()
                st.rerun()
            else:
                st.error("Insufficient balance!")
    else:
        # Opening Animation
        st.markdown('<img src="http://googleusercontent.com/image_collection/image_retrieval/12921852151188288944" class="gift-box-opening">', unsafe_allow_html=True)
        time.sleep(1.5) # Time for visual shaking
        
        # Reward Logic
        roll = random.choice(["jackpot", "mega", "pph"])
        if roll == "jackpot":
            win = 25000
            coins += win
            st.balloons()
            st.markdown(f'<div class="deluxe-reward-container"><h1 style="color:#ffd700;">JACKPOT!</h1><img src="http://googleusercontent.com/image_collection/image_retrieval/996288920124292514" width="200"><h2 style="font-size:3rem;">🪙 +{win:,}</h2></div>', unsafe_allow_html=True)
        elif roll == "mega":
            win = 5000
            coins += win
            st.markdown(f'<div class="deluxe-reward-container"><h1 style="color:#ffd700;">MEGA WIN</h1><h2 style="font-size:2.5rem;">🪙 +{win:,}</h2></div>', unsafe_allow_html=True)
        else:
            win_pph = 500
            pph += win_pph
            st.markdown(f'<div class="deluxe-reward-container"><h1 style="color:#4caf50;">PPH BOOST</h1><h2 style="font-size:2.5rem;">+{win_pph:,} PPH</h2></div>', unsafe_allow_html=True)
        
        db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, user_id))
        conn.commit()
        st.session_state.opening = False
        if st.button("Continue Farming"): st.rerun()

elif active_mod == "🛒 Shop":
    st.markdown("### Production Tools")
    # Simple Purchase Logic
    cost = 500 + (pph * 2)
    st.markdown(f'<div style="background:#111; padding:20px; border-radius:15px; border:1px solid #2e7d32; display:flex; justify-content:space-between;"><div><b>Hybrid Seeds</b><br>+100 PPH</div><div style="color:#ffd700;">🪙 {cost:,}</div></div>', unsafe_allow_html=True)
    if st.button("Buy Upgrade"):
        if coins >= cost:
            coins -= cost
            pph += 100
            db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, user_id))
            conn.commit()
            st.rerun()

elif active_mod == "📋 Quests":
    st.markdown("### Daily Assignments")
    if st.button("Claim Daily Reward (+5,000 Coins)"):
        coins += 5000
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, user_id))
        conn.commit()
        st.rerun()

elif active_mod == "🏆 Ranks":
    st.markdown("### Leaderboard")
    st.write("🥇 **Tycoon_King** - 15,403,000")
    st.write(f"⭐ **{user_id}** - {coins:,}")

elif active_mod == "💰 Airdrop":
    st.markdown("### TON Wallet Integration")
    st.success("Eligibility: Connect your wallet to claim tokens soon!")
    st.button("Connect Wallet (Mainnet)", disabled=True)

st.divider()
st.markdown('<p style="text-align:center; color:#4caf50; font-size:0.7rem;">VILLAGE MINING AI v3.7 • DELUXE EDITION</p>', unsafe_allow_html=True)
