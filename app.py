import streamlit as st
import sqlite3
import random
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- ULTRA-PLATINUM VISUALS & ANIMATIONS CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    
    /* Core Styling */
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at center, #0f2310 0%, #000000 100%); }
    
    /* Stats Headers */
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.03);
        padding: 15px; border-radius: 20px; border: 1px solid #4caf50; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.6rem; font-weight: 700; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.3); }
    .stat-label { font-size: 0.75rem; color: #aaa; letter-spacing: 1px; }

    /* Main Balance */
    .main-coin-display {
        text-align: center; font-size: 4.5rem; font-weight: 800; color: #ffd700;
        margin: 15px 0; text-shadow: 0 0 25px rgba(255, 215, 0, 0.5);
    }
    
    /* Progress Bar */
    .progress-bar-bg { background: #222; border-radius: 10px; height: 12px; width: 100%; margin: 10px 0; overflow:hidden; }
    .progress-bar-fill { background: linear-gradient(90deg, #4caf50, #81c784); height: 100%; border-radius: 10px; }

    /* Keyframes for Animations */
    @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
    @keyframes explode { 0% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.5); opacity: 0.5; } 100% { transform: scale(2); opacity: 0; } }
    @keyframes rewardRise { 0% { transform: translateY(50px); opacity: 0; } 50% { transform: translateY(0); opacity: 1; } 100% { transform: translateY(-20px); opacity: 1; } }

    /* Mystery Box Pre-Open (Pulsing) */
    .mystery-crate-pulsing {
        background: linear-gradient(135deg, #b8860b, #1b5e20); padding: 25px; 
        border-radius: 20px; text-align: center; border: 3px solid #ffd700; margin-top: 15px; margin-bottom: 15px;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
        animation: pulse 2s infinite ease-in-out;
    }

    /* Exploding State */
    .mystery-crate-exploded {
        text-align: center; margin: 30px 0; animation: explode 0.8s ease-out;
    }

    /* Final Reward Visual (Text Rising & Coin Shower) */
    .reward-visual-container {
        text-align: center; padding: 20px; border-radius: 20px;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.2) 0%, rgba(0,0,0,0) 70%);
        border: 2px solid #ffd700; margin: 20px 0;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
        animation: rewardRise 1s ease-out;
    }
    
    /* Navigation Bar */
    .stRadio > div { flex-direction: row; justify-content: space-around; background: transparent; border: none; }
    .stRadio label { background-color: transparent !important; color: #4caf50 !important; font-weight: bold; font-size: 1.1rem; }
    .stRadio div[role="radiogroup"] { gap: 10px; }
    .stRadio input:checked + div { color: #ffd700 !important; font-size: 1.3rem; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
conn = sqlite3.connect("village_v36_visual.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS system_users (id TEXT PRIMARY KEY, reserves INTEGER, output_rate INTEGER, stage INTEGER)")
conn.commit()

session_user = "Murthy_Visual_Tycoon"
row = db.execute("SELECT reserves, output_rate, stage FROM system_users WHERE id = ?", (session_user,)).fetchone()

if not row:
    db.execute("INSERT INTO system_users VALUES (?, 5000, 0, 1)", (session_user,))
    conn.commit()
    reserves, output_rate, stage = 5000, 0, 1
else:
    reserves, output_rate, stage = row

# --- MATRIX ENGINE ---
CAPACITY_LIMIT = 10000
stage = 1 + (reserves // CAPACITY_LIMIT)
target_score = stage * CAPACITY_LIMIT
remaining_reserves = target_score - reserves

if stage == 1: stage_title = "Suburban Farmer 🌾"
elif stage == 2: stage_title = "Village Landlord 🚜"
else: stage_title = "AI Village Tycoon 👑"

db.execute("UPDATE system_users SET stage = ? WHERE id = ?", (stage, session_user))
conn.commit()

# --- TOP STATS INTERFACE ---
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-label">PROFIT PER HOUR</div><div class="stat-val">+{output_rate:,}</div></div>
        <div class="stat-box"><div class="stat-label">RANK TITLE</div><div class="stat-val" style="font-size:1.1rem; color:#4caf50;">{stage_title}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-coin-display">🪙 {reserves:,}</div>', unsafe_allow_html=True)

bar_ratio = int(((reserves % CAPACITY_LIMIT) / CAPACITY_LIMIT) * 100)
st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {bar_ratio}%;"></div></div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#81c784; font-size:0.9rem;'>🎯 <b>{remaining_reserves:,} Coins remaining</b> to unlock Level {stage + 1}</p>", unsafe_allow_html=True)

# Main Harvest Interactive Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=130)
    if st.button("🚜 HARVEST RICE (TAP) 🚜", use_container_width=True):
        reserves += (10 * stage)
        db.execute("UPDATE system_users SET reserves = ? WHERE id = ?", (reserves, session_user))
        conn.commit()
        st.rerun()

st.divider()

# Navigation Tabs (Horizontal Radio Style)
active_module = st.radio(
    "Destination Menu",
    ["🛒 Shop", "🎁 Mystery Box", "📋 Quests", "🏆 Ranks"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# --- MODULE ROUTING ---

if active_module == "🛒 Shop":
    st.markdown("### Production Infrastructure")
    st.info("Unlock advanced agricultural technology to increase passive income.")
    # Seeds
    seed_cost = 500 + (output_rate * 2)
    st.markdown(f"""<div class="upgrade-card"><div><div class="upgrade-title">Premium Seeds</div><div class="upgrade-desc">+100 Profit Per Hour</div></div><div class="upgrade-cost">🪙 {seed_cost:,}</div></div>""", unsafe_allow_html=True)
    if st.button("Purchase Seeds"):
        if reserves >= seed_cost:
            reserves -= seed_cost
            output_rate += 100
            db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
            conn.commit()
            st.toast("Seeds successfully planted!", icon="🌱")
            st.rerun()
        else:
            diff = seed_cost - reserves
            st.error(f"You need {diff:,} more coins for this upgrade.")

elif active_module == "🎁 Mystery Box":
    st.markdown("### Lucky Mystery Box")
    
    # Session state to manage the sequence of the extraordinary animation
    if 'mb_state' not in st.session_state: st.session_state.mb_state = 'ready'
    if 'mb_reward' not in st.session_state: st.session_state.mb_reward = None

    # Step 1: Ready to Open (Pulsing Crate)
    if st.session_state.mb_state == 'ready':
        st.markdown("""
            <div class="mystery-crate-pulsing">
                <h3 style="color:#ffd700; margin:0;">🎁 GOLDEN MYSTERY CRATE 🎁</h3>
                <p style="font-size:0.9rem; margin-top:5px; color:#eee;">Cost: 1,000 Coins<br>Open the crate to reveal guaranteed high-yield multipliers instantly!</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Mystery Box 📦", use_container_width=True):
            if reserves >= 1000:
                # Deduct, set state to explode, store reward
                reserves -= 1000
                reward_choice = random.choice(["grand_jackpot", "mega_win", "pph_boost"])
                st.session_state.mb_reward = reward_choice
                st.session_state.mb_state = 'exploding'
                
                db.execute("UPDATE system_users SET reserves = ? WHERE id = ?", (reserves, session_user))
                conn.commit()
                st.rerun()
            else:
                st.error("Insufficient balance! You need 1,000 coins to access this crate.")

    # Step 2: Explosion Animation
    elif st.session_state.mb_state == 'exploding':
        st.markdown("""<div class="mystery-crate-exploded"><h1 style="font-size:100px; margin:0;">💥</h1></div>""", unsafe_allow_html=True)
        # Briefly pause to allow the explosion visual to render before showing reward
        time.sleep(0.8)
        st.session_state.mb_state = 'reward'
        st.rerun()

    # Step 3: Extraordinary Reward Reveal (Rising Text & Coin Shower)
    elif st.session_state.mb_state == 'reward':
        reward_choice = st.session_state.mb_reward
        
        # Display localized visual based on stored reward configuration
        if reward_choice == "grand_jackpot":
            add_coins = 25000
            reserves += add_coins
            st.balloons()
            st.markdown(f"""
                <div class="reward-visual-container">
                    <h2 style="color:#ffd700; margin:0;">🎉 GRAND JACKPOT! 🎉</h2>
                    <h1 style="color:#ffffff; font-size:4rem; text-shadow:0 0 20px gold; margin:10px 0;">🪙 +{add_coins:,}</h1>
                    <p style="font-size:1.1rem; color:#eee;">Rice coins added to main balance!</p>
                </div>
            """, unsafe_allow_html=True)
        elif reward_choice == "mega_win":
            add_coins = 5000
            reserves += add_coins
            st.markdown(f"""
                <div class="reward-visual-container">
                    <h2 style="color:#ffd700; margin:0;">💰 MEGA WIN! 💰</h2>
                    <h1 style="color:#ffffff; font-size:3.5rem; text-shadow:0 0 15px gold; margin:10px 0;">🪙 +{add_coins:,}</h1>
                </div>
            """, unsafe_allow_html=True)
        elif reward_choice == "pph_boost":
            add_pph = 400
            output_rate += add_pph
            st.markdown(f"""
                <div class="reward-visual-container">
                    <h2 style="color:#4caf50; margin:0;">⚡ PRODUCTION BOOST! ⚡</h2>
                    <h1 style="color:#ffffff; font-size:3.5rem; text-shadow:0 0 15px #4caf50; margin:10px 0;">+ {add_pph:,} PPH</h1>
                </div>
            """, unsafe_allow_html=True)
        
        # Save new balance and reset state for next attempt
        db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
        conn.commit()
        st.session_state.mb_state = 'ready'
        st.session_state.mb_reward = None
        
        # Button to re-engage with the core game lifecycle
        if st.button("Return to Harvest", use_container_width=True): st.rerun()

elif active_module == "📋 Quests":
    st.markdown("### Daily Campaigns")
    st.info("Complete assignments to build your reserves quickly.")
    st.checkbox("Daily Check-in Bonus (Day 1 Claimed: +5,000 Coins)", value=True, disabled=True)
    if st.button("▶️ Watch Sponsored Media Stream (+1,000 Coins)"):
        reserves += 1000
        db.execute("UPDATE system_users SET reserves = ? WHERE id = ?", (reserves, session_user))
        conn.commit()
        st.toast("Task completed successfully!", icon="🪙")
        st.rerun()

elif active_module == "🏆 Ranks":
    st.markdown("### Worldwide Leaderboard")
    st.write("🥇 **Tycoon_King** - 15,403,000 Coins")
    st.write("🥈 **FarmMaster** - 12,110,500 Coins")
    st.write(f"⭐ **{session_user}** (You) - {reserves:,} Coins")

st.divider()
st.markdown('<p style="text-align:center; color:#4caf50; font-size:0.75rem; font-weight:bold;">VILLAGE MINING AI v3.6 • PLATINUM VISUAL EDITION</p>', unsafe_allow_html=True)
