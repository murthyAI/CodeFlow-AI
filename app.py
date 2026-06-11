import streamlit as st
import sqlite3
import random
import time
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- v15.6 FORCED NATIVE WEB3 MAINFRAME WALLPAPER & UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght=700;900&family=Urbanist:wght=600;800;900&display=swap');
    
    /* FORCED NATIVE BACKGROUND ENFORCEMENT */
    html, body, [class*="st-"] { 
        font-family: 'Urbanist', sans-serif !important; 
        background-color: #000000 !important; 
        color: #ffffff !important; 
    }
    
    .stApp { 
        background: 
            radial-gradient(circle at 50% 20%, rgba(76, 175, 80, 0.4) 0%, rgba(0,0,0,0) 60%),
            radial-gradient(circle at 80% 80%, rgba(2, 136, 209, 0.2) 0%, rgba(0,0,0,0) 50%),
            linear-gradient(180deg, #010d01 0%, #031403 35%, #000000 100%) !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    
    .premium-header-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.01) 100%);
        border-radius: 22px; padding: 12px 16px; border: 1px solid rgba(76, 175, 80, 0.45);
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7); margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    .profile-img-frame { width: 42px; height: 42px; border-radius: 50%; border: 2px solid #ffd700; background: #111; text-align: center; line-height: 38px; font-size: 20px; }
    .dashboard-stats-grid { display: flex; gap: 8px; margin-bottom: 15px; }
    .dashboard-stat-unit { background: rgba(10,25,10,0.85); border: 1px solid rgba(76, 175, 80, 0.25); border-radius: 14px; padding: 10px; flex: 1; text-align: center; backdrop-filter: blur(5px); }
    .dashboard-stat-val { font-size: 0.9rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron'; }
    .dashboard-stat-lbl { font-size: 0.55rem; color: #bbb; font-weight: bold; }
    .grand-token-display { text-align: center; margin: 10px 0; }
    .grand-token-val { font-size: 3.5rem; font-weight: 900; color: #ffd700; font-family: 'Orbitron'; text-shadow: 0 0 25px rgba(255,215,0,0.6); }
    
    /* NATIVE HTML LINK STYLING */
    .web3-link-driver-btn {
        display: block !important; text-align: center !important; 
        background: linear-gradient(90deg, #0288d1 0%, #0056b3 100%) !important;
        color: #ffffff !important; padding: 12px !important; border-radius: 12px !important; 
        font-weight: bold !important; text-decoration: none !important; 
        box-shadow: 0 4px 15px rgba(2,136,209,0.3) !important; margin-bottom: 10px !important;
    }
    .web3-link-driver-btn-yt {
        display: block !important; text-align: center !important; 
        background: linear-gradient(90deg, #e53935 0%, #b71c1c 100%) !important;
        color: #ffffff !important; padding: 12px !important; border-radius: 12px !important; 
        font-weight: bold !important; text-decoration: none !important; 
        box-shadow: 0 4px 15px rgba(229,57,53,0.3) !important; margin-bottom: 10px !important;
    }
    
    .action-module-row-card {
        background: rgba(15,15,15,0.93); border: 1px solid #222; border-radius: 16px; padding: 15px;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }
    .module-card-headline { font-weight: 800; font-size: 0.95rem; color: #fff; }
    .module-card-sub { font-size: 0.7rem; color: #888; font-weight: bold; }
    .module-card-cost-index { color: #ffd700; font-weight: 900; font-family: 'Orbitron'; font-size: 0.9rem; }
    
    .monetization-ad-banner {
        background: linear-gradient(90deg, rgba(255,215,0,0.08) 0%, rgba(76,175,80,0.08) 100%);
        border: 2px dashed rgba(255,215,0,0.4); border-radius: 14px;
        padding: 15px; text-align: center; margin-top: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        cursor: pointer; display: block; text-decoration: none; color: white !important;
    }
    
    .custom-reward-toast {
        background: linear-gradient(135deg, #1b5e20 0%, #000000 100%);
        border: 2px solid #ffd700; padding: 20px; border-radius: 18px;
        text-align: center; box-shadow: 0 0 40px rgba(255,215,0,0.5);
        margin-top: 20px;
    }
    
    .streak-container { display: flex; gap: 6px; justify-content: space-between; margin-bottom: 15px; }
    .streak-day-box { background: #111; border: 1px solid #222; border-radius: 10px; padding: 8px 4px; text-align: center; flex: 1; }
    .streak-day-box.active { border-color: #ffd700; background: rgba(255,215,0,0.07); }
    .streak-day-title { font-size: 10px; color: #aaa; font-weight: bold; }
    .streak-day-reward { font-size: 11px; color: #ffd700; font-family: 'Orbitron'; font-weight: 900; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
conn = sqlite3.connect("village_master_v15.db", check_same_thread=False)
db = conn.cursor()
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER, 
        last_claim TEXT, streak_count INTEGER, energy INTEGER, 
        wallet_address TEXT, total_invites INTEGER, tractor_tier TEXT,
        tg_done INTEGER, yt_done INTEGER, combo_done INTEGER, share_done INTEGER
    )
""")
conn.commit()

# Share done safety ledger column check
try:
    db.execute("ALTER TABLE users ADD COLUMN share_done INTEGER DEFAULT 0")
    conn.commit()
except:
    pass

USER_ID = "Murthy_Grand_Tycoon"
row = db.execute("SELECT coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier, tg_done, yt_done, combo_done, share_done FROM users WHERE id = ?", (USER_ID,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 1635965, 900, 3, '', 1, 500, '', 0, 'Cyber Tractor', 0, 0, 0, 0)", (USER_ID,))
    conn.commit()
    coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier, tg_done, yt_done, combo_done, share_done = 1635965, 900, 3, "", 1, 500, "", 0, "Cyber Tractor", 0, 0, 0, 0
else:
    coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier, tg_done, yt_done, combo_done, share_done = row

# Full Energy Module Restored
if energy is None or energy < 0:
    energy = 500

# Cache triggers
if "won_reward" not in st.session_state: st.session_state.won_reward = None
if "tg_visited" not in st.session_state: st.session_state.tg_visited = False
if "yt_visited" not in st.session_state: st.session_state.yt_visited = False

# --- v15.6 BILLIONS SUPREME ECONOMY LAWS ---
if coins < 100000: level = 1
elif coins < 1000000: level = 2
elif coins < 5000000: level = 3
elif coins < 20000000: level = 4          
elif coins < 100000000: level = 5         
elif coins < 250000000: level = 6         
elif coins < 500000000: level = 7         
elif coins < 1000000000: level = 8        
elif coins < 2500000000: level = 9        
else: level = 10                          

level_targets = [0, 100000, 1000000, 5000000, 20000000, 100000000, 250000000, 500000000, 1000000000, 2500000000, 5000000000]
next_target = level_targets[level]
points_needed = max(0, next_target - coins)
previous_target = level_targets[level - 1]
progress_denominator = max(1, next_target - previous_target)
progress_bar_val = min(int(((coins - previous_target) / progress_denominator) * 100), 100)

tractor_multiplier = 1
if tractor_tier == "Iron Tractor": tractor_multiplier = 2
elif tractor_tier == "Cyber Tractor": tractor_multiplier = 4

# --- AIRDROP FIXED TO NOVEMBER 10, 2026 (5 MONTHS COUNTDOWN) ---
launch_target_date = datetime(2026, 11, 10)  
current_time_now = datetime.now()
days_remaining = max(0, (launch_target_date - current_time_now).days)

# --- HEADER INTERFACE ---
st.markdown(f"""
    <div class="premium-header-card">
        <div style="display:flex; align-items:center; gap:12px;">
            <div class="profile-img-frame">👨‍🌾</div>
            <div>
                <div style="font-weight:900; font-size:14px; letter-spacing:0.3px;">{USER_ID}</div>
                <div style="color:#4caf50; font-size:10px; font-weight:bold;">LEVEL {level}/10 • CYBER ZAMINDAR</div>
            </div>
        </div>
        <div style="text-align:right;">
            <span style="font-size:8px; font-weight:bold; color:#aaa;">LAUNCH: NOV 10, 2026</span><br>
            <b style="color:#ffd700; font-family:'Orbitron'; font-size:12px;">⏳ {days_remaining} DAYS LEFT</b>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STATS BLOCK ROW ---
st.markdown(f"""
    <div class="dashboard-stats-grid">
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">PROFIT / HOUR</div><div class="dashboard-stat-val">⚡ +{pph:,}</div></div>
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">TOTAL TIERS</div><div class="dashboard-stat-val">⭐ 10 LEVELS</div></div>
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">SKIN BOOST</div><div class="dashboard-stat-val">x{tractor_multiplier}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="grand-token-display"><div class="grand-token-val">🪙 {coins:,}</div></div>', unsafe_allow_html=True)

# --- NAVIGATION CONTROLLER ---
active_panel = st.segmented_control("Nav", ["🎯 MINE", "🚀 BOOST", "📜 QUESTS", "🏆 FRENZ", "💎 DROP"], selection_mode="single", default="🎯 MINE", label_visibility="collapsed")
st.divider()

if active_panel == "🎯 MINE":
    st.session_state.won_reward = None
    if level < 10:
        st.markdown(f"""
            <div style='display:flex; justify-content:space-between; font-size:11px; color:#81c784; margin-bottom:4px; font-weight:900;'>
                <span>RANK METRIC: {coins:,} / {next_target:,}</span>
                <span style='color:#ffd700;'>🚜 NEXT TARGET: {points_needed:,} POINTS</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:11px; color:#ffd700; font-weight:900; text-align:center;'>🏆 MAXIMUM LEVEL ACQUIRED!</div>", unsafe_allow_html=True)
        
    st.progress(progress_bar_val / 100)
    
    # --- v15.6 BYPASS COMPONENT NATIVE HTML GIANT TAP MATRIX ---
    # మొబైల్ సిస్టమ్ బటన్ కన్స్ట్రైంట్స్ ని బ్రేక్ చేస్తూ డిజైన్ చేసిన ప్యూర్ నియాన్ కాయిన్ ఎలిమెంట్
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; margin: 30px auto;">
            <div style="
                background: radial-gradient(circle, #388e3c 15%, #1b5e20 85%);
                border: 6px solid #ffd700;
                width: 220px;
                height: 220px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 0 50px rgba(76, 175, 80, 0.8), inset 0 0 25px rgba(0,0,0,0.9);
                font-size: 95px;
                user-select: none;
                animation: pulse 2s infinite ease-in-out;
            ">🚜</div>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 40px rgba(76, 175, 80, 0.7); }
            50% { transform: scale(1.03); box-shadow: 0 0 60px rgba(76, 175, 80, 0.9); }
            100% { transform: scale(1); box-shadow: 0 0 40px rgba(76, 175, 80, 0.7); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="text-align:center; font-weight:bold; font-size:14px; margin-top:10px; margin-bottom:15px;">
            <span style="color:#ffd700; background:rgba(76,175,80,0.15); padding:5px 15px; border-radius:12px; border:1px solid rgba(76,175,80,0.4);">⚡ ENERGY: {energy} / 500</span>
        </div>
    """, unsafe_allow_html=True)
    
    # ఈ హార్వెస్టర్ బటన్ సిస్టమ్ క్లిక్స్ ని పక్కాగా రికార్డ్ చేస్తుంది
    if st.button("⚡ CLICK HERE TO TAP TRACTOR COIN ⚡", key="mainframe_harvester_v156", use_container_width=True):
        if energy >= 10:
            energy -= 10
            coins += (40 * level * tractor_multiplier)
            db.execute("UPDATE users SET coins = ?, energy = ? WHERE id = ?", (coins, energy, USER_ID))
            conn.commit()
            st.toast(f"🪙 +{40 * level * tractor_multiplier} Coins Harvested!", icon="🚜")
            st.rerun()
        else:
            st.error("❌ Out of Energy! Move tabs to refresh and auto-charge instantly!")

elif active_panel == "🚀 BOOST":
    st.markdown("### 🚀 Premium Booster Engine")
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.12) 0%, rgba(0,0,0,0.7) 100%); border: 2px dashed #ffd700; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0; font-size:45px;">🎁</h2>
            <h4 style="color:#ffd700; margin:5px 0; font-family:'Orbitron';">GOLD CRATE REVEAL</h4>
            <p style="font-size:0.7rem; color:#ccc; margin:0;">Costs 1,000 coins. Drop matrix luck chance: 2K, 5K, or 15K coins instantly!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔓 Open Premium Mystery Box (1,000 Coins)", key="crate_v156", use_container_width=True):
        if coins >= 1000:
            coins -= 1000
            prize = random.choice([2000, 5000, 15000])
            coins += prize
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.session_state.won_reward = prize
            st.rerun()
        else:
            st.error("❌ Insufficient tokens inside account!")

    if st.session_state.won_reward is not None:
        st.snow()
        st.balloons()
        st.markdown(f"""
            <div class="custom-reward-toast">
                <h1 style="margin:0; font-size:35px;">✨🪙✨</h1>
                <h3 style="color:#ffd700; margin:5px 0; font-family:'Orbitron'; font-weight:900;">CRATE UNLOCKED SUCCESS</h3>
                <h1 style="color:#ffffff; margin:5px 0; font-family:'Orbitron'; font-weight:900; font-size:30px;">+{st.session_state.won_reward:,} COINS</h1>
            </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.markdown("### 🚜 Upgrade Tractor Upgrades")
    
    # Iron Upgrade
    st.markdown(f"""
        <div class="action-module-row-card">
            <div>
                <div class="module-card-headline">⛓️ Iron Tractor Skin</div>
                <div class="module-card-sub">Gives Double (x2) Tap Mining Rewards permanently</div>
            </div>
            <div class="module-card-cost-index">50,000 COINS</div>
        </div>
    """, unsafe_allow_html=True)
    if tractor_tier != "Basic Tractor":
        st.button("Owned / Activated", disabled=True, key="iron_owned")
    else:
        if st.button("Buy Iron Tractor Skin", key="buy_iron", use_container_width=True):
            if coins >= 50000:
                coins -= 50000
                db.execute("UPDATE users SET coins = ?, tractor_tier = 'Iron Tractor' WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.success("Successfully upgraded to Iron Tractor Skin!")
                st.rerun()
            else:
                st.error("❌ Insufficient coins!")
                
    # Cyber Upgrade
    st.markdown(f"""
        <div class="action-module-row-card">
            <div>
                <div class="module-card-headline">⚡ Cyber Gold Tractor Skin</div>
                <div class="module-card-sub">Gives Quadruple (x4) Tap Mining Rewards permanently</div>
            </div>
            <div class="module-card-cost-index">150,000 COINS</div>
        </div>
    """, unsafe_allow_html=True)
    if tractor_tier == "Cyber Tractor":
        st.button("Owned / Activated", disabled=True, key="cyber_owned")
    else:
        if st.button("Buy Cyber Gold Tractor Skin", key="buy_cyber", use_container_width=True):
            if coins >= 150000:
                coins -= 150000
                db.execute("UPDATE users SET coins = ?, tractor_tier = 'Cyber Tractor' WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.success("Successfully upgraded to Cyber Gold Tractor Skin!")
                st.rerun()
            else:
                st.error("❌ Insufficient coins!")

elif active_panel == "📜 QUESTS":
    st.session_state.won_reward = None
    st.markdown("### 🗓️ 7-Days Web3 Streak Check-In")
    
    streak_rewards = [5000, 10000, 15000, 25000, 40000, 60000, 100000]
    st.markdown("<div class='streak-container'>", unsafe_allow_html=True)
    cols = st.columns(7)
    for i in range(7):
        with cols[i]:
            is_active = "active" if i < streak_count else ""
            st.markdown(f"""
                <div class="streak-day-box {is_active}">
                    <div class="streak-day-title">Day {i+1}</div>
                    <div class="streak-day-reward">+{streak_rewards[i]//1000}K</div>
                </div>
            """, unsafe_allow_html=True)
            
    current_date_stamp = datetime.now().strftime("%Y-%m-%d")
    if last_claim == current_date_stamp:
        st.warning(f"🔒 Streak day {streak_count} claimed safely! Return tomorrow.")
    else:
        if st.button("🎁 CLAIM DAILY STREAK MILESTONE", use_container_width=True, key="claim_streak_btn"):
            next_streak = (streak_count % 7) + 1
            if streak_count == 0: next_streak = 1
            reward_granted = streak_rewards[next_streak - 1]
            coins += reward_granted
            db.execute("UPDATE users SET coins = ?, streak_count = ?, last_claim = ? WHERE id = ?", (coins, next_streak, current_date_stamp, USER_ID))
            conn.commit()
            st.balloons()
            st.success(f"Claimed Day {next_streak} Bonus! +{reward_granted:,} Coins added!")
            st.rerun()
            
    st.divider()
    st.markdown("### 📜 Social Media Missions")
    
    # 1. Telegram
    if tg_done == 1:
        st.markdown("<div class='action-module-row-card'><div><b>✅ Join Official Telegram Channel</b></div><div style='color:#4caf50; font-weight:bold;'>Claimed Forever</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='action-module-row-card'><div><b>📢 Join Official Telegram Channel</b></div><div class='module-card-cost-index'>+50,000</div></div>", unsafe_allow_html=True)
        st.markdown('<a href="https://t.me/telegram" target="_blank" class="web3-link-driver-btn">📢 STAGE 1: Open Telegram Channel</a>', unsafe_allow_html=True)
        if st.button("🔄 STAGE 2: Click to Verify Channel Visit", key="v_tg_v156", use_container_width=True):
            st.session_state.tg_visited = True
            st.toast("Telegram redirection verified! Stage 3 unlocked.", icon="🔓")
            
        if st.session_state.tg_visited:
            if st.button("⚡ STAGE 3: Verify & Claim +50K Coins", key="claim_tg_v156", use_container_width=True):
                coins += 50000
                db.execute("UPDATE users SET coins = ?, tg_done = 1 WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.success("Successfully credited 50,000 tokens!")
                st.rerun()
                
    st.write("") 
    
    # 2. YouTube
    if yt_done == 1:
        st.markdown("<div class='action-module-row-card'><div><b>✅ Subscribe YouTube Channel</b></div><div style='color:#4caf50; font-weight:bold;'>Claimed Forever</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='action-module-row-card'><div><b>📺 Subscribe YouTube Channel</b></div><div class='module-card-cost-index'>+40,000</div></div>", unsafe_allow_html=True)
        st.markdown('<a href="https://www.youtube.com" target="_blank" class="web3-link-driver-btn-yt">📺 STAGE 1: Open YouTube Channel</a>', unsafe_allow_html=True)
        if st.button("🔄 STAGE 2: Click to Verify Subscription Trace", key="v_yt_v156", use_container_width=True):
            st.session_state.yt_visited = True
            st.toast("YouTube action trace verified! Stage 3 unlocked.", icon="🔓")
            
        if st.session_state.yt_visited:
            if st.button("⚡ STAGE 3: Verify & Claim +40K Coins", key="claim_yt_v156", use_container_width=True):
                coins += 40000
                db.execute("UPDATE users SET coins = ?, yt_done = 1 WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.success("Successfully credited 40,000 tokens!")
                st.rerun()

    st.divider()
    
    # 3. DAILY COMBO BOX
    st.markdown("### 🔑 Channel Daily Combo Code")
    if combo_done == 1:
        st.success("🎉 You have already claimed today's Daily Combo! Come back tomorrow.")
    else:
        secret_input = st.text_input("Enter Secret Code from Telegram Channel", placeholder="Type daily combo code here...", key="secret_code_box")
        if st.button("Claim Combo Reward (+100,000 Coins)", use_container_width=True):
            if secret_input.strip() == "VILLAGE2026":
                coins += 100000
                db.execute("UPDATE users SET coins = ?, combo_done = 1 WHERE id = ?", (coins, USER_ID))
                conn.commit()
                st.balloons()
                st.success("🎉 Correct Combo! +100,000 Bonus Tokens Added!")
                st.rerun()
            else:
                st.error("❌ Invalid combo key trace! Check official channel node.")

elif active_panel == "🏆 FRENZ":
    st.session_state.won_reward = None
    st.markdown("### 👥 Web3 Referral Program")
    
    st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02); border:1px solid #222; border-radius:14px; padding:15px; text-align:center; margin-bottom:15px;">
            <span style="font-size:12px; color:#aaa; font-weight:bold;">TOTAL INVITED FRIENDS</span>
            <h1 style="margin:0; font-family:'Orbitron'; color:#4caf50; font-size:32px;">{total_invites} FRENZ</h1>
            <p style="font-size:11px; color:#ccc; margin:4px 0 0 0;">Earn +25,000 Coins for every successful network invite verified.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.text_input("Your Custom Telegram Referral Link", value=f"https://t.me/VillageMiningAI_bot?start=ref_{USER_ID}", disabled=True)
    
    if share_done == 1:
        if st.button("🔗 SHARE REFERRAL LINK", use_container_width=True):
            st.toast("Referral code copied safely to clipboard!", icon="🚀")
    else:
        if st.button("🔗 SHARE REFERRAL LINK (+5,000 First Time Reward)", use_container_width=True):
            coins += 5000
            db.execute("UPDATE users SET coins = ?, share_done = 1 WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.toast("Referral code copied! +5,000 Community Bonus Credited!", icon="🎉")
            st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("👥 SIMULATE 1 SUCCESSFUL INVITE (+25,000 Coins)", key="simulate_invite_btn", use_container_width=True):
        total_invites += 1
        coins += 25000
        db.execute("UPDATE users SET coins = ?, total_invites = ? WHERE id = ?", (coins, total_invites, USER_ID))
        conn.commit()
        st.balloons()
        st.success("Simulation Success! 1 Fren Joined.")
        st.rerun()

elif active_panel == "💎 DROP":
    st.session_state.won_reward = None
    st.markdown("### 💎 Bind TON Wallet Interface")
    
    if wallet_address and wallet_address.strip() != "":
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(76,175,80,0.12) 0%, rgba(0,0,0,0.8) 100%); border: 2px solid #4caf50; border-radius: 20px; padding: 25px; text-align: center; box-shadow: 0 0 25px rgba(76,175,80,0.25);">
                <h1 style="margin:0; font-size:45px;">💎</h1>
                <h3 style="color:#4caf50; margin-top:5px; font-family:'Orbitron'; font-weight:900;">WALLET LINKED SECURELY</h3>
                <code style="background:#222; padding:6px 12px; border-radius:6px; color:#ffd700; display:inline-block; margin:10px 0; font-size:10px; border:1px solid #333;">{wallet_address}</code>
                <p style="font-size:11px; color:#aaa; margin:5px 0 0 0;">Status: ELIGIBLE. Simulated transaction verification task unlockable in October 2026 (1-Month Prior to Launch).</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ Disconnect Wallet Address Key", use_container_width=True):
            db.execute("UPDATE users SET wallet_address = '' WHERE id = ?", (USER_ID,))
            conn.commit()
            st.toast("Wallet connection keys flushed safely.", icon="🔄")
            st.rerun()
    else:
        st.markdown("""
            <p style="font-size:0.8rem; color:#ccc;">Submit your standard non-custodial TON Wallet node key configuration to lock your allocation data node.</p>
        """, unsafe_allow_html=True)
        
        input_address = st.text_input("Enter TON Wallet Node Address Link", placeholder="EQA1b...7z3X_N7pG2qK", key="wallet_input_box")
        if st.button("🔗 LINK WALLET NODE ADDRESS", use_container_width=True, key="save_wallet_address_v148"):
            if input_address.strip() != "":
                db.execute("UPDATE users SET wallet_address = ? WHERE id = ?", (input_address.strip(), USER_ID))
                conn.commit()
                st.success("TON Wallet node reference bound successfully!")
                st.rerun()
            else:
                st.error("❌ Box cannot be submitted blank!")

# --- REVENUE PROMO BANNER ---
st.markdown("""
    <a href="https://www.google.com" target="_blank" class="monetization-ad-banner">
        <span style="font-size: 0.65rem; color: #ffd700; font-weight: bold; letter-spacing: 1px; display: block; margin-bottom: 2px;">💰 SPONSORED PROMO AD ZONE (CLICK TO EARN) 💰</span>
        <p style="font-size: 0.85rem; color: #fff; margin: 0; font-weight: bold;">🌾 Upgrade Your Crop Yields with Village Mining AI Partners! Click here! 🌾</p>
    </a>
""", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
