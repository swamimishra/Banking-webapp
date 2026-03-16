import streamlit as st
from bank import Bank
import pandas as pd

st.set_page_config(page_title="StreamBank NetBanking", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR LIGHT PROFESSIONAL LOOK ---
st.markdown("""
<style>
    /* Professional Light Theme */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* Metrics styling - Clean & Professional */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #1e40af !important; /* Deep Blue */
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #64748b !important;
        font-weight: 500;
    }
    
    /* Primary buttons */
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        transition: background-color 0.2s;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        border-color: #1d4ed8;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Cards */
    .bank-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏦 StreamBank NetBanking")
st.caption("Secure. Reliable. Innovative. | Professional Demo Version")
st.markdown("---")

# Initialize session state for authentication
if 'user' not in st.session_state:
    st.session_state.user = None

def logout():
    st.session_state.user = None
    st.success("Logged out successfully!")
    st.rerun()

# Sidebar Navigation
if st.session_state.user:
    st.sidebar.title("Navigation")
    st.sidebar.info(f"Welcome back, **{st.session_state.user['name']}**")
    
    nav_mode = st.sidebar.radio("Go to", ["Dashboard", "Payments", "Account Services", "Settings"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        logout()
else:
    nav_mode = st.sidebar.selectbox("Access", ["Login", "Create Account"])

# --- PAGE LOGIC ---

if nav_mode == "Create Account":
    st.subheader("👤 Create New Account")
    with st.form("create_account_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, step=1)
        email = st.text_input("Email Address")
        pin = st.text_input("Set a 4-digit Secure PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Create My Account")

    if submitted:
        if name and email and pin:
            if age < 18:
                st.warning("You must be at least 18 years old to create an account.")
            elif len(pin) != 4 or not pin.isdigit():
                st.warning("PIN must be exactly 4 digits.")
            else:
                user, msg = Bank.create_account(name, int(age), email, int(pin))
                if user:
                    st.success(msg)
                    st.info(f"Your Unique Account Number: {user['accountNo.']}")
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.warning("Please fill in all mandatory fields.")

elif nav_mode == "Login":
    st.subheader("🔐 Secure Entry")
    with st.form("login_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("Security PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Login")
    
    if submit:
        if acc_no and pin:
            try:
                user = Bank.find_user(acc_no, int(pin))
                if user:
                    st.session_state.user = user
                    st.success("Authorization Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Account Number or PIN.")
            except ValueError:
                st.error("PIN must be numeric.")
        else:
            st.warning("Credentials required.")

elif nav_mode == "Dashboard":
    if st.session_state.user:
        user = st.session_state.user
        st.subheader("📊 Accounts Overview")
        
        # S12: Advanced Dashboard UI
        updated_user = Bank.find_user(user['accountNo.'], user['pin'])
        if updated_user:
            st.session_state.user = updated_user
            transactions = Bank.get_transactions(user['accountNo.'])
            
            with st.container():
                col1, col2, col3 = st.columns(3)
                if transactions == "TABLE_MISSING":
                     st.warning("⚠️ **Note**: Transactions table not found in Supabase. Logging is disabled.")
                     col1.metric("Available Balance", f"₹ {updated_user['balance']}")
                     col2.metric("Savings Account", f"{user['accountNo.']}")
                     col3.metric("Daily Limit", "₹ 10,000")
                else:
                    total_deposited = sum(t['amount'] for t in transactions if t['type'] == 'Deposit')
                    total_withdrawn = sum(t['amount'] for t in transactions if t['type'] == 'Withdrawal')
                    
                    col1.metric("Available Balance", f"₹ {updated_user['balance']}", delta=f"₹ {total_deposited - total_withdrawn}")
                    col2.metric("Savings Account", f"{user['accountNo.']}")
                    col3.metric("Total Deposits", f"₹ {total_deposited}")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # S11: Transaction History
            st.subheader("📜 Recent Transactions")
            if isinstance(transactions, list) and transactions:
                df = pd.DataFrame(transactions)
                
                # Real Insights: Building chart from actual transaction categories
                with st.expander("📈 Insights: Spending Breakdown", expanded=True):
                    st.write("Visual analytics of your actual transaction categories.")
                    if not df.empty and 'category' in df.columns:
                        # Filter for 'Withdrawal' or 'Transfer' to show "Spending"
                        spending_df = df[df['type'].isin(['Withdrawal', 'Transfer'])]
                        if not spending_df.empty:
                            cat_counts = spending_df.groupby('category')['amount'].sum()
                            st.bar_chart(cat_counts)
                        else:
                            st.info("📊 Chart will appear once you have spending transactions (Transfers or Withdrawals).")
                    else:
                        st.info("Add transactions to see your spending breakdown.")

                # Process DF for display table
                df_display = df[['type', 'category', 'amount', 'timestamp']].sort_values('timestamp', ascending=False)
                df_display['amount'] = df_display['amount'].apply(lambda x: f"₹ {x}")
                df_display.rename(columns={'type': 'Type', 'category': 'Reference', 'amount': 'Amount', 'timestamp': 'Date'}, inplace=True)
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info("No recent activities documented.")
            
        else:
            st.error("Session verification failed. Please login again.")

elif nav_mode == "Payments":
    if st.session_state.user:
        st.subheader("💸 Payments & Fund Transfers")
        pay_tab1, pay_tab2 = st.tabs(["Quick Deposit", "P2P Fund Transfer"])
        
        with pay_tab1:
            with st.form("deposit_form_new"):
                st.write("Deposit funds into your Savings account.")
                amount = st.number_input("Amount to Deposit", min_value=1)
                cat = st.selectbox("Category", ["Salary", "Savings", "Gift", "Refund", "Others"])
                submit_dep = st.form_submit_button("Confirm Deposit")
                
                if submit_dep:
                    success, msg = Bank.deposit(st.session_state.user['accountNo.'], st.session_state.user['pin'], amount)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
        
        with pay_tab2:
            st.write("Send money instantly to other StreamBank customers.")
            with st.form("transfer_form"):
                target_acc = st.text_input("Recipient's Account Number")
                transfer_amt = st.number_input("Amount (up to ₹10,000)", min_value=1, max_value=10000)
                t_pin = st.text_input("Authorize with PIN", type="password", max_chars=4)
                submit_transfer = st.form_submit_button("Initiate Transfer")
                
                if submit_transfer:
                    if target_acc and transfer_amt and t_pin:
                        success, msg = Bank.transfer_funds(st.session_state.user['accountNo.'], target_acc, t_pin, transfer_amt)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                    else:
                        st.warning("All security fields are required.")

elif nav_mode == "Account Services":
    if st.session_state.user:
        st.subheader("🛠️ Services & Management")
        serv_menu = st.radio("Access Tool", ["Update Profile", "Withdrawal Hub", "Deactivate Account"], horizontal=True)
        
        if serv_menu == "Update Profile":
             with st.form("update_form"):
                new_name = st.text_input("Legal Name", value=st.session_state.user['name'])
                new_email = st.text_input("Primary Email", value=st.session_state.user['email'])
                curr_pin = st.text_input("Current Authorization PIN", type="password")
                new_pin = st.text_input("Change PIN (Optional)", type="password", max_chars=4)
                submit_up = st.form_submit_button("Apply Changes")
                
                if submit_up:
                    success, msg = Bank.update_user(st.session_state.user['accountNo.'], curr_pin, 
                                                  name=new_name, email=new_email, 
                                                  new_pin=new_pin if new_pin else None)
                    if success: st.success(msg)
                    else: st.error(msg)
                    
        elif serv_menu == "Withdrawal Hub":
            with st.form("withdraw_form"):
                st.write("Withdrawal from Savings Account")
                w_amt = st.number_input("Amount", min_value=1, step=100)
                w_pin = st.text_input("Security PIN", type="password")
                submit_w = st.form_submit_button("Verify & Dispense")
                if submit_w:
                    success, msg = Bank.withdraw(st.session_state.user['accountNo.'], w_pin, w_amt)
                    if success: st.success(msg)
                    else: st.error(msg)
        
        elif serv_menu == "Deactivate Account":
            st.error("CRITICAL: Account Termination")
            st.write("Deleting your account will purge all associated data immediately.")
            with st.form("delete_form"):
                d_pin = st.text_input("Confirm PIN for Termination", type="password")
                submit_d = st.form_submit_button("Permanently Terminate Account")
                if submit_d:
                    success, msg = Bank.delete_user(st.session_state.user['accountNo.'], d_pin)
                    if success:
                        st.success(msg)
                        st.session_state.user = None
                        st.rerun()
                    else:
                        st.error(msg)

elif nav_mode == "Settings":
    st.subheader("⚙️ Regional & Security Settings")
    colA, colB = st.columns(2)
    with colA:
        st.info("🔒 **Biometric Authentication**\nPlanned for next Sprint.")
    with colB:
        st.info("🌍 **Language: English (Global)**")
