import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# ==============================
# APP CONFIGURATION
# ==============================
st.set_page_config(
    page_title="Smart Business Analytics Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Smart Business Analytics Agent")
st.caption("An AI-powered demo for intelligent email & inventory analytics")

# ==============================
# LOAD OR CREATE DATABASE SAFELY
# ==============================

def load_data():
    db_path = "emails.db"
    table_name = "emails"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)
    )
    exists = cursor.fetchone()

    if not exists:
        # Create demo dataset
        demo_data = [
            (
                "sales_confirmation.eml",
                "Sales Confirmation",
                "sales@example.com",
                "This is a sales confirmation email.",
                "Sales Confirmation",
                0.95,
                "High confidence due to 'confirmation' and 'sale' keywords.",
            ),
            (
                "shipment_update.eml",
                "Shipment Update",
                "logistics@example.com",
                "Your order has shipped and will arrive soon.",
                "Shipment Update",
                0.90,
                "Detected logistics terms like 'shipped' and 'arrival'.",
            ),
            (
                "rfq_request.eml",
                "Request for Quotation",
                "buyer@example.com",
                "Please send a quotation for 65-inch models.",
                "RFQ",
                0.93,
                "Found 'quotation' and 'request' patterns with high certainty.",
            ),
        ]
        df_demo = pd.DataFrame(
            demo_data,
            columns=[
                "filename",
                "subject",
                "from",
                "body",
                "category",
                "confidence",
                "explanation",
            ],
        )
        df_demo.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        st.session_state["demo_mode"] = True
        return df_demo

    # If table exists, read data safely
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        st.session_state["demo_mode"] = False
        return df
    except Exception as e:
        conn.close()
        st.session_state["demo_mode"] = True
        st.error(f"Database error recovered: {e}")
        return pd.DataFrame(
            [
                (
                    "demo.eml",
                    "Fallback Email",
                    "noreply@example.com",
                    "This is sample fallback data.",
                    "General",
                    0.5,
                    "Fallback default due to DB issue.",
                )
            ],
            columns=[
                "filename",
                "subject",
                "from",
                "body",
                "category",
                "confidence",
                "explanation",
            ],
        )


df = load_data()

# ==============================
# DEMO MODE BANNER
# ==============================
if st.session_state.get("demo_mode", False):
    st.warning(
        "💡 Running in demo mode with sample emails. "
        "Connect your production SQLite or cloud database for live analytics.",
        icon="⚙️",
    )

# ==============================
# DASHBOARD SECTION
# ==============================
st.header("📬 Email Intelligence Dashboard")

col1, col2 = st.columns(2)

# Bright, accessible color palette
color_map = {
    "Sales Confirmation": "#FF6B6B",  # bright red
    "Shipment Update": "#4ECDC4",     # turquoise
    "RFQ": "#FFD93D",                # bright yellow
    "Complaint": "#FF9F1C",          # orange
    "General": "#1E90FF",            # blue
}

with col1:
    st.subheader("📈 Email Category Distribution")
    fig_cat = px.histogram(
        df,
        x="category",
        color="category",
        color_discrete_map=color_map,
        title="Distribution by Category",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col2:
    st.subheader("🎯 Confidence Scores Overview")
    fig_conf = px.box(
        df,
        x="category",
        y="confidence",
        color="category",
        color_discrete_map=color_map,
        title="Confidence Levels by Category",
    )
    st.plotly_chart(fig_conf, use_container_width=True)

# ==============================
# EMAIL TABLE WITH DETAILS
# ==============================
st.subheader("📋 Classified Email Records")

st.dataframe(
    df[["filename", "subject", "from", "category", "confidence", "explanation"]],
    use_container_width=True,
    hide_index=True,
)

# ==============================
# INTERACTIVE QUERY ASSISTANT
# ==============================
st.markdown("---")
st.header("💬 Query Assistant")

st.markdown(
    "Ask a question about your data (e.g., _'Show average confidence for RFQ emails'_ or _'Which category has the highest confidence?'_):"
)

query = st.text_input("Type your question here...")

if query:
    query_lower = query.lower()
    response = "🤖 Sorry, I couldn't understand that query."

    if "average" in query_lower and "confidence" in query_lower:
        avg_conf = df["confidence"].mean()
        response = f"The **average confidence score** across all emails is **{avg_conf:.2f}**."

    elif "highest confidence" in query_lower:
        top = df.loc[df["confidence"].idxmax()]
        response = f"The highest confidence email is **'{top['subject']}'**, categorized as **{top['category']}** with a score of **{top['confidence']:.2f}**."

    elif "rfq" in query_lower:
        rfq_avg = df[df["category"].str.lower() == "rfq"]["confidence"].mean()
        response = f"The **average confidence** for RFQ emails is **{rfq_avg:.2f}**."

    elif "categories" in query_lower:
        cats = ", ".join(df["category"].unique())
        response = f"The current categories detected are: **{cats}**."

    elif "emails" in query_lower or "records" in query_lower:
        response = f"There are **{len(df)} emails** analyzed in this batch."

    st.success(response)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Built using Streamlit · Prototype powered
