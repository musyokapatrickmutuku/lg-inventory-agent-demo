## LG Inventory Automation Demo (AI + Data Fusion)

An interactive Streamlit demo showcasing an automated workflow for a consumer electronics business.
It demonstrates how AI agents can integrate with emails, databases, and dashboards to streamline operations and business analytics.

### 🌐 Live Demo

Once deployed, the app will be available at:
👉 https://your-app-name.streamlit.app

### 🧠 Overview

This demo simulates an automation flow for a retail electronics business that sells LG TVs, phones, and other devices.
It showcases a LangGraph-ready workflow combining:

Email ingestion & classification

Data persistence in SQLite

Analytics dashboard

Natural-language querying

### ⚡ Architecture (LangGraph-Ready)
graph TD
    A[📥 Email Connector<br/>.eml ingestion] --> B[🧠 Rule-based + LLM Classifier]
    B --> C[💾 SQLite Database<br/>(inventory + email logs)]
    C --> D[📊 Streamlit Dashboard<br/>with analytics & insights]
    D --> E[💬 Query Assistant<br/>Natural language queries]


This architecture can easily be extended into a production LangGraph flow where each node (A–E) becomes an independent, orchestrated agent.

🧩 Features

#### ✅ Automatic Email Classification
– Processes .eml files and classifies them into categories (RFQ, Complaint, Finance, etc.)

#### ✅ Centralized Inventory Database
– SQLite backend containing all product and sales data

#### ✅ Accessible Analytics Dashboard
– High-contrast charts for inclusivity (colorblind-friendly design)

#### ✅ LLM-Style Query Assistant
– Ask questions like “show average price of 65-inch models” or “what division has the highest resale price”

#### ✅ LangGraph Integration Ready
– Each layer is modular and ready to be transformed into a node in LangGraph for production orchestration

### 🚀 Quick Start (Local)

1️⃣ Clone the repository

git clone https://github.com/your-username/lg-inventory-agent-demo.git
cd lg-inventory-agent-demo


2️⃣ Install dependencies

pip install -r requirements.txt


3️⃣ Initialize the database

python init_db.py


4️⃣ Process sample emails

python process_eml.py


5️⃣ Run the Streamlit app

streamlit run app.py


6️⃣ Open in browser
Go to http://localhost:8501

### 🌍 Deploy to Streamlit Cloud (Free)

Go to https://share.streamlit.io/

Log in with GitHub

Click “New App”

Select your repo and branch

Set app.py as the main file

Click Deploy

### 💥 Done — you’ll get a public link like:
https://lg-inventory-agent-demo.streamlit.app

Anyone can now run your app instantly — no installation required.

### 📊 Example Use Cases
Task	Description
Classify incoming emails	Automatically categorize supplier or customer emails
Generate insights	Average resale prices, model mix, inventory count
Visual analytics	Interactive, colorblind-safe dashboard
Query Assistant	Ask questions in plain English and get data-driven answers
🧱 Future Work (Production Readiness)

Integrate with LangGraph for modular flow orchestration

Replace mock LLM classifier with an actual LLM API (OpenAI or local model)

Add email API connectors (Gmail, Outlook)

Extend BI module with real-time sales tracking

#### 👨‍💻 Author

Patrick Musyoka
Data Scientist & Automation Specialist
🔗 LinkedIn
 | 🌍 Portfolio

📜 License

MIT License — free for demo and educational use.

#### 🧩 BONUS: Optional .streamlit/config.toml

To ensure a bright UI theme for presentations, add this file:

[theme]
base="light"
primaryColor="#004c6d"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F8F9FA"
textColor="#000000"
