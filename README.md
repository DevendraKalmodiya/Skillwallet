# Multimodal Construction Intelligence Platform
## Skill Wallet Capstone Project 1

> AI-powered construction site safety, structural diagnostics, real estate valuation, and site assistance — powered by **Google Gemini 1.5 Flash**

---

### 🚀 Quick Start

```bash
# 1. Clone or navigate to this directory
cd "d:\Medicaps notes\7th sem\Skillwallet"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

### 🌐 Deploy to Streamlit Community Cloud (1-click)

1. Push this folder to a **GitHub repository**
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as the main file
4. Click **Deploy** — no other configuration needed

---

### 🔑 API Key Setup

- Get a **free** Google Gemini API key at [aistudio.google.com](https://aistudio.google.com/app/apikey)
- Enter it in the sidebar **API Configuration** section
- Without a key, the app runs in **Demo Mode** with realistic sample data

---

### 📦 Module Overview

| Tab | Feature | Standards |
|-----|---------|-----------|
| 🦺 Tab 1 | Site Safety & PPE Audit | OSHA 29 CFR 1926, IS 456:2000 |
| 🔍 Tab 2 | Crack Diagnostics | IS 456:2000, IS 13920:1993 |
| 💰 Tab 3 | Planning & Valuation | CPWD Rates, Indian Market |
| 🤖 Tab 4 | Daily Site Assistant | IS 456, IS 800, NBC 2016 |

---

### 🏗️ Architecture

```
Frontend    →  Streamlit 1.35+
AI Core     →  Google Gemini 1.5 Flash (Multimodal)
Vision      →  Multimodal Image Prompting
3D Render   →  Pollinations AI (Flux Model)
Standards   →  IS 456, IS 800, OSHA CFR 1926
Database    →  Zero (all state in session)
Deploy      →  Streamlit Community Cloud
```

---

### 📁 File Structure

```
Skillwallet/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Theme & server config
```

---

*Skill Wallet Capstone Project 1 · © 2024*
