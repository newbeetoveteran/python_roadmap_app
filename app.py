import streamlit as st
import pandas as pd
from roadmap import generate_roadmap
from database import toggle_day, is_completed, get_completed_days

st.set_page_config(page_title="Python Roadmap", layout="wide")

roadmap = generate_roadmap()
df = pd.DataFrame(roadmap)

completed_days = get_completed_days()
total_days = 365

xp = completed_days * 10
level = (
    "Beginner" if xp < 500 else
    "Intermediate" if xp < 1500 else
    "Advanced" if xp < 3000 else
    "Python Pro"
)

# ---------------- DASHBOARD ----------------
st.title("🐍 Python 1-Year Learning App")
st.progress(completed_days / total_days)

col1, col2, col3 = st.columns(3)
col1.metric("Completed Days", completed_days)
col2.metric("XP", xp)
col3.metric("Level", level)

st.divider()

# ---------------- MONTH WISE VIEW ----------------
st.subheader("📅 Month-wise Learning Plan")

months = df["month"].unique()

for month in months:
    with st.expander(f"📘 {month}", expanded=False):
        month_df = df[df["month"] == month]

        for _, row in month_df.iterrows():
            done = is_completed(row["day"])
            cols = st.columns([1, 3, 3, 2])

            cols[0].write(f"Day {row['day']}")
            cols[1].write(str(row["date"]))
            cols[2].write(row["topic"])

            if cols[3].button(
                "✅ Done" if done else "⬜ Mark Complete",
                key=row["day"]
            ):
                toggle_day(row["day"])
                st.rerun()
