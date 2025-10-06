# app.py
"""
Streamlit dashboard for the LG TV Inventory Demo Agent (Accessible Version)

✅ Features:
- High-contrast, colorblind-safe color palettes
- KPI summary, visual analytics, and query assistant
- Ideal for LangGraph production orchestration later
"""

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import plotly.express as px
import re

# === Database path ===
DB_PATH = Path(__file__).resolve().parent / "demo.db"

# === Streamlit setup ===
st.set_page_config(page_title="LG TV Inventory Demo", layout="wide")
st.title("📺 LG TV Inventory Automation Dashboard (Accessible Edition)")

# === Utility functions ===
@st.cache_data
def load_inventory():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    return df

@st.cache_data
def load_emails():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM emails ORDER BY processed_at DESC", conn)
    conn.close()
    return df

# === Load data ===
inv = load_inventory()

# -------------------------------------------------------------------
# 📊 KPI SUMMARY
# -------------------------------------------------------------------
st.markdown("### 🔹 Summary Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Distinct LG Models", inv["model"].nunique())
col2.metric("Total Inventory (Units)", int(inv["total_qty"].sum()))
col3.metric("Average Resale Price (Batch)", f"${inv['resale_price'].mean():.2f}")
col4.metric("Highest Resale Price", f"${inv['resale_price'].max():.2f}")

# -------------------------------------------------------------------
# 📈 1. What different LG models are offered
# -------------------------------------------------------------------
st.markdown("### 1️⃣ What different LG models are offered?")
models_list = inv["model"].unique().tolist()
st.write(f"**LG Models:** {', '.join(models_list)}")

# -------------------------------------------------------------------
# 💰 2. Average resale price per LG model (accessible colors)
# -------------------------------------------------------------------
st.markdown("### 2️⃣ Average Resale Price per LG Model")
avg_price = inv.groupby("model", as_index=False)["resale_price"].mean()

