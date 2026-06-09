import streamlit as st
import sqlite3
import random

# --- APP CONFIG ---
st.set_page_config(page_title="Village Mining AI", page_icon="🌾", layout="centered")

# --- CUSTOM PLATINUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Urbanist', sans-serif; background-color: #000000; color: #ffffff; }
    .stApp { background: radial-gradient(circle at center, #0f2310 0%, #000000 100%); }
    
    .stats-container {
        display: flex; justify-content: space-around; background: rgba(255,255,255,0.03);
        padding: 15px; border-radius: 20px; border: 1px solid #4caf50; margin-bottom: 20px;
    }
    .stat-box { text-align: center; }
    .stat-val { font-size: 1.6rem; font-weight: 700; color: #ffd700; }
    .stat-label { font-size: 0.75rem; color: #aaa; letter-spacing: 1px; }

    .main-coin-display {
        text-align: center; font-size: 4.5rem; font-weight: 800; color: #ffd700; margin: 15px 0;
    }
    
    .progress-bar-bg { background: #222; border-radius: 10px; height: 12px; width: 100%; margin: 10px 0; overflow:hidden; }
    .progress-bar-fill { background: linear-gradient(90deg, #4caf50, #81c784); height: 100%; border-radius: 10px; }

    .section-header {
        font-size: 1.6rem; font-weight: 700; color: #4caf50; margin-top: 30px; margin-bottom: 15px;
        border-bottom: 2px solid #2e7d32; padding-bottom: 5px;
    }

    .upgrade-card {
        background: rgba(20,20,20,0.8); padding: 18px; border-radius: 15px; border: 1px solid #2e7d32; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
    }
    
    .mystery-box {
        background: linear-gradient(135deg, #b8860b, #1b5e20); padding: 20px; 
        border-radius: 15px; text-align: center; border: 2px solid #ffd700; margin-top: 15px; margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE (FRESH ISOLATED TABLE) ---
conn = sqlite3.connect("village_v34_final.db", check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS system_users (id TEXT PRIMARY KEY, reserves INTEGER, output_rate INTEGER, stage INTEGER)")
conn.commit()

session_user = "Murthy_Final_Tycoon"
row = db.execute("SELECT reserves, output_rate, stage FROM system_users WHERE id = ?", (session_user,)).fetchone()

if not row:
    db.execute("INSERT INTO system_users VALUES (?, 1000, 0, 1)", (session_user,))
    conn.commit()
    reserves, output_rate, stage = 1000, 0, 1
else:
    reserves, output_rate, stage = row

# --- LEVEL CALCULATIONS ---
CAPACITY_LIMIT = 10000 
stage = 1 + (reserves // CAPACITY_LIMIT)
target_score = stage * CAPACITY_LIMIT
remaining_reserves = target_score - reserves

if stage == 1: stage_title = "Suburban Farmer 🌾"
elif stage == 2: stage_title = "Village Landlord 🚜"
else: stage_title = "AI Village Tycoon 👑"

db.execute("UPDATE system_users SET stage = ? WHERE id = ?", (stage, session_user))
conn.commit()

# --- MAIN DASHBOARD UI ---

st.markdown(f"""
    <div class="stats-container">
        <div class="stat-box"><div class="stat-label">PROFIT PER HOUR</div><div class="stat-val">+{output_rate:,}</div></div>
        <div class="stat-box"><div class="stat-label">RANK TITLE</div><div class="stat-val" style="color:#4caf50;">{stage_title}</div></div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-coin-display">🪙 {reserves:,}</div>', unsafe_allow_html=True)

bar_ratio = int(((reserves % CAPACITY_LIMIT) / CAPACITY_LIMIT) * 100)
st.markdown(f'<div class="progress-bar-bg"><div class="progress-bar-fill" style="width: {bar_ratio}%;"></div></div>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#81c784; font-size:0.9rem;'>🎯 <b>{remaining_reserves:,} Coins remaining</b> to unlock Level {stage + 1}</p>", unsafe_allow_html=True)

# Harvest Tapping Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/2424/2424750.png", width=130)
    if st.button("🚜 HARVEST RICE (TAP) 🚜", use_container_width=True):
        reserves += (10 * stage)
        db.execute("UPDATE system_users SET reserves = ? WHERE id = ?", (reserves, session_user))
        conn.commit()
        st.rerun()

# --- SECTION 1: MYSTERY BOX (FORCED ON MAIN PAGE) ---
st.markdown('<div class="section-header">🎁 Lucky Rewards</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="mystery-box">
        <h3 style="color:#ffd700; margin:0;">🎁 GOLDEN MYSTERY CRATE 🎁</h3>
        <p style="font-size:0.9rem; margin-top:5px; color:#eee;">Cost: 1,000 Coins • Win up to 50,000 Coins or huge PPH boosts instantly!</p>
    </div>
""", unsafe_allow_html=True)

if st.button("Open Mystery Box 📦", use_container_width=True):
    if reserves >= 1000:
        reserves -= 1000
        roll = random.choice(["reserves", "output_rate", "null"])
        if roll == "reserves":
            bonus = random.choice([5000, 10000, 25000, 50000])
            reserves += bonus
            st.balloons()
            st.success(f"🎉 JACKPOT! You won 🪙 {bonus:,} Coins!")
        elif roll == "output_rate":
            boost = random.choice([200, 500, 1000])
            output_rate += boost
            st.success(f"⚡ BOOST! Received +{boost:,} PPH permanently!")
        else:
            st.warning("Box contained basic fertilizers. Better luck next time!")
        
        db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
        conn.commit()
        st.rerun()
    else:
        diff = 1000 - reserves
        st.error(f"❌ You need {diff:,} more coins to open the Mystery Box!")

# --- SECTION 2: UPGRADE SHOP (FORCED ON MAIN PAGE) ---
st.markdown('<div class="section-header">🛒 Upgrade Shop</div>', unsafe_allow_html=True)

# Item 1
pack_cost = 500 + (output_rate * 2)
st.markdown(f'<div class="upgrade-card"><div><b>Premium Hybrid Seeds</b><br><small>+100 PPH</small></div><div style="color:#ffd700;">🪙 {pack_cost:,}</div></div>', unsafe_allow_html=True)
if st.button("Purchase Seeds", use_container_width=True):
    if reserves >= pack_cost:
        reserves -= pack_cost
        output_rate += 100
        db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
        conn.commit()
        st.toast("Seeds successfully planted!", icon="🌱")
        st.rerun()
    else:
        diff = pack_cost - reserves
        st.error(f"❌ You need {diff:,} more coins for this upgrade.")

# Item 2
grid_cost = 2500 + (output_rate * 5)
st.markdown(f'<div class="upgrade-card"><div><b>Solar Irrigation Pumps</b><br><small>+500 PPH</small></div><div style="color:#ffd700;">🪙 {grid_cost:,}</div></div>', unsafe_allow_html=True)
if st.button("Install Irrigation", use_container_width=True):
    if reserves >= grid_cost:
        reserves -= grid_cost
        output_rate += 500
        db.execute("UPDATE system_users SET reserves = ?, output_rate = ? WHERE id = ?", (reserves, output_rate, session_user))
        conn.commit()
        st.toast("Irrigation online!", icon="⚡")
        st.rerun()
    else:
        diff = grid_cost - reserves
        st.error(f"❌ You need {diff:,} more coins for this irrigation.")

st.divider()
st.markdown('<p style="text-align:center; color:#4caf50; font-size:0.75rem; font-weight:bold;">VILLAGE MINING AI v3.4 • PLATINUM MASTER ENGINE</p>', unsafe_allow_html=True)
