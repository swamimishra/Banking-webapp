import streamlit as st
from bank import Bank

st.set_page_config(page_title="StreamBank App", layout="centered")
st.title("🏦 Welcome to Streamlit Bank")

# Initialize session state for authentication
if 'user' not in st.session_state:
    st.session_state.user = None

def logout():
    st.session_state.user = None
    st.success("Logged out successfully!")

# Sidebar Navigation
if st.session_state.user:
    st.sidebar.success(f"Logged in as: {st.session_state.user['name']}")
    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Deposit", "Withdraw", "Update Info", "Delete Account"]
    )
    if st.sidebar.button("Logout"):
        logout()
        st.rerun()
else:
    menu = st.sidebar.selectbox("Menu", ["Login", "Create Account"])

if menu == "Create Account":
    st.subheader("👤 Create New Account")
    with st.form("create_account_form"):
        name = st.text_input("Your Name")
        age = st.number_input("Your Age", min_value=0, step=1)
        email = st.text_input("Your Email")
        pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if name and email and pin:
            if age < 18:
                st.warning("You must be at least 18 years old to create an account.")
            elif len(pin) != 4 or not pin.isdigit():
                st.warning("PIN must be exactly 4 digits.")
            else:
                try:
                    user, msg = Bank.create_account(name, int(age), email, int(pin))
                    if user:
                        st.success(msg)
                        st.info(f"Your Account Number: {user['accountNo.']}")
                        st.session_state.user = user  # Auto-login after creation
                        st.markdown("Please **Login** specifically if auto-redirect doesn't work (or just refresh).")
                        st.rerun()
                    else:
                        st.error(msg)
                except ValueError:
                    st.error("Invalid input. Please check your details.")
        else:
            st.warning("Fill all fields")

elif menu == "Login":
    st.subheader("🔐 Login to Your Account")
    with st.form("login_form"):
        acc_no = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submit = st.form_submit_button("Login")
    
    if submit:
        if acc_no and pin:
            try:
                user = Bank.find_user(acc_no, int(pin))
                if user:
                    st.session_state.user = user
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Account Number or PIN.")
            except ValueError:
                st.error("PIN must be numeric.")
        else:
            st.warning("Please enter Account Number and PIN.")

elif menu == "Dashboard":
    if st.session_state.user:
        user = st.session_state.user
        st.subheader("📊 Your Dashboard")
        st.info(f"**Account Number:** {user['accountNo.']}")
        st.info(f"**Name:** {user['name']}")
        
        updated_user = Bank.find_user(user['accountNo.'], user['pin'])
        if updated_user:
            st.session_state.user = updated_user 
            st.metric(label="Current Balance", value=f"₹ {updated_user['balance']}")
        else:
            st.error("Error fetching latest data.")

elif menu == "Deposit":
    st.subheader("💰 Deposit Money")
    if st.session_state.user:
        user = st.session_state.user
        st.write(f"Depositing to Account: **{user['accountNo.']}**")
        amount = st.number_input("Amount to Deposit", min_value=1)
        
        if st.button("Deposit"):
            success, msg = Bank.deposit(user['accountNo.'], user['pin'], int(amount))
            if success:
                st.success(msg)
                updated_user = Bank.find_user(user['accountNo.'], user['pin'])
                if updated_user:
                    st.session_state.user = updated_user
            else:
                st.error(msg)

elif menu == "Withdraw":
    st.subheader("🏧 Withdraw Money")
    if st.session_state.user:
        user = st.session_state.user
        st.write(f"Withdrawing from Account: **{user['accountNo.']}**")
        st.info(f"Current Balance: ₹ {user['balance']}")
        
        # S5: Use st.number_input with step increments (e.g., 100, 500)
        amount = st.number_input("Amount to Withdraw", min_value=1, step=100)
        
        if st.button("Withdraw"):
            success, msg = Bank.withdraw(user['accountNo.'], user['pin'], int(amount))
            if success:
                st.success(msg)
                # S5: Display new remaining balance immediately (Update Session)
                updated_user = Bank.find_user(user['accountNo.'], user['pin'])
                if updated_user:
                    st.session_state.user = updated_user
            else:
                st.error(msg)

elif menu == "Update Info":
    st.subheader("✏️ Update Profile")
    if st.session_state.user:
        user = st.session_state.user
        with st.form("update_info_form"):
            st.write("Update any of the following fields:")
            new_name = st.text_input("New Name", value=user["name"])
            new_email = st.text_input("New Email", value=user["email"])
            new_pin = st.text_input("New PIN (4 digits, leave blank if unchanged)", type="password", max_chars=4)
            current_pin = st.text_input("Current PIN (Required to authorize changes)", type="password", max_chars=4)
            submit = st.form_submit_button("Update Info")
            
        if submit:
            if not current_pin:
                st.warning("Current PIN is required to authorize changes.")
            else:
                name_to_update = new_name if new_name != user["name"] else None
                email_to_update = new_email if new_email != user["email"] else None
                pin_to_update = new_pin if new_pin else None
                
                if pin_to_update and (len(pin_to_update) != 4 or not pin_to_update.isdigit()):
                    st.warning("New PIN must be exactly 4 digits.")
                elif not (name_to_update or email_to_update or pin_to_update):
                    st.info("No changes detected.")
                else:
                    success, msg = Bank.update_user(user["accountNo."], current_pin, name=name_to_update, email=email_to_update, new_pin=pin_to_update)
                    if success:
                        st.success(msg)
                        updated_user = Bank.find_user(user['accountNo.'], pin_to_update if pin_to_update else current_pin)
                        if updated_user:
                            st.session_state.user = updated_user
                            st.rerun()
                    else:
                        st.error(msg)

elif menu == "Delete Account":
    st.subheader("🗑️ Delete Account")
    if st.session_state.user:
        user = st.session_state.user
        st.warning(f"Warning: This action is irreversible. All data for account **{user['accountNo.']}** will be permanently deleted.")
        with st.form("delete_account_form"):
            pin_confirm = st.text_input("Enter PIN to confirm deletion", type="password", max_chars=4)
            submit = st.form_submit_button("Delete My Account")
            
        if submit:
            if pin_confirm:
                success, msg = Bank.delete_user(user["accountNo."], pin_confirm)
                if success:
                    st.session_state.user = None
                    st.success(msg)
                    st.info("Your account has been deleted. Refresh or switch to the Login menu.")
                    # Using rerun to immediately navigate away from logged-in view
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please enter your PIN to confirm.")