fig1 = px.bar(
    avg_price,
    x="model",
    y="resale_price",
    color="resale_price",
    color_continuous_scale=["#00429d", "#73a2f0", "#f4777f", "#93003a"],  # high-contrast blue-red
    title="Average Resale Price by Model",
)
fig1.update_layout(
    xaxis_title="Model",
    yaxis_title="Average Resale Price (USD)",
    font=dict(size=14),
    title_font=dict(size=18),
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------------------------
# 💵 3. Average resale price of the whole batch
# -------------------------------------------------------------------
st.markdown("### 3️⃣ Average Resale Price of the Whole Batch")
avg_batch = inv["resale_price"].mean()
st.info(f"**Average resale price across all LG TV models:** ${avg_batch:.2f}")

# -------------------------------------------------------------------
# ⚙️ 4. Technological divisions (accessible sunburst)
# -------------------------------------------------------------------
st.markdown("### 4️⃣ Technological Divisions by Model")
tech_div = inv.groupby(["division", "model"]).size().reset_index(name="count")
fig2 = px.sunburst(
    tech_div,
    path=["division", "model"],
    values="count",
    color="division",
    color_discrete_sequence=["#1b9e77", "#d95f02", "#7570b3", "#e7298a"],  # colorblind-friendly
    title="Technological Divisions by LG Model",
)
fig2.update_layout(font=dict(size=14))
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------------
# 📦 5. Total inventory by model (accessible)
# -------------------------------------------------------------------
st.markdown("### 5️⃣ Total Current Inventory of LG TV Models")
inv_qty = inv.groupby("model", as_index=False)["total_qty"].sum()

fig3 = px.bar(
    inv_qty,
    x="model",
    y="total_qty",
    color="total_qty",
    color_continuous_scale=["#004c6d", "#ffa600"],  # dark blue to orange gradient
    title="Total Inventory (Units) by Model",
)
fig3.update_layout(
    xaxis_title="Model",
    yaxis_title="Total Units in Stock",
    font=dict(size=14),
    title_font=dict(size=18),
)
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------------------------------------
# 🏷️ 6. Different model names
# -------------------------------------------------------------------
st.markdown("### 6️⃣ Different Model Names Offered")
st.dataframe(inv[["model", "model_name"]].drop_duplicates(), use_container_width=True)

# -------------------------------------------------------------------
# 📬 EMAIL CLASSIFICATION RESULTS
# -------------------------------------------------------------------
st.markdown("---")
st.header("📨 Email Classification Results")

try:
    emails = load_emails()
    if emails.empty:
        st.info("No emails processed yet. Run `python process_eml.py` to ingest sample .eml files.")
    else:
        # Bright, high-contrast confidence scheme
        def color_confidence(val):
            if val >= 0.9:
                return "background-color: #99e600"  # bright green
            elif val >= 0.6:
                return "background-color: #ffcc00"  # bright yellow
            else:
                return "background-color: #ff4d4d"  # bright red

        st.dataframe(
            emails[
                ["filename", "subject", "label", "confidence", "explanation", "processed_at"]
            ].style.applymap(color_confidence, subset=["confidence"])
        )

        conf_fig = px.histogram(
            emails,
            x="confidence",
            nbins=10,
            color="label",
            color_discrete_sequence=["#0072B2", "#E69F00", "#D55E00", "#56B4E9"],  # accessible colors
            title="Confidence Score Distribution (Accessible Colors)",
        )
        conf_fig.update_layout(
            font=dict(size=14),
            title_font=dict(size=18),
            xaxis_title="Confidence Score",
            yaxis_title="Count of Emails",
        )
        st.plotly_chart(conf_fig, use_container_width=True)

        st.markdown(
            """
            **🟩 High Confidence (≥0.9)** — Rule-based match  
            **🟨 Medium Confidence (0.6–0.9)** — Fallback heuristic  
            **🟥 Low Confidence (<0.6)** — Needs manual review
            """
        )
except Exception as e:
    st.error(f"Error loading emails: {e}")

# -------------------------------------------------------------------
# 🤖 QUERY ASSISTANT (LLM + Data Fusion Simulation)
# -------------------------------------------------------------------
st.markdown("---")
st.header("🤖 Query Assistant (LLM + Data Fusion Simulation)")

st.markdown(
    """
    Type a natural language query below to interact with your inventory database.  
    Examples:  
    - "show average price of 65-inch models"  
    - "which LG model has the highest resale price?"  
    - "total inventory for 43-inch TVs"
    """
)

query = st.text_input("Ask a question about your LG inventory:", "")

def answer_query(q: str, data: pd.DataFrame) -> str:
    q = q.lower()
    models_mentioned = [m for m in data["model"].unique() if m.lower() in q]

    # Highest resale price
    if "highest" in q and "price" in q:
        top_row = data.loc[data["resale_price"].idxmax()]
        return f"The highest resale price is **${top_row['resale_price']:.2f}** for model **{top_row['model']} ({top_row['model_name']})**."

    # Average resale price (global)
    if "average" in q and "price" in q and not models_mentioned:
        return f"The overall average resale price is **${data['resale_price'].mean():.2f}**."

    # Average resale for specific models
    if models_mentioned:
        responses = []
        for m in models_mentioned:
            avg = data.loc[data["model"] == m, "resale_price"].mean()
            responses.append(f"Model **{m}** average resale price: **${avg:.2f}**.")
        return " ".join(responses)

    # Total inventory
    if "total" in q and ("inventory" in q or "stock" in q):
        if models_mentioned:
            total = data.loc[data["model"].isin(models_mentioned), "total_qty"].sum()
            return f"Total inventory for {', '.join(models_mentioned)} is **{int(total)} units**."
        else:
            return f"Total inventory across all models is **{int(data['total_qty'].sum())} units**."

    # Division query
    if "division" in q:
        divisions = ", ".join(data["division"].unique())
        return f"The available technological divisions are: **{divisions}**."

    return "I'm not sure about that query. Try asking about price, models, inventory, or divisions."

if query:
    st.markdown(f"**🧠 Query:** {query}")
    with st.spinner("Analyzing your request..."):
        answer = answer_query(query, inv)
    st.success(answer)

# -------------------------------------------------------------------
# 📘 Footer
# -------------------------------------------------------------------
st.markdown("---")
st.caption(
    "This dashboard demonstrates an end-to-end automation flow:\n"
    "📥 Email ingestion → 🧠 LLM-style classification → 💾 Data storage → 📊 Visual BI → 💬 Natural-language querying.\n"
    "This accessible edition uses high-contrast color schemes suitable for users with visual impairments."
)
