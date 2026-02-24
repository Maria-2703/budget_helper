# 💰 AI Budgeting & Transaction Classification App

A Flask web application that allows users to upload bank statement CSV files and automatically classify transactions into financial categories using a hybrid system:

- ✅ Keyword-based classification (fast, rule-based)
- 🤖 AI-powered classification using Cohere (for unmatched transactions)

This app helps users organize and better understand their spending for budgeting purposes.

---

## 🚀 Features

- Upload one or multiple CSV bank statement files
- Automatic transaction categorization
- Hybrid classification system (keywords + AI fallback)
- Clean HTML table output
- Secure API key management using environment variables

---

## 🏗️ Tech Stack

- **Backend:** Flask  
- **AI Model:** Cohere `command-nightly`  
- **Data Processing:** Pandas  
- **Environment Variables:** python-dotenv  
- **Frontend:** Jinja2 Templates  

---

## 📂 Project Structure
├── app.py
├── keywords.json
├── templates/
│ └── home.html
├── .env
├── requirements.txt
└── README.md


---

## 🧠 How Classification Works

### 1️⃣ Keyword-Based Classification

- Loads `keywords.json`
- Checks if any keyword appears in the transaction description
- Assigns the corresponding category immediately

Example `keywords.json`:

```json
{
  "Subscriptions": ["netflix", "spotify", "apple"],
  "Groceries": ["walmart", "carrefour", "tesco"],
  "Transportation": ["uber", "metro", "shell"]
}