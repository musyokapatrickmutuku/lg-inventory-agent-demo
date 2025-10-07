import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# --------------------------------------------
# CONFIG & PAGE SETUP
# --------------------------------------------
st.set_page_config(
    page_title="Smart Business Analytics Agent",
    page_icon="📦",
    layout="wide",
)

# Define color scheme (high-contrast for visibility)
COLOR_CONFIDENCE_HIGH = "#2ecc71"   # Bright green
COLOR_CONFIDENCE_MED = "#f1c40f"    # Yellow
COLOR_CONFIDENCE_LOW = "#e74c3c"    # Red
COLOR_PRIMARY = "#1e90ff"           # Bright blue

# --------------------------------------------
# NAVIGATION BAR
# --------------------------------------------
menu = st.sidebar.radio("📂 Navigation", ["Dashboard", "Query Assistant", "Settings"])

st.markdown(
    f"""
    <style>
        .main {{
            background-color: #ffffff;
        }}
        .stApp header {{
            background-color: {COLOR_PRIMARY};
            color: white;
            padding: 0.5rem;
        }}
        .stApp header h1 {{
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------
DB_PATH = "demo_agent.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

# Helper to get data
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM emails", conn)
    conn.close()
    return df

# --------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------
if menu == "Dashboard":
    st.title("📦 Smart SupplyMail Analyzer")
    st.caption("AI-powered insights from supplier and buyer communications")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No email data available. Please process .eml files first.")
    else:
        # Add confidence color
        def confidence_color(score):
            if score >= 0.8:
                return COLOR_CONFIDENCE_HIGH
            elif score >= 0.5:
                return COLOR_CONFIDENCE_MED
            return COLOR_CONFIDENCE_LOW

        df["ConfidenceColor"] = df["confidence"].apply(confidence_color)

        st.subheader("📊 Classified Emails Overview")
        st.dataframe(df[["subject", "category", "confidence", "explanation"]], use_container_width=True)

        # Visualization
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(
                df,
                x="category",
                color="category",
                title="Email Distribution by Category",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.scatter(
                df,
                x="category",
                y="confidence",
                color="category",
                size=[10 for _ in range(len(df))],
                title="Confidence Levels by Category",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            st.plotly_chart(fig2, use_container_width=True)

        # Inventory summary block
        st.markdown("---")
        st.subheader("📦 Inventory Summary Insights")

        try:
            conn = get_connection()
            inventory_df = pd.read_sql_query("SELECT * FROM inventory", conn)
            conn.close()

            st.dataframe(inventory_df, use_container_width=True)

            avg_price = inventory_df["Resale Price"].mean()
            avg_lg = inventory_df[inventory_df["Model"].str.contains("LG", case=False, na=False)]["Resale Price"].mean()
            total_lg = inventory_df[inventory_df["Model"].str.contains("LG", case=False, na=False)]["Stock"].sum()

            st.metric("💰 Average Resale Price (All Models)", f"KES {avg_price:,.2f}")
            st.metric("💰 Average Resale Price (LG Models)", f"KES {avg_lg:,.2f}")
            st.metric("📦 Total LG Inventory", f"{int(total_lg)} units")

        except Exception as e:
            st.warning(f"⚠️ Could not load inventory data: {e}")

# --------------------------------------------
# QUERY ASSISTANT PAGE
# --------------------------------------------
elif menu == "Query Assistant":
    st.title("💬 Query Assistant")
    st.caption("Ask natural language questions about your inventory and email data")

    user_query = st.text_input("Ask your question below:", placeholder="e.g., show average price of 65-inch models")

    if st.button("Ask"):
        if not user_query.strip():
            st.warning("Please enter a question first.")
        else:
            conn = get_connection()
            inv_df = pd.read_sql_query("SELECT * FROM inventory", conn)
            conn.close()

            user_query_lower = user_query.lower()
            response = ""

            # Simple AI-ish deterministic responses
            if "average" in user_query_lower and "price" in user_query_lower:
                if "65" in user_query_lower:
                    avg_65 = inv_df[inv_df["Model"].str.contains("65", na=False)]["Resale Price"].mean()
                    response = f"The average resale price for 65-inch models is **KES {avg_65:,.2f}**."
                else:
                    avg_all = inv_df["Resale Price"].mean()
                    response = f"The overall average resale price across all models is **KES {avg_all:,.2f}**."

            elif "inventory" in user_query_lower or "stock" in user_query_lower:
                total_stock = inv_df["Stock"].sum()
                response = f"The total inventory currently in stock is **{int(total_stock)} units**."

            elif "lg" in user_query_lower:
                lg_models = inv_df[inv_df["Model"].str.contains("LG", case=False, na=False)]["Model"].unique()
                response = f"The LG models on offer include: **{', '.join(lg_models)}**."

            else:
                response = "I'm not sure how to answer that yet — the full LLM integration will handle this in production."

            st.success(response)

# --------------------------------------------
# SETTINGS PAGE
# --------------------------------------------
elif menu == "Settings":
    st.title("⚙️ Settings")
    st.info("Future features: Email API keys, scheduling, and LangGraph workflow integrations.")
    st.markdown(
        """
        **Coming soon:**
        - Gmail/Outlook ingestion settings  
        - Rule tuning for classification  
        - LangGraph orchestration hooks  
        - Data source management
        """
    )

