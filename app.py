import streamlit as st
import sqlite3
from datetime import datetime
from auth import create_user_table, signup_user, login
from roadmap_data import load_roadmap

# ------------------ CONFIG ------------------
st.set_page_config(page_title="365 Days Python Roadmap", layout="wide")
create_user_table()

# ------------------ MONTH ORDER FIX ------------------
MONTH_ORDER = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# ------------------ SESSION ------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ AUTH ------------------
if st.session_state.user is None:
    st.title("🔐 Welcome to 365 Days Python Roadmap")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        username = st.text_input("Email or Mobile")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Email or Mobile")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Sign Up"):
            if signup_user(new_user, new_pass):
                st.success("Account created. Please login.")
            else:
                st.error("User already exists")

    st.stop()  # ⛔ BLOCK ROADMAP

# ------------------ USER ------------------
USER = st.session_state.user

# ------------------ PROGRESS DB ------------------
conn = sqlite3.connect("progress.db", check_same_thread=False)
conn.execute("""
CREATE TABLE IF NOT EXISTS progress (
    user TEXT,
    date TEXT,
    completed INTEGER,
    PRIMARY KEY (user, date)
)
""")

def is_done(date):
    row = conn.execute(
        "SELECT completed FROM progress WHERE user=? AND date=?",
        (USER, date)
    ).fetchone()
    return row and row[0] == 1

def set_done(date, val):
    conn.execute(
        "INSERT OR REPLACE INTO progress VALUES (?, ?, ?)",
        (USER, date, int(val))
    )
    conn.commit()

# ------------------ LOAD DATA ------------------
df = load_roadmap()

# ------------------ SIDEBAR ------------------
st.sidebar.success(USER)

completed = conn.execute(
    "SELECT COUNT(*) FROM progress WHERE user=? AND completed=1",
    (USER,)
).fetchone()[0]

st.sidebar.metric("Completed", f"{completed}/365")
st.sidebar.progress(completed / 365)

# 🔥 STREAK
dates = conn.execute(
    "SELECT date FROM progress WHERE user=? AND completed=1",
    (USER,)
).fetchall()

date_set = {datetime.strptime(d[0], "%Y-%m-%d").date() for d in dates}
streak = 0
today = datetime.today().date()

while today in date_set:
    streak += 1
    today = today.fromordinal(today.toordinal() - 1)

st.sidebar.metric("🔥 Streak", f"{streak} days")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ------------------ MAIN UI ------------------
st.markdown("## 🚀 365 Days Python Roadmap")

# ✅ MONTH DROPDOWN — FIXED ORDER
available_months = [m for m in MONTH_ORDER if m in df["Month"].unique()]
month = st.selectbox("📅 Select Month", available_months)

week = st.selectbox(
    "🗓️ Select Week",
    sorted(df[df["Month"] == month]["Week"].unique())
)

filtered = df[(df["Month"] == month) & (df["Week"] == week)]

for _, row in filtered.iterrows():
    date_key = row["Date"].strftime("%Y-%m-%d")
    checked = is_done(date_key)

    c1, c2 = st.columns([0.05, 0.95])
    with c1:
        val = st.checkbox("", value=checked, key=f"{USER}_{date_key}")
        if val != checked:
            set_done(date_key, val)
            st.rerun()

    with c2:
        st.markdown(
            f"""
            <div style="background:#fff;color:#000;padding:16px;border-radius:10px;margin-bottom:12px">
                <h4>Day {row['Day']} — {row['Topic']}</h4>
                <p><b>Practice:</b> {row['Practice']}</p>
                <small>📅 {row['Date'].strftime('%d %b %Y')}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
