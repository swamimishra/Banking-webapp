import random
import string
import streamlit as st
from supabase import create_client, Client

class Bank:
    # Initialize Supabase Client
    # Expects st.secrets["SUPABASE_URL"] and st.secrets["SUPABASE_KEY"]
    
    MAX_TRANSACTION_LIMIT = 10000

    @staticmethod
    def _get_client() -> Client:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)

    @classmethod
    def generate_account_number(cls):
        # Unique alphanumeric Account ID (random + string)
        # Using 8 characters for enough entropy
        chars = random.choices(string.ascii_uppercase + string.digits, k=8)
        random.shuffle(chars)
        return ''.join(chars)

    @classmethod
    def create_account(cls, name, age, email, pin):
        if age < 18 or len(str(pin)) != 4:
            return None, "Age must be 18+ and PIN should be 4 digits"
        
        supabase = cls._get_client()
        acc_no = None

        # Loop check: SELECT 1 to ensure ID does not already exist
        for _ in range(5):
            temp_acc_no = cls.generate_account_number()
            try:
                # Check uniqueness
                response = supabase.table("users").select("account_number").eq("account_number", temp_acc_no).execute()
                if not response.data:
                    acc_no = temp_acc_no
                    break
            except Exception:
                continue

        if not acc_no:
             return None, "Failed to generate a unique account number. Please try again."

        user_data = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "account_number": acc_no,
            "balance": 0
        }

        try:
            response = supabase.table("users").insert(user_data).execute()
            # Check if insertion was successful (response.data should not be empty)
            if response.data:
                 return {"accountNo.": acc_no}, "Account created successfully" # Returning dict with key expected by app.py
            else:
                 return None, "Failed to create account (No data returned)"

        except Exception as e:
            return None, f"Error creating account: {str(e)}"

    # Placeholder/Legacy methods - needing update for full DB support
    @classmethod
    def find_user(cls, acc_no, pin):
        try:
            supabase = cls._get_client()
            response = supabase.table("users").select("*") \
                .eq("account_number", acc_no) \
                .eq("pin", int(pin)) \
                .execute()
            
            if response.data:
                user = response.data[0]
                user['accountNo.'] = user['account_number']
                return user
            return None
        except Exception as e:
            print(f"Supabase Error: {e}")
            return None

    @classmethod
    def deposit(cls, acc_no, pin, amount):
        if amount <= 0:
            return False, "Amount must be positive"
        
        if amount > cls.MAX_TRANSACTION_LIMIT:
            return False, f"Transaction limit exceeded. Max limit is ₹{cls.MAX_TRANSACTION_LIMIT}"

        try:
            supabase = cls._get_client()
            
            # Fetch current user details to verify and get current balance
            response = supabase.table("users").select("*") \
                .eq("account_number", acc_no) \
                .eq("pin", int(pin)) \
                .execute()
            
            if not response.data:
                return False, "Invalid Account Number or PIN"
            
            user = response.data[0]
            current_balance = user['balance']
            
            # Update balance
            new_balance = current_balance + amount
            
            update_response = supabase.table("users") \
                .update({"balance": new_balance}) \
                .eq("account_number", acc_no) \
                .execute()
            
            if update_response.data:
                return True, f"Deposit Successful! New Balance: ₹ {new_balance}"
            else:
                return False, "Transaction Failed (Database Error)"
                
        except Exception as e:
            return False, f"Error processing deposit: {str(e)}"

    @classmethod
    def withdraw(cls, acc_no, pin, amount):
        if amount <= 0:
             return False, "Amount must be positive"

        if amount > cls.MAX_TRANSACTION_LIMIT:
            return False, f"Transaction limit exceeded. Max limit is ₹{cls.MAX_TRANSACTION_LIMIT}"
             
             
        try:
            supabase = cls._get_client()
            # 1. Fetch current balance (Atomic check start)
            # We fetch using account_number and PIN to verify owner
            response = supabase.table("users").select("*") \
                .eq("account_number", acc_no) \
                .eq("pin", int(pin)) \
                .execute()
            
            if not response.data:
                return False, "Invalid Account Number or PIN"
            
            user = response.data[0]
            current_balance = user['balance']
            
            # 2. Check sufficient funds
            if current_balance < amount:
                return False, "Insufficient Funds"
                
            # 3. Update balance
            new_balance = current_balance - amount
            update_response = supabase.table("users") \
                .update({"balance": new_balance}) \
                .eq("account_number", acc_no) \
                .execute()
            
            if update_response.data:
                return True, f"Withdrawal Successful! New Balance: ₹ {new_balance}"
            else:
                return False, "Transaction Failed (Database Error)"
                
        except Exception as e:
            return False, f"Error processing withdrawal: {str(e)}"

    @classmethod
    def update_user(cls, acc_no, pin, name=None, email=None, new_pin=None):
         # TODO: Update to update Supabase
        pass

    @classmethod
    def delete_user(cls, acc_no, pin):
         # TODO: Update to delete from Supabase
        pass

