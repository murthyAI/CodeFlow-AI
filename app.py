import streamlit as st
import sqlite3
import random

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- PLATINUM EXTRAORDINARY CSS ---
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
    
    .mystery-box {
        background: linear-gradient(135deg, #b8860b, #1b5e20); padding: 20px; 
        border-radius: 15px; text-align: center; border: 2px solid #ffd700; margin-top: 15px; margin-bottom: 15px;
    }
    .reward-popup {
        background: rgba(255, 215, 0, 0.1); padding: 15px; border-radius: 12px;
        border: 2px dashed #ffd700; text-align: center; margin: 15px 0;
        animation: pulse 1.5s infinite;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
conn = sqlite3.connect("village_v35_master.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS system_users (id TEXT PRIMARY KEY, reserves INTEGER, output_rate INTEGER, stage INTEGER)")
conn.commit()

session_user = "Murthy_Master_Tycoon"
row = db.execute("SELECT reserves, output_rate, stage FROM system_users WHERE id = ?", (session_user,)).fetchone()

if not row:
    db.execute("INSERT INTO system_users VALUES (?, 5000, 0, 1)", (session_user,))
    conn.commit()
    reserves, output_rate, stage = 5000, 0, 1
else:
    reserves, output_rate, stage = row

# --- LEVEL MATRIX CALCULATIONS ---
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

# Central Core Tap Mechanism
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=130)
    if st.button("🚜 HARVEST RICE (TAP) 🚜", use_container_width=True):
        reserves += (10 * stage)
        db.execute("UPDATE system_users SET reserves = ? WHERE id = ?", (reserves, session_user))
        conn.commit()
        st.rerun()

st.divider()

# --- REVOLUTIONARY NAVIGATION NAVIGATION MENU ---
# Session state initialized to persist menu choices smoothly
active_module = st.radio(
    "Select Destination Menu",
    ["🛒 Shop", "🎁 Mystery Box", "📋 Quests", "🏆 Ranks", "💰 Airdrop"],
    horizontal=True,
    label_visibility="collapsed"
)

st.divider()

# --- MENU ROUTING ---

if active_module == "🛒 Shop":
    st.markdown("### Production Upgrades")
    
    # Premium Hybrid Seeds
    pack_cost = 500 + (output_rate * 2)
    st.markdown(f"""
        <div class="upgrade-card">
            <div><div class="upgrade-title">Premium Hybrid Seeds</div><div class="upgrade-desc">+100 Profit Per Hour</div></div>
            <div class="upgrade-cost">🪙 {pack_cost:,}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Purchase Seeds", use_container_width=True):
        if reserves >= pack_cost:
            reserves -= pack_cost
            output_rate += 100
            db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
            conn.commit()
            st.toast("Seeds planted!", icon="🌱")
            st.rerun()
        else:
            diff = pack_cost - reserves
            st.error(f"❌ You need {diff:,} more coins to purchase this upgrade.")

    # Solar Irrigation Pumps
    grid_cost = 2500 + (output_rate * 5)
    st.markdown(f"""
        <div class="upgrade-card">
            <div><div class="upgrade-title">Solar Irrigation Pumps</div><div class="upgrade-desc">+500 Profit Per Hour</div></div>
            <div class="upgrade-cost">🪙 {grid_cost:,}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Install Irrigation", use_container_width=True):
        if reserves >= grid_cost:
            reserves -= grid_cost
            output_rate += 500
            db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
            conn.commit()
            st.toast("Irrigation activated!", icon="⚡")
            st.rerun()
        else:
            diff = grid_cost - reserves
            st.error(f"❌ You need {diff:,} more coins to install irrigation.")

elif active_module == "🎁 Mystery Box":
    st.markdown("### Lucky Mystery Box")
    st.markdown("""
        <div class="mystery-box">
            <h3 style="color:#ffd700; margin:0;">🎁 GOLDEN MYSTERY CRATE 🎁</h3>
            <p style="font-size:0.9rem; margin-top:5px; color:#eee;">Cost: 1,000 Coins<br>Open the crate to reveal your guaranteed reward instantly!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Open Mystery Box 📦", use_container_width=True):
        if reserves >= 1000:
            reserves -= 1000
            roll = random.choice(["coins_grand", "coins_mega", "pph_boost", "fertilizer"])
            
            # Save configuration to trigger localized display
            if roll == "coins_grand":
                reserves += 25000
                st.balloons()
                st.markdown("""<div class="reward-popup"><h2 style="color:#ffd700; margin:0;">🎉 GRAND JACKPOT! 🎉</h2><p style="font-size:1.3rem; margin:5px 0;">You discovered <b>🪙 25,000 Coins</b> inside!</p></div>""", unsafe_allow_html=True)
            elif roll == "coins_mega":
                reserves += 5000
                st.markdown("""<div class="reward-popup"><h2 style="color:#ffd700; margin:0;">💰 MEGA WIN! 💰</h2><p style="font-size:1.3rem; margin:5px 0;">You discovered <b>🪙 5,000 Coins</b> inside!</p></div>""", unsafe_allow_html=True)
            elif roll == "pph_boost":
                output_rate += 400
                st.markdown("""<div class="reward-popup"><h2 style="color:#4caf50; margin:0;">⚡ PRODUCTION BOOST! ⚡</h2><p style="font-size:1.3rem; margin:5px 0;">Found advanced automated tools! <b>+400 PPH</b> permanently!</p></div>""", unsafe_allow_html=True)
            else:
                reserves += 200 # Consolation prize
                st.markdown("""<div class="reward-popup"><h2 style="color:#aaa; margin:0;">📦 STANDARD ITEM 📦</h2><p style="font-size:1.2rem; margin:5px 0;">Found Premium Organic Fertilizer worth <b>🪙 200 Coins</b>!</p></div>""", unsafe_allow_html=True)
            
            db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
            conn.commit()
        else:
            diff = 1000 - reserves
            st.error(f"❌ You need {diff:,} more coins to unlock this crate.")

elif active_module == "📋 Quests":
    st.markdown("### Active Quests")
    st.info("Complete objectives to earn additional resources.")
    st.checkbox("Daily Check-in Bonus (Claimed: +5,000 Coins)", value=True, disabled=True)
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

elif active_module == "💰 Airdrop":
    st.markdown("### Blockchain Infrastructure")
    st.success("Allocation formulas will verify final Level Titles and PPH parameters.")
    st.button("🔗 Link TON Mainnet Wallet (Coming Soon)", disabled=True)

st.divider()
st.markdown('<p style="text-align:center; color:#4caf50; font-size:0.75rem; font-weight:bold;">VILLAGE MINING AI v3.5 • PLATINUM MASTER ENGINE</p>', unsafe_allow_html=True)
