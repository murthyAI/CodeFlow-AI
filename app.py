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
        width: 170px; height: 170px; border-radius: 50%; margin: 10px auto;
        background: radial-gradient(circle, #2e7d32 10%, #1b5e20 80%);
        border: 6px solid #ffd700; display: flex; justify-content: center; align-items: center;
        box-shadow: 0 0 45px rgba(76, 175, 80, 0.7), inset 0 0 20px rgba(0,0,0,0.8);
        font-size: 80px; user-select: none;
    }
    
    .action-module-row-card {
        background: rgba(12,12,12,0.95); border: 1px solid #222; border-radius: 16px; padding: 15px;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }
    .module-card-headline { font-weight: 800; font-size: 0.95rem; color: #fff; }
    .module-card-sub { font-size: 0.7rem; color: #777; font-weight: bold; }
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
    .streak-day-box.active { border-color: #ffd700; background: rgba(255,215,0,0.05); }
    .streak-day-title { font-size: 10px; color: #aaa; font-weight: bold; }
    .streak-day-reward { font-size: 11px; color: #ffd700; font-family: 'Orbitron'; font-weight: 900; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE (v14.7 CLEAN PATCH) ---
# కన్ఫ్లిక్ట్స్ రాకుండా సరికొత్త వెర్షన్ నేమ్ సింక్ చేశాను
conn = sqlite3.connect("village_v14_7_final.db", check_same_thread=False)
db = conn.cursor()
db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, coins INTEGER, pph INTEGER, level INTEGER, 
        last_claim TEXT, streak_count INTEGER, energy INTEGER, 
        wallet_address TEXT, total_invites INTEGER, tractor_tier TEXT
    )
""")
conn.commit()

USER_ID = "Murthy_Grand_Tycoon"
row = db.execute("SELECT coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier FROM users WHERE id = ?", (USER_ID,)).fetchone()

if not row:
    db.execute("INSERT INTO users VALUES (?, 336365, 900, 4, '', 0, 500, '', 0, 'Basic Tractor')", (USER_ID,))
    conn.commit()
    coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier = 336365, 900, 4, "", 0, 500, "", 0, "Basic Tractor"
else:
    coins, pph, level, last_claim, streak_count, energy, wallet_address, total_invites, tractor_tier = row

# Fallback auto energy matrix
if energy is None or energy < 0:
    energy = 500

# --- SESSION STATE MANAGEMENT ---
if "won_reward" not in st.session_state:
    st.session_state.won_reward = None
if "claimed_tasks" not in st.session_state:
    st.session_state.claimed_tasks = set()

# --- COIN ENGINE & TIERS MIGRATION ---
COINS_PER_LEVEL = 100000  
MAX_SYSTEM_LEVELS = 10
calculated_level = 1 + (coins // COINS_PER_LEVEL)
level = min(calculated_level, MAX_SYSTEM_LEVELS)
next_target = level * COINS_PER_LEVEL
points_needed = max(0, next_target - coins)
progress_bar_val = min(int(((coins % COINS_PER_LEVEL) / COINS_PER_LEVEL) * 100), 100)

tractor_multiplier = 1
if tractor_tier == "Iron Tractor": tractor_multiplier = 2
elif tractor_tier == "Cyber Tractor": tractor_multiplier = 4

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
        <div class="dashboard-stat-unit"><div class="dashboard-stat-lbl">SKIN BOOST</div><div class="dashboard-stat-val">x{tractor_multiplier}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="grand-token-display"><div class="grand-token-val">🪙 {coins:,}</div></div>', unsafe_allow_html=True)

# --- NAVIGATION TABS ---
active_panel = st.segmented_control("Nav", ["🎯 MINE", "🚀 BOOST", "📜 QUESTS", "🏆 FRENZ", "💎 DROP"], selection_mode="single", default="🎯 MINE", label_visibility="collapsed")
st.divider()
current_date_stamp = datetime.now().strftime("%Y-%m-%d")

if active_panel == "🎯 MINE":
    st.session_state.won_reward = None
    if level < MAX_SYSTEM_LEVELS:
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
    
    st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px; font-weight:bold; font-size:13px;">
            <span style="color:#ffd700;">⚡ ENERGY: {energy} / 500</span>
            <span style="color:#777; font-size:11px;">Skin: {tractor_tier}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ TAP TRACTOR TO HARVEST COINS ⚡", key="harvest_v147", use_container_width=True):
        if energy >= 10:
            energy -= 10
            coins += (40 * level * tractor_multiplier)
            db.execute("UPDATE users SET coins = ?, energy = ? WHERE id = ?", (coins, energy, USER_ID))
            conn.commit()
            st.toast(f"🪙 +{40 * level * tractor_multiplier} Coins Harvested!", icon="🚜")
            st.rerun()
        else:
            st.error("❌ Out of Energy! Move tabs or refresh to auto-charge!")

elif active_panel == "🚀 BOOST":
    st.markdown("### 🚀 Premium Booster Engine")
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255,215,0,0.12) 0%, rgba(0,0,0,0.7) 100%); border: 2px dashed #ffd700; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0; font-size:45px;">🎁</h2>
            <h4 style="color:#ffd700; margin:5px 0; font-family:'Orbitron';">GOLD CRATE REVEAL</h4>
            <p style="font-size:0.7rem; color:#ccc; margin:0;">Costs 1,000 coins. Drop matrix luck chance: 2K, 5K, or 15K coins instantly!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔓 Open Premium Mystery Box (1,000 Coins)", key="crate_v147", use_container_width=True):
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
        st.markdown(f"""
            <div class="custom-reward-toast">
                <h1 style="margin:0; font-size:35px;">✨🪙✨</h1>
                <h3 style="color:#ffd700; margin:5px 0; font-family:'Orbitron'; font-weight:900;">CRATE UNLOCKED</h3>
                <h1 style="color:#ffffff; margin:5px 0; font-family:'Orbitron'; font-weight:900; font-size:30px;">+{st.session_state.won_reward:,} COINS</h1>
            </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.markdown("### 🚜 Upgrade Tractor Upgrades")
    
    # Iron tractor option
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
                
    # Cyber tractor option
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
            
    if last_claim == current_date_stamp:
        st.warning(f"🔒 Streak day {streak_count} claimed safely! Return tomorrow.")
    else:
        if st.button("🎁 CLAIM DAILY STREAK MILESTONE", use_container_width=True, key="claim_streak_btn"):
            next_streak = (streak_count % 7) + 1
            reward_granted = streak_rewards[next_streak - 1]
            coins += reward_granted
            db.execute("UPDATE users SET coins = ?, streak_count = ?, last_claim = ? WHERE id = ?", (coins, next_streak, current_date_stamp, USER_ID))
            conn.commit()
            st.balloons()
            st.success(f"Claimed Day {next_streak} Bonus! +{reward_granted:,} Coins added!")
            st.rerun()
            
    st.divider()
    st.markdown("### 📜 Social Media Missions")
    
    # Mission 1
    if "task1" in st.session_state.claimed_tasks:
        st.markdown("<div class='action-module-row-card'><div><b>✅ Join Telegram Channel</b></div><div style='color:#4caf50;'>Claimed</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='action-module-row-card'><div><b>📢 Join Official Telegram</b></div><div class='module-card-cost-index'>+50,000</div></div>", unsafe_allow_html=True)
        if st.button("Verify & Claim +50K Coins", key="t1"):
            coins += 50000
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.session_state.claimed_tasks.add("task1")
            st.toast("Task balance credited safely!", icon="✅")
            st.rerun()
            
    # Mission 2
    if "task2" in st.session_state.claimed_tasks:
        st.markdown("<div class='action-module-row-card'><div><b>✅ Follow X Community</b></div><div style='color:#4caf50;'>Claimed</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='action-module-row-card'><div><b>🐦 Follow X (Twitter) Node</b></div><div class='module-card-cost-index'>+30,000</div></div>", unsafe_allow_html=True)
        if st.button("Verify & Claim +30K Coins", key="t2"):
            coins += 30000
            db.execute("UPDATE users SET coins = ? WHERE id = ?", (coins, USER_ID))
            conn.commit()
            st.session_state.claimed_tasks.add("task2")
            st.toast("Task balance credited safely!", icon="✅")
            st.rerun()

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
    if st.button("🔗 SHARE REFERRAL LINK", use_container_width=True):
        st.toast("Referral code copied seamlessly!", icon="🚀")
        
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
                <p style="font-size:11px; color:#aaa; margin:5px 0 0 0;">Status: ELIGIBLE. Simulated transaction verification task unlockable in August 2026.</p>
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
        if st.button("🔗 LINK WALLET NODE ADDRESS", use_container_width=True, key="save_wallet_address_v147"):
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
