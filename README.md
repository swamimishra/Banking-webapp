# 🏦 StreamBank App

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red.svg)
![Supabase](https://img.shields.io/badge/Supabase-Backend-green.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Issues](https://img.shields.io/github/issues/PruthvirajChavan45/streambank-app)
![Stars](https://img.shields.io/github/stars/PruthvirajChavan45/streambank-app?style=social)

A **modern banking management system** built with **Python & Streamlit**, powered by **Supabase** for secure and scalable backend operations.
This project allows users to create and manage accounts with features like deposit, withdrawal, and viewing account details through an intuitive web interface.

> 💡 Ideal for learning **OOP concepts**, **Python development**, **Streamlit web apps**, and **Supabase integration**.

---

## ✨ Features

- 👤 **Create Account**: Open a new account with a unique, auto-generated account number.
- 💰 **Deposit Money**: Secure deposit transactions (up to ₹10,000 per transaction).
- 🏧 **Withdraw Money**: Withdraw funds with real-time balance checks.
- 📑 **View Account Details**: Check balance and account info (protected by PIN).
- 🔒 **Secure Authentication**: PIN-based verification for all sensitive operations.
- ☁️ **Cloud Storage**: Data is securely stored in a Supabase PostgreSQL database.

### 🚧 Planned Features (Coming Soon)
- ✏️ Update account information (Name, Email, PIN)
- 🗑️ Delete account functionality
- � Transaction history log
- � Email notifications

---

## 📂 Project Structure

```
streambank-app/
│── app.py              # Streamlit frontend (UI + interactions)
│── bank.py             # Backend logic (Supabase integration)
│── requirements.txt    # Required Python libraries
│── .streamlit/         # Configuration directory
│   └── secrets.toml    # Supabase credentials (not committed)
│── screenshots/        # App UI screenshots
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/PruthvirajChavan45/streamlit-bank.git
cd streamlit-bank
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# Activate virtual environment:
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase

1. Create a project on [Supabase.com](https://supabase.com/).
2. Create a table named `users` with the following columns:
    - `name` (text)
    - `age` (int8)
    - `email` (text)
    - `pin` (int8)
    - `account_number` (text) - *Primary Key*
    - `balance` (float8) - *Default: 0.0*
3. Get your **Project URL** and **API Key** from Supabase Settings > API.
4. Create a file `.streamlit/secrets.toml` inside the project folder and add your credentials:

```toml
[general]
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

By default, the app runs locally at: `http://localhost:8501/`

---

## 📸 Screenshots

### 🏠 Home Page
![Home Screenshot](screenshots/home.png)

### 👤 Create Account
![Create Account Screenshot](screenshots/create-account.png)

### 💰 Deposit Money
![Deposit Screenshot](screenshots/deposit.png)

### 🏧 Withdraw Money
![Withdraw Screenshot](screenshots/withdraw.png)

### 📑 Account Details
![Show Details Screenshot](screenshots/show_details.png)

---

## �️ Tech Stack

- **Frontend**: Streamlit
- **Backend Logic**: Python
- **Database**: Supabase (PostgreSQL)

---

## 👨‍💻 Author

Developed by **Pruthviraj Chavan** ✨
🔗 [GitHub Profile](https://github.com/PruthvirajChavan45)
