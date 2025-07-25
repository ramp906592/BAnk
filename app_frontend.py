import streamlit as st
from bank_backend import BANK
import time

def show_loading():
    with st.spinner('Processing...'):
        time.sleep(0.5)

def show_success(message):
    st.success(message)
    time.sleep(0.5)

st.markdown("""
<style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
    .stButton>button {
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

BANK.load_data()
st.set_page_config(page_title="Simple Banking System", page_icon="🏦", layout="wide")
st.title("🏦 Simple Banking System")
st.markdown("<div class='fade-in'>", unsafe_allow_html=True)

MENU_OPTIONS = [
    "Create Account", 
    "Deposit", 
    "Withdraw", 
    "Show Details", 
    "Update Details", 
    "Delete Account"
]
menu = st.sidebar.selectbox("Choose Action", MENU_OPTIONS)

if menu == "Create Account":
    st.subheader("Open New Account")
    with st.form("create_account"):
        name = st.text_input("Full Name")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=1, max_value=120)
        with col2:
            pin = st.text_input("4-digit PIN", type="password", max_chars=4)
        email = st.text_input("Email Address")
        if st.form_submit_button("Create Account"):
            if not all([name, age, pin, email]):
                st.error("Please fill in all fields")
            elif not pin.isdigit() or len(pin) != 4:
                st.error("PIN must be 4 digits")
            else:
                show_loading()
                try:
                    success, result = BANK.create_account(name, int(age), email, int(pin))
                    if success:
                        show_success("🎉 Account created successfully!")
                        with st.expander("View Account Details"):
                            st.json(result)
                    else:
                        st.error(f"❌ Error: {result}")
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
else:
    st.subheader("Account Login")
    with st.form("login"):
        acc_no = st.text_input("Account Number").strip()
        pin = st.text_input("PIN", type="password")
        if st.form_submit_button("Login"):
            st.session_state.user = None
            if acc_no and pin and pin.isdigit():
                show_loading()
                try:
                    user = BANK.validate_user(acc_no, int(pin))
                    if user:
                        st.session_state.user = user
                        show_success("🔓 Login successful! Welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    if hasattr(st.session_state, 'user') and st.session_state.user:
        user = st.session_state.user
        if menu == "Deposit":
            st.subheader("💵 Deposit Money")
            with st.form("deposit"):
                amount = st.number_input("Amount", min_value=1, max_value=10000, step=1)
                if st.form_submit_button("💾 Deposit"):
                    show_loading()
                    success, msg = BANK.deposit_money(user, amount)
                    if success:
                        show_success(f"✅ {msg}")
                        st.session_state.user = BANK.validate_user(user['accountNo'], user['pin'])
                    else:
                        st.error(f"❌ {msg}")
        elif menu == "Withdraw":
            st.subheader("💰 Withdraw Money")
            with st.form("withdraw"):
                amount = st.number_input("Amount", min_value=1, step=1)
                if st.form_submit_button("💸 Withdraw"):
                    show_loading()
                    success, msg = BANK.withdraw_money(user, amount)
                    if success:
                        show_success(f"✅ {msg}")
                        st.session_state.user = BANK.validate_user(user['accountNo'], user['pin'])
                    else:
                        st.error(f"❌ {msg}")
        elif menu == "Show Details":
            st.subheader("📋 Account Information")
            with st.container():
                st.markdown(f"""
                <style>
                .account-card {{
                    padding: 24px;
                    border-radius: 16px;
                    background: linear-gradient(135deg, #232526 0%, #414345 100%);
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                    margin: 10px 0;
                    animation: fadeIn 0.8s ease-out;
                }}
                .account-field {{
                    margin: 12px 0;
                    padding: 10px;
                    border-bottom: 1px solid #444;
                    color: #f8f8f8;
                    font-size: 1.1rem;
                }}
                .account-field:last-child {{
                    border-bottom: none;
                }}
                .account-card strong {{
                    color: #00e6d0;
                }}
                </style>
                <div class='account-card'>
                    <div class='account-field'><strong>👤 Name:</strong> {user.get('name', 'N/A')}</div>
                    <div class='account-field'><strong>🔢 Account #:</strong> {user.get('accountNo', 'N/A')}</div>
                    <div class='account-field'><strong>💰 Balance:</strong> ₹{float(user.get('balance', 0)):,}</div>
                    <div class='account-field'><strong>📧 Email:</strong> {user.get('email', 'N/A')}</div>
                    <div class='account-field'><strong>🎂 Age:</strong> {user.get('age', 'N/A')}</div>
                </div>
                """, unsafe_allow_html=True)
            with st.expander("View Raw Data"):
                st.json(user)
        elif menu == "Update Details":
            st.subheader("🔄 Update Account Information")
            with st.form("update"):
                new_name = st.text_input("Full Name", value=user.get('name', ''))
                new_email = st.text_input("Email", value=user.get('email', ''))
                new_pin = st.text_input("New 4-digit PIN", type="password", max_chars=4, help="Leave empty to keep current PIN")
                if st.form_submit_button("🔄 Update Profile"):
                    if new_pin and (not new_pin.isdigit() or len(new_pin) != 4):
                        st.error("❌ PIN must be 4 digits")
                    else:
                        show_loading()
                        success, msg = BANK.update_user(
                            user, 
                            new_name or user.get('name'),
                            new_email or user.get('email'),
                            int(new_pin) if new_pin else user.get('pin')
                        )
                        if success:
                            st.session_state.user = BANK.validate_user(
                                user['accountNo'], 
                                int(new_pin) if new_pin else user.get('pin')
                            )
                            show_success(f"✅ {msg}")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg}")
        elif menu == "Delete Account":
            st.subheader("🗑️ Delete Account")
            st.warning("⚠️ This action is permanent and cannot be undone!")
            if not st.session_state.get('confirm_delete', False):
                if st.button("Delete My Account", type="primary"):
                    st.session_state.confirm_delete = True
                    st.rerun()
            else:
                st.error("Are you absolutely sure? This will permanently delete all your account data!")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, delete my account", type="primary"):
                        show_loading()
                        msg = BANK.delete_account(user)
                        show_success(msg)
                        st.session_state.user = None
                        st.session_state.confirm_delete = False
                        st.rerun()
                with col2:
                    if st.button("❌ No, keep my account"):
                        st.session_state.confirm_delete = False
                        st.rerun()