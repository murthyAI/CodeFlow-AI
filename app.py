import streamlit as st
import sqlite3
import random
import time

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- CUSTOM CSS: THE ULTIMATE "HAMSTER KOMBAT & X-EMPIRE" LOOK ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Urbanist:wght@400;600;800&display=swap');
    
    /* Core Styling */
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at 50% 30%, #152e15 0%, #050f05 50%, #000000 100%); }
    
    /* Block Streamlit Default Elements */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    /* Premium Header Card */
    .premium-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 24px; padding: 16px; border: 1px solid rgba(76, 175, 80, 0.2);
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); margin-bottom: 15px;
    }
    .avatar-zone { width: 45px; height: 45px; border-radius: 50%; border: 2px solid #ffd700; background: #222; text-align: center; line-height: 42px; font-size: 24px; box-shadow: 0 0 10px rgba(255,215,0,0.4); }
    .rank-tag { background: linear-gradient(90deg, #ffd700, #b8860b); color: #000; font-size: 0.65rem; font-weight: 900; padding: 2px 8px; border-radius: 20px; text-transform: uppercase; margin-top: 2px; display: inline-block;}
    
    /* Stats Row (Hamster Style) */
    .stats-container { display: flex; gap: 12px; margin-bottom: 20px; }
    .stat-box { background: rgba(20,20,20,0.7); border: 1px solid #222; border-radius: 14px; padding: 10px; flex: 1; text-align: center; transition: all 0.3s; }
    .stat-box:hover { border-color: #4caf50; box-shadow: 0 0 12px rgba(76,175,80,0.2); }
    .stat-title { font-size: 0.6rem; color: #888; letter-spacing: 1px; margin-bottom: 2px; }
    .stat-number { font-size: 0.95rem; font-weight: 800; color: #ffd700; font-family: 'Orbitron', sans-serif; }

    /* Grand Coin Balance Display */
    .balance-wrapper { text-align: center; margin: 15px 0; }
    .coin-balance { font-size: 3.8rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron', sans-serif; text-shadow: 0 0 20px rgba(255,215,0,0.45); animation: pulse 2s infinite; }

    /* THE GLOWING TAPPER ENGINE (Center Coin) */
    .tapper-container { display: flex; justify-content: center; align-items: center; position: relative; margin: 25px 0; }
    .main-coin-glow {
        position: absolute; width: 230px; height: 230px; 
        background: radial-gradient(circle, rgba(76,175,80,0.4) 0%, rgba(0,0,0,0) 70%); 
        border-radius: 50%; filter: blur(20px); z-index: 1;
    }
    .hamster-coin-btn {
        z-index: 5; background: radial-gradient(circle, #2e7d32 0%, #1b5e20 100%);
        width: 200px; height: 200px; border-radius: 50%;
        border: 8px solid #ffd700; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 0 40px rgba(76,175,80,0.6), inset 0 0 20px rgba(0,0,0,0.6);
        cursor: pointer; transition: transform 0.05s active;
    }
    .hamster-coin-btn:active { transform: scale(0.92); filter: brightness(1.2); }
    .tapper-emoji { font-size: 95px; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5)); user-select: none; }

    /* Progress & Level Bar */
    .level-info { display: flex; justify-content: space-between; font-size: 0.75rem; color: #81c784; margin-bottom: 4px; font-weight: bold;}
    .bar-bg { background: #111; border-radius: 30px; height: 14px; width: 100%; border: 1px solid #333; overflow: hidden; margin-bottom: 25px;}
    .bar-fill { background: linear-gradient(90deg, #4caf50 0%, #81c784 50%, #ffd700 100%); height: 100%; box-shadow: 0 0 10px rgba(76,175,80,0.5); }

    /* Cards & Upgrades (X-Empire Style) */
    .section-headline { font-family: 'Orbitron', sans-serif; font-size: 1.1rem; font-weight: bold; color: #fff; margin-bottom: 12px; border-left: 4px solid #4caf50; padding-left: 8px; }
    .mystery-box-card {
        background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(0,0,0,0.4) 100%);
        border: 2px dashed #ffd700; border-radius: 20px; padding: 25px; text-align: center;
        box-shadow: 0 0 25px rgba(255,215,0,0.15); margin-bottom: 20px;
    }
    .premium-item-card {
        background: rgba(15,15,15,0.85); border: 1px solid #222; border-radius: 16px; padding: 14px;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;
    }
    .item-title { font-weight: bold; font-size: 0.95rem; color: #fff; }
    .item-desc { font-size: 0.7rem; color: #888; }
    .item-cost { color: #ffd700; font-weight: 800; font-family: 'Orbitron', sans-serif; font-size: 0.9rem; }

    /* FIXED DOCK NAVIGATION BAR (Hamster Style) */
    .dock-nav-bar {
        position: fixed; bottom: 0; left: 0; width: 100%; height: 75px;
        background: linear-gradient(to top, #000000 70%, #0c0c0c 100%);
        border-top: 1px solid rgba(255,255,255,0.08);
        display: flex; justify-content: space-around; align-items: center;
        z-index: 99999; padding-bottom: 12px; box-shadow: 0 -10px 30px rgba(0,0,0,0.9);
    }
    
    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.02); } 100% { transform: scale(1); } }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
conn = sqlite3.connect("village_tycoon_v50.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER)")
conn.commit()

USER_ID = "Murthy_Grand_Tycoon"
row = db.execute("SELECT coins, pph, level FROM users WHERE id = ?", (USER_ID,)).fetchone()
if not row:
    db.execute("INSERT INTO users VALUES (?, 5060, 500, 1)", (USER_ID,))
    conn.commit()
    coins, pph, level = 5060, 500, 1
else:
    coins, pph, level = row

# --- CLIENT-SIDE RE-CALCULATION ---
COINS_PER_LEVEL = 10000
level = 1 + (coins // COINS_PER_LEVEL)
next_level_target = level * COINS_PER_LEVEL
progress_percent = min(int(((coins % COINS_PER_LEVEL) / COINS_PER_LEVEL) * 100), 100)

if level == 1: level_title = "Bronze Farmer 🌾"
elif level == 2: level_title = "Silver Landlord 🚜"
else: level_title = "Gold Village Tycoon 👑"

# --- TOP PROFILE PATTERN ---
st.markdown(f"""
    <div class="premium-header">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="avatar-zone">👨‍🌾</div>
            <div>
                <div style="font-weight: 800; font-size: 0.95rem; color: #fff; letter-spacing: 0.5px;">{USER_ID}</div>
                <div class="rank-tag">{level_title}</div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.55rem; color: #888; letter-spacing: 1px;">AIRDROP SEASON 1</div>
            <div style="font-size: 0.8rem; color: #4caf50; font-weight: 900; font-family: 'Orbitron', sans-serif;">LIVE UNITS</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- HAMSTER-STYLE MULTI-STATS BAR ---
st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-title">PROFIT PER HOUR</div><div class="stat-number">⚡ +{pph:,}</div></div>
        <div class="stat-box"><div class="stat-title">GLOBAL RANK</div><div class="stat-number">#1,042</div></div>
        <div class="stat-box"><div class="stat-title">MULTIPLIER</div><div class="stat-number">x{level}</div></div>
    </div>
""", unsafe_allow_html=True)

# --- COIN MATRIX ---
st.markdown(f"""
    <div class="balance-wrapper">
        <div class="coin-balance">🪙 {coins:,}</div>
    </div>
""", unsafe_allow_html=True)

# --- NATIVE STREAMLIT MENU INTERFACE (REPLACES BROKEN TABS) ---
selected_tab = st.radio("DOCK_NAV", ["🎯 MINE", "🚀 BOOST & UPGRADES", "📜 QUESTS", "🏆 LEADERBOARD", "💎 AIRDROP"], horizontal=True, label_visibility="collapsed")

st.write("")

# --- CORE SYSTEMS ENGINE ---
if selected_tab == "🎯 MINE":
    # Level & Progress Mechanics
    st.markdown(f"""
        <div class="level-info">
            <div>Level {level}</div>
            <div>Next Level: {coins:,} / {next_level_target:,}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="bar-bg"><div class="bar-fill" style="width: {progress_percent}%;"></div></div>', unsafe_allow_html=True)
    
    # HAMSTER THEMED TAP BUTTON AREA
    st.markdown('<div class="tapper-container"><div class="main-coin-glow"></div></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Streamlit-safe structural button mapping simulation
        st.markdown("<p style='text-align:center; font-size:14px; color:#888; margin-bottom:-10px;'>TAP THE TRACTOR TO HARVEST</p>", unsafe_allow_html=True)
        if st.button("🚜", key="main_tap_btn", use_container_width=True):
            coins += (15 * level)
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.toast(f"+{15 * level} Coins Harvested!", icon="🪙")
            st.rerun()

elif selected_tab == "🚀 BOOST & UPGRADES":
    st.markdown('<div class="section-headline">GOLD REWARD CRATE</div>', unsafe_allow_html=True)
    
    if 'box_state' not in st.session_state: st.session_state.box_state = "closed"
    if 'prize_won' not in st.session_state: st.session_state.prize_won = None

    if st.session_state.box_state == "closed":
        st.markdown("""
            <div class="mystery-box-card">
                <h1 style="font-size: 70px; margin: 0;">🎁</h1>
                <h3 style="color:#ffd700; margin-top:10px;">Premium Mystery Box</h3>
                <p style="font-size:0.8rem; color:#aaa;">Costs 1,500 coins. Win massive token stacks or permanent hourly production boosts!</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🔓 Open Crate (1,500 Coins)", use_container_width=True):
            if coins >= 1500:
                coins -= 1500
                st.session_state.prize_won = random.choice(["jackpot", "boost_pack"])
                st.session_state.box_state = "opened"
                db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.rerun()
            else:
                st.error("❌ Not enough coins to unlock!")
    else:
        st.markdown('<div class="mystery-box-card">', unsafe_allow_html=True)
        if st.session_state.prize_won == "jackpot":
            coins += 30000
            st.balloons()
            st.markdown("<h1 style='font-size:70px; margin:0;'>🎉</h1><h2 style='color:#ffd700;'>GRAND CRYPTO JACKPOT!</h2><h1>🪙 +30,000</h1>", unsafe_allow_html=True)
        else:
            pph += 600
            st.markdown("<h1 style='font-size:70px; margin:0;'>⚡</h1><h2 style='color:#4caf50;'>PRODUCTION BOOSTED!</h2><h1>+600 Profit/Hour</h1>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, USER_ID))
        conn.commit()
        
        if st.button("Collect & Continue 🚜", use_container_width=True):
            st.session_state.box_state = "closed"
            st.session_state.prize_won = None
            st.rerun()

    # INFRASTRUCTURE UPGRADES MARKET
    st.write("")
    st.markdown('<div class="section-headline">UPGRADE BUSINESS DECK</div>', unsafe_allow_html=True)
    
    upgrade_cost = 800 + (pph * 3)
    st.markdown(f"""
        <div class="premium-item-card">
            <div>
                <div class="item-title">🚜 Next-Gen Drone Harvester</div>
                <div class="item-desc">+250 Profit Per Hour permanent capacity</div>
            </div>
            <div class="item-cost">🪙 {upgrade_cost:,}</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Buy Drone Upgrade Pack", use_container_width=True):
        if coins >= upgrade_cost:
            coins -= upgrade_cost
            pph += 250
            db.execute("UPDATE users SET coins = ?, pph = ? WHERE id = ?", (coins, pph, USER_ID))
            conn.commit()
            st.toast("Drone Upgrade Unlocked!", icon="🚀")
            st.rerun()
        else:
            st.error("❌ Insufficient funds for this business asset.")

elif selected_tab == "📜 QUESTS":
    st.markdown('<div class="section-headline">EARN REWARDS</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="premium-item-card">
            <div><div class="item-title">Daily Check-In Multiplier</div><div class="item-desc">Claim your daily production bonus stack</div></div>
            <div style="color:#4caf50; font-weight:bold;">+5,000</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Claim Daily Reward", use_container_width=True):
        coins += 5000
        db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
        conn.commit()
        st.toast("5,000 Coins added directly!", icon="🎁")
        st.rerun()

elif selected_tab == "🏆 LEADERBOARD":
    st.markdown('<div class="section-headline">TOP RURAL GLOBAL TYCOONS</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="premium-item-card"><div><b>🥇 Tycoon_King</b></div><div class="item-cost">15,403,000</div></div>
        <div class="premium-item-card"><div><b>🥈 FarmMaster_AI</b></div><div class="item-cost">12,110,500</div></div>
        <div class="premium-item-card" style="border: 1px solid #ffd700; background:rgba(255,215,0,0.05);"><div><b>⭐ {USER_ID} (YOU)</b></div><div class="item-cost">{coins:,}</div></div>
    """, unsafe_allow_html=True)

elif selected_tab == "💎 AIRDROP":
    st.markdown('<div class="section-headline">WEB3 DISTRIBUTION MATRIX</div>', unsafe_allow_html=True)
    st.info("Ecosystem mapping algorithm checks total Profit Per Hour (PPH) dynamically. Keep expanding your production grids before final distribution snapshot.")
    st.button("🔗 Bind TON Wallet Address (Coming Soon)", disabled=True, use_container_width=True)

# Padding space block for the bottom navigation tray
st.markdown("<br><br><br><br>", unsafe_allow_html=True)

# --- VISUAL HUD BAR OVERLAY LAYER ---
st.markdown("""
    <div class="dock-nav-bar">
        <div style="text-align:center; color:#ffd700;"><div style="font-size:1.3rem;">🎯</div><div style="font-size:0.6rem; font-weight:bold;">MINE</div></div>
        <div style="text-align:center; color:#888;"><div style="font-size:1.3rem;">🚀</div><div style="font-size:0.6rem; font-weight:bold;">BOOST</div></div>
        <div style="text-align:center; color:#888;"><div style="font-size:1.3rem;">📜</div><div style="font-size:0.6rem; font-weight:bold;">EARN</div></div>
        <div style="text-align:center; color:#888;"><div style="font-size:1.3rem;">🏆</div><div style="font-size:0.6rem; font-weight:bold;">FRENZ</div></div>
        <div style="text-align:center; color:#888;"><div style="font-size:1.3rem;">💎</div><div style="font-size:0.6rem; font-weight:bold;">AIRDROP</div></div>
    </div>
""", unsafe_allow_html=True)
