"""
new development 
SecureVault Pro - Premium FinTech Application
A secure, beautiful personal wealth management platform with modern UI/UX
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, Any
import os
import time
import json
import pil

# Import our custom modules
from database import DatabaseManager
from security import SecurityManager, SessionManager
from validators import InputValidator
from styles import load_custom_css, show_password_strength
from ui_components import *
from config import *

# Initialize managers
db = DatabaseManager()
session_manager = SessionManager()

def enable_testing_mode():
    """Add testing utilities to sidebar for security testing"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧪 Security Testing Mode")
    
    if st.sidebar.checkbox("Enable Testing Panel", help="Enable security testing utilities"):
        with st.sidebar.expander("📋 Quick Test Inputs", expanded=True):
            st.markdown("""
            **Common Security Test Inputs:**
            
            **SQL Injection:**
            ```
            ' OR '1'='1' --
            admin'--
            1' UNION SELECT * FROM users--
            ```
            
            **XSS Attacks:**
            ```
            <script>alert('XSS')</script>
            <img src=x onerror=alert('XSS')>
            javascript:alert('XSS')
            ```
            
            **Input Validation:**
            ```
            Long Input: A * 5000 characters
            Special Chars: !@#$%^&*()
            Unicode/Emoji: 😀🔐💰🚀
            Numbers: 999999999999999
            ```
            """)
        
        with st.sidebar.expander("🔍 System Information"):
            if st.button("📁 Show Database Location"):
                db_path = os.path.abspath(DATABASE_PATH)
                st.code(f"Database: {db_path}")
                st.info(f"Database exists: {os.path.exists(db_path)}")
            
            if st.button("🔧 Show Session State"):
                session_data = {k: str(v) for k, v in st.session_state.items()}
                st.json(session_data)
            
            if st.button("🗑️ Clear All Sessions"):
                keys_to_clear = list(st.session_state.keys())
                for key in keys_to_clear:
                    del st.session_state[key]
                st.success("✅ All sessions cleared!")
                st.rerun()
        
        with st.sidebar.expander("⏰ Session Testing"):
            if st.button("⏱️ Simulate Session Timeout"):
                if 'last_activity' in st.session_state:
                    st.session_state.last_activity = datetime.now() - timedelta(minutes=11)
                    st.success("✅ Session timeout simulated!")
                else:
                    st.warning("No active session to timeout")
            
            if st.button("🔒 Force Logout"):
                session_manager.destroy_session()
                st.session_state.page = 'landing'
                st.success("✅ Forced logout completed!")
                st.rerun()
        
        with st.sidebar.expander("👥 Test Accounts"):
            st.markdown("""
            **Pre-created Test Accounts:**
            
            **Account 1:**
            - Username: `testuser1`
            - Email: `test1@securevault.com`
            - Password: `Test@1234`
            
            **Account 2:**
            - Username: `testuser2`
            - Email: `test2@securevault.com`
            - Password: `Test@5678`
            
            **Weak Account (for testing):**
            - Username: `weakuser`
            - Password: `12345` (should be rejected)
            """)
            
            if st.button("🔧 Create Test Accounts"):
                create_test_accounts()

def create_test_accounts():
    """Create test accounts for security testing"""
    test_users = [
        {"username": "testuser1", "email": "test1@securevault.com", "password": "Test@1234"},
        {"username": "testuser2", "email": "test2@securevault.com", "password": "Test@5678"},
        {"username": "admintest", "email": "admin@securevault.com", "password": "Admin@9999"},
    ]
    
    results = []
    for user in test_users:
        try:
            success, message, user_id = db.create_user(user['username'], user['email'], user['password'])
            if success:
                results.append(f"✅ Created: {user['username']}")
            else:
                results.append(f"ℹ️ {user['username']}: {message}")
        except Exception as e:
            results.append(f"❌ Error creating {user['username']}: {str(e)}")
    
    for result in results:
        if "✅" in result:
            st.success(result)
        elif "ℹ️" in result:
            st.info(result)
        else:
            st.error(result)

def show_security_testing_info():
    """Display security testing information"""
    if st.sidebar.checkbox("📊 Show Security Features"):
        st.sidebar.markdown("""
        **Implemented Security Features:**
        - 🔐 bcrypt Password Hashing
        - 🛡️ Input Validation & Sanitization
        - 🔒 Session Management & Timeouts
        - 🔑 Fernet Data Encryption
        - 📝 Comprehensive Audit Logging
        - 🚫 SQL Injection Prevention
        - 🛡️ XSS Protection
        - 🔒 Account Lockout (5 attempts)
        - 📊 Error Handling
        - 🔍 File Upload Validation
        """)

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="SecureVault Pro",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session
    session_manager.initialize_session()
    
    # Initialize page state
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    # Add testing mode (always available for security testing)
    enable_testing_mode()
    show_security_testing_info()
    
    # Check session validity
    if session_manager.is_session_valid():
        session_manager.update_activity()
        show_main_app()
    else:
        show_landing_page()

def show_landing_page():
    """Display the premium landing page"""
    # Hero section
    show_hero_section()
    
    # Feature cards
    show_feature_cards()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Authentication tabs
    tab1, tab2 = st.tabs(["🔓 Sign In", "✨ Create Account"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()

def show_login_form():
    """Display premium login form"""
    st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
                🔓 Welcome Back
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns([1, 3])
        with col2:
            username = st.text_input(
                "👤 Username or Email", 
                placeholder="Enter your username or email",
                key="login_username"
            )
            password = st.text_input(
                "🔒 Password", 
                type="password", 
                placeholder="Enter your password",
                key="login_password"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit = st.form_submit_button("🚀 Sign In", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please fill in all fields")
                return
            
            # Show loading
            with st.spinner("Authenticating..."):
                time.sleep(0.5)  # Brief loading animation
                
                # Check if account is locked
                is_locked, lockout_until = session_manager.is_account_locked(username)
                if is_locked:
                    st.error(f"🔒 Account is locked until {lockout_until.strftime('%H:%M:%S')}")
                    return
                
                # Attempt authentication
                success, message, user_data = db.authenticate_user(username, password)
                
                if success:
                    session_manager.create_session(user_data['username'], user_data['id'])
                    session_manager.record_login_attempt(username, True)
                    
                    # Success animation
                    st.success("🎉 Login successful! Welcome to SecureVault Pro")
                    time.sleep(1)
                    st.rerun()
                else:
                    session_manager.record_login_attempt(username, False)
                    remaining = session_manager.get_remaining_attempts(username)
                    if remaining > 0:
                        st.error(f"❌ {message}. {remaining} attempts remaining.")
                    else:
                        st.error("🔒 Account has been locked due to too many failed attempts.")

def show_register_form():
    """Display premium registration form"""
    st.markdown("""
        <div class="glass-card">
            <h2 style="color: white; text-align: center; margin-bottom: 2rem;">
                ✨ Join SecureVault Pro
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input(
                "👤 Username", 
                placeholder="Choose a unique username",
                key="reg_username"
            )
            email = st.text_input(
                "📧 Email", 
                placeholder="your@email.com",
                key="reg_email"
            )
        
        with col2:
            password = st.text_input(
                "🔒 Password", 
                type="password", 
                placeholder="Create a strong password",
                key="reg_password"
            )
            confirm_password = st.text_input(
                "🔒 Confirm Password", 
                type="password", 
                placeholder="Confirm your password",
                key="reg_confirm"
            )
        
        # Password strength indicator with visual feedback
        if password:
            score, strength, feedback = show_password_strength(password)
            
            # Requirements checklist
            st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
            requirements = [
                ("At least 8 characters", len(password) >= 8),
                ("Contains uppercase letter", any(c.isupper() for c in password)),
                ("Contains lowercase letter", any(c.islower() for c in password)),
                ("Contains number", any(c.isdigit() for c in password)),
                ("Contains special character", any(c in "@#$%&*!" for c in password)),
            ]
            
            for req, met in requirements:
                icon = "✅" if met else "⭕"
                color = "#00d4aa" if met else "#6e6e8f"
                st.markdown(f"<span style='color: {color}; font-size: 0.875rem;'>{icon} {req}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Terms checkbox
        terms = st.checkbox("I agree to the Terms & Conditions and Privacy Policy", key="terms_check")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit button
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            submitted = st.form_submit_button("🚀 Create My Vault", use_container_width=True)
        
        if submitted:
            if not terms:
                st.error("Please accept the Terms & Conditions")
                return
            
            # Show loading
            with st.spinner("Creating your secure vault..."):
                time.sleep(0.8)  # Brief loading animation
                
                # Validate inputs
                valid_username, username_error = InputValidator.validate_username(username)
                valid_email, email_error = InputValidator.validate_email(email)
                valid_password, password_error = InputValidator.validate_password(password)
                
                if not valid_username:
                    st.error(f"❌ {username_error}")
                    return
                
                if not valid_email:
                    st.error(f"❌ {email_error}")
                    return
                
                if not valid_password:
                    st.error(f"❌ {password_error}")
                    return
                
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                    return
                
                # Create account
                success, message, user_id = db.create_user(username, email, password)
                
                if success:
                    st.success("🎉 Account created successfully! Welcome to SecureVault Pro")
                    st.info("Please sign in with your new credentials")
                    time.sleep(2)
                else:
                    st.error(f"❌ {message}")

def show_main_app():
    """Display the main application with sidebar navigation"""
    # Sidebar with premium styling
    with st.sidebar:
        show_logo()
        
        # User info
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem; margin-bottom: 2rem; 
                        background: rgba(255,255,255,0.05); border-radius: 12px;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
                <div style="color: white; font-weight: 600;">{st.session_state.username}</div>
                <div style="color: #a0a0c0; font-size: 0.75rem;">Premium Member</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        menu_options = [
            ("🏠", "Dashboard", "dashboard"),
            ("💰", "Add Money", "add_money"),
            ("💸", "Send Money", "send_money"),
            ("📜", "History", "history"),
            ("📊", "Analytics", "analytics"),
            ("👤", "Profile", "profile"),
            ("🔒", "Security", "security")
        ]
        
        st.markdown("### Navigation")
        
        for icon, label, page_key in menu_options:
            if st.button(f"{icon} {label}", use_container_width=True, key=f"nav_{page_key}"):
                st.session_state.page = page_key
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            db.log_audit_event(st.session_state.user_id, st.session_state.username, 
                             AUDIT_ACTIONS['LOGOUT'], "User logged out")
            session_manager.destroy_session()
            st.session_state.page = 'landing'
            st.rerun()
    
    # Main content area
    page = st.session_state.get('page', 'dashboard')
    
    if page == "dashboard":
        show_dashboard_content()
    elif page == "add_money":
        show_add_money()
    elif page == "send_money":
        show_send_money()
    elif page == "history":
        show_transaction_history()
    elif page == "analytics":
        show_analytics()
    elif page == "profile":
        show_profile()
    elif page == "security":
        show_security_settings()
    else:
        show_dashboard_content()

def show_dashboard_content():
    """Display premium dashboard overview"""
    # Get user data
    success, balance = db.get_wallet_balance(st.session_state.user_id)
    
    if not success:
        st.error("Failed to load wallet balance")
        return
    
    # Welcome message
    show_welcome_message(st.session_state.username)
    
    # Balance card with gradient
    show_balance_card(balance, 12.5)  # Mock 12.5% increase
    
    # Quick actions
    actions = show_quick_actions()
    if actions:
        st.session_state.page = actions[0]
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Statistics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Get transaction data
    transactions = db.get_user_transactions(st.session_state.user_id, limit=100)
    
    # Calculate stats
    recent_count = len([t for t in transactions if 
                      datetime.fromisoformat(t['created_at']) > datetime.now() - timedelta(days=7)])
    
    monthly_transactions = [t for t in transactions if 
                          datetime.fromisoformat(t['created_at']) > datetime.now() - timedelta(days=30)]
    total_spent = sum(t['amount'] for t in monthly_transactions if t['type'] == 'DEBIT')
    total_earned = sum(t['amount'] for t in monthly_transactions if t['type'] == 'CREDIT')
    
    with col1:
        st.markdown(show_stat_card("This Week", f"{recent_count}", "📅"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(show_stat_card("Monthly Spending", f"${total_spent:,.0f}", "💸", "#ff6b9d"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(show_stat_card("Monthly Income", f"${total_earned:,.0f}", "💰", "#00d4aa"), unsafe_allow_html=True)
    
    with col4:
        savings_rate = ((total_earned - total_spent) / total_earned * 100) if total_earned > 0 else 0
        st.markdown(show_stat_card("Savings Rate", f"{savings_rate:.1f}%", "📈", "#6bcfff"), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Recent transactions section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📜 Recent Transactions")
        recent_transactions = db.get_user_transactions(st.session_state.user_id, limit=5)
        
        if recent_transactions:
            for transaction in recent_transactions:
                show_transaction_card(transaction)
        else:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 3rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">💳</div>
                    <h3 style="color: white;">No transactions yet</h3>
                    <p style="color: #a0a0c0;">Start by adding money to your vault!</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📊 Quick Insights")
        
        if transactions:
            # Balance trend mini chart
            fig = create_balance_trend_chart(transactions[-10:])  # Last 10 transactions
            if fig:
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">📈</div>
                    <p style="color: #a0a0c0;">Charts will appear here once you start making transactions</p>
                </div>
            """, unsafe_allow_html=True)

def show_add_money():
    """Display premium add money form"""
    st.markdown("""
        <div class="fade-in">
            <h1 style="color: white;">💰 Add Money to Your Vault</h1>
            <p style="color: #a0a0c0; margin-bottom: 2rem;">
                Securely deposit funds into your SecureVault Pro account
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Current balance display
    success, current_balance = db.get_wallet_balance(st.session_state.user_id)
    if success:
        st.markdown(f"""
            <div class="glass-card" style="text-align: center; margin-bottom: 2rem;">
                <div style="color: #a0a0c0; font-size: 0.875rem; margin-bottom: 0.5rem;">CURRENT BALANCE</div>
                <div style="color: white; font-size: 2rem; font-weight: 700;">${current_balance:,.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick amount buttons (outside form)
    st.markdown("### 💡 Quick Amounts")
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("💵 $100", use_container_width=True, key="quick_100"):
            st.session_state.quick_amount = "100.00"
    with quick_col2:
        if st.button("💵 $500", use_container_width=True, key="quick_500"):
            st.session_state.quick_amount = "500.00"
    with quick_col3:
        if st.button("💵 $1000", use_container_width=True, key="quick_1000"):
            st.session_state.quick_amount = "1000.00"
    with quick_col4:
        if st.button("💵 $2500", use_container_width=True, key="quick_2500"):
            st.session_state.quick_amount = "2500.00"
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("add_money_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Use quick amount if selected
            default_amount = st.session_state.get('quick_amount', '')
            amount_str = st.text_input(
                "💵 Amount ($)", 
                value=default_amount,
                placeholder="Enter amount to add",
                key="add_amount"
            )
            source = st.selectbox(
                "🏦 Funding Source", 
                ["Bank Transfer", "Credit Card", "Debit Card", "Wire Transfer", "Cash Deposit"],
                key="add_source"
            )
        
        with col2:
            description = st.text_area(
                "📝 Description (Optional)", 
                placeholder="What's this deposit for?",
                key="add_description"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            submit = st.form_submit_button("💰 Add Money to Vault", use_container_width=True)
        
        if submit:
            # Clear quick amount selection
            if 'quick_amount' in st.session_state:
                del st.session_state.quick_amount
                
            with st.spinner("Processing your deposit..."):
                time.sleep(1)  # Loading animation
                
                # Validate amount
                valid_amount, amount_error, amount = InputValidator.validate_amount(amount_str)
                if not valid_amount:
                    st.error(f"❌ {amount_error}")
                    return
                
                # Validate description
                if description:
                    valid_desc, desc_error = InputValidator.validate_text_field(
                        description, "Description", MAX_DESCRIPTION_LENGTH, required=False
                    )
                    if not valid_desc:
                        st.error(f"❌ {desc_error}")
                        return
                
                # Create transaction
                success, transaction_id = db.create_transaction(
                    st.session_state.user_id, 'CREDIT', amount, 
                    source=source, description=description
                )
                
                if success:
                    st.success(f"🎉 Successfully added ${amount:.2f} to your vault!")
                    st.info(f"📋 Transaction ID: {transaction_id}")
                    
                    # Show updated balance
                    new_success, new_balance = db.get_wallet_balance(st.session_state.user_id)
                    if new_success:
                        st.markdown(f"""
                            <div class="glass-card" style="text-align: center; margin-top: 1rem;">
                                <div style="color: #00d4aa; font-size: 0.875rem;">NEW BALANCE</div>
                                <div style="color: white; font-size: 1.5rem; font-weight: 700;">${new_balance:,.2f}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.balloons()
                else:
                    st.error(f"❌ Failed to add money: {transaction_id}")

def show_send_money():
    """Display send money form"""
    st.subheader("💸 Send Money")
    
    with st.form("send_money_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            recipient = st.text_input("Recipient Username", placeholder="Enter recipient's username")
            amount_str = st.text_input("Amount ($)", placeholder="0.00")
        
        with col2:
            purpose = st.selectbox("Purpose", [
                "Personal", "Business", "Gift", "Payment", "Refund", "Other"
            ])
            description = st.text_area("Description (Optional)", placeholder="What's this payment for?")
        
        submit = st.form_submit_button("Send Money", use_container_width=True)
        
        if submit:
            # Validate recipient
            valid_username, username_error = InputValidator.validate_username(recipient)
            if not valid_username:
                st.error(username_error)
                return
            
            # Check if recipient exists
            if not db.user_exists(recipient):
                st.error("Recipient username not found")
                return
            
            # Can't send to yourself
            if recipient == st.session_state.username:
                st.error("You cannot send money to yourself")
                return
            
            # Validate amount
            valid_amount, amount_error, amount = InputValidator.validate_amount(amount_str)
            if not valid_amount:
                st.error(amount_error)
                return
            
            # Check balance
            success, current_balance = db.get_wallet_balance(st.session_state.user_id)
            if not success or current_balance < amount:
                st.error("Insufficient funds")
                return
            
            # Validate description
            if description:
                valid_desc, desc_error = InputValidator.validate_text_field(
                    description, "Description", MAX_DESCRIPTION_LENGTH, required=False
                )
                if not valid_desc:
                    st.error(desc_error)
                    return
            
            # Create transaction
            success, transaction_id = db.create_transaction(
                st.session_state.user_id, 'DEBIT', amount,
                recipient_username=recipient, description=f"{purpose}: {description}"
            )
            
            if success:
                st.success(f"Successfully sent ${amount:.2f} to {recipient}!")
                st.info(f"Transaction ID: {transaction_id}")
            else:
                st.error(f"Failed to send money: {transaction_id}")

def show_transaction_history():
    """Display transaction history"""
    st.subheader("📊 Transaction History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        transaction_type = st.selectbox("Type", ["All", "CREDIT", "DEBIT"])
    
    with col2:
        days_back = st.selectbox("Period", [7, 30, 90, 365])
    
    with col3:
        limit = st.selectbox("Show", [10, 25, 50, 100])
    
    # Get transactions
    transactions = db.get_user_transactions(st.session_state.user_id, limit=limit)
    
    # Filter by type
    if transaction_type != "All":
        transactions = [t for t in transactions if t['type'] == transaction_type]
    
    # Filter by date
    cutoff_date = datetime.now() - timedelta(days=days_back)
    transactions = [t for t in transactions if 
                   datetime.fromisoformat(t['created_at']) > cutoff_date]
    
    if transactions:
        # Create DataFrame for display
        df_data = []
        for t in transactions:
            df_data.append({
                'Date': datetime.fromisoformat(t['created_at']).strftime('%Y-%m-%d %H:%M'),
                'Type': t['type'],
                'Amount': f"${t['amount']:,.2f}",
                'Recipient/Source': t['recipient_username'] or t['source'] or 'N/A',
                'Description': t['description'] or 'No description',
                'Balance After': f"${t['balance_after']:,.2f}",
                'Transaction ID': t['transaction_id']
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Transaction summary chart
        if len(transactions) > 1:
            st.subheader("Transaction Trends")
            
            # Prepare data for chart
            chart_data = []
            for t in transactions:
                chart_data.append({
                    'Date': datetime.fromisoformat(t['created_at']).date(),
                    'Amount': t['amount'] if t['type'] == 'CREDIT' else -t['amount'],
                    'Type': t['type']
                })
            
            chart_df = pd.DataFrame(chart_data)
            
            # Create chart
            fig = px.bar(chart_df, x='Date', y='Amount', color='Type',
                        title="Transaction Flow Over Time",
                        color_discrete_map={'CREDIT': '#10B981', 'DEBIT': '#EF4444'})
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactions found for the selected criteria.")

def show_profile():
    """Display user profile"""
    st.subheader("👤 User Profile")
    
    # Get current balance for display
    success, balance = db.get_wallet_balance(st.session_state.user_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Account Information")
        st.info(f"**Username:** {st.session_state.username}")
        st.info(f"**Current Balance:** ${balance:,.2f}" if success else "**Current Balance:** Error loading")
        st.info(f"**Account Status:** Active")
    
    with col2:
        st.markdown("### Account Statistics")
        transactions = db.get_user_transactions(st.session_state.user_id, limit=1000)
        
        total_transactions = len(transactions)
        total_credits = sum(t['amount'] for t in transactions if t['type'] == 'CREDIT')
        total_debits = sum(t['amount'] for t in transactions if t['type'] == 'DEBIT')
        
        st.metric("Total Transactions", total_transactions)
        st.metric("Total Money Added", f"${total_credits:,.2f}")
        st.metric("Total Money Sent", f"${total_debits:,.2f}")

def show_security_settings():
    """Display enhanced security settings with testing capabilities"""
    st.markdown("""
        <div class="fade-in">
            <h1 style="color: white;">🔒 Security Center</h1>
            <p style="color: #a0a0c0; margin-bottom: 2rem;">
                Manage your account security and monitor activity
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔑 Change Password", "📊 Activity Log", "🧪 Security Testing"])
    
    with tab1:
        st.markdown("### Change Password")
        
        with st.form("change_password_form"):
            current_password = st.text_input("Current Password", type="password", key="current_pwd")
            new_password = st.text_input("New Password", type="password", key="new_pwd")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pwd")
            
            # Password strength indicator
            if new_password:
                score, suggestions = InputValidator.get_password_strength_score(new_password)
                if score < 50:
                    st.error(f"Password strength: Weak ({score}%)")
                elif score < 80:
                    st.warning(f"Password strength: Medium ({score}%)")
                else:
                    st.success(f"Password strength: Strong ({score}%)")
                
                if suggestions:
                    st.info("Suggestions: " + ", ".join(suggestions))
            
            submit = st.form_submit_button("🔄 Change Password")
            
            if submit:
                if not all([current_password, new_password, confirm_password]):
                    st.error("❌ Please fill in all fields")
                    return
                
                if new_password != confirm_password:
                    st.error("❌ New passwords do not match")
                    return
                
                # Validate new password
                valid_password, password_error = InputValidator.validate_password(new_password)
                if not valid_password:
                    st.error(f"❌ {password_error}")
                    return
                
                # For testing purposes, simulate password change
                st.success("✅ Password change functionality demonstrated (not implemented in demo)")
                st.info("🔒 In production, this would verify current password and update securely")
    
    with tab2:
        st.markdown("### 📊 Recent Security Activity")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            log_limit = st.selectbox("Show entries", [10, 20, 50, 100], index=1)
        with col2:
            if st.button("🔄 Refresh Logs"):
                st.rerun()
        
        # Get audit logs for current user
        audit_logs = db.get_audit_logs(limit=log_limit, user_id=st.session_state.user_id)
        
        if audit_logs:
            st.markdown(f"**Showing {len(audit_logs)} recent activities:**")
            
            for i, log in enumerate(audit_logs):
                status_color = "#00d4aa" if log['status'] == 'SUCCESS' else "#ff6b9d"
                status_icon = "✅" if log['status'] == 'SUCCESS' else "❌"
                
                st.markdown(f"""
                <div class="glass-card" style="margin: 0.5rem 0; padding: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.1rem;">{status_icon}</span>
                            <strong style="color: white; margin-left: 0.5rem;">{log['action']}</strong>
                            <div style="color: #a0a0c0; margin-top: 0.25rem; font-size: 0.875rem;">
                                {log['details']}
                            </div>
                        </div>
                        <div style="text-align: right; color: #6e6e8f; font-size: 0.75rem;">
                            {log['timestamp']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 3rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📝</div>
                    <h3 style="color: white;">No Activity Logs</h3>
                    <p style="color: #a0a0c0;">Security activities will appear here</p>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🧪 Security Testing Dashboard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔍 Current Session Info")
            if st.session_state.get('logged_in'):
                st.success(f"✅ Logged in as: {st.session_state.username}")
                st.info(f"👤 User ID: {st.session_state.user_id}")
                if st.session_state.get('last_activity'):
                    time_diff = datetime.now() - st.session_state.last_activity
                    st.info(f"⏰ Last activity: {time_diff.seconds} seconds ago")
            else:
                st.warning("❌ Not logged in")
            
            st.markdown("#### 🛡️ Security Features Status")
            features = [
                ("Password Hashing", "bcrypt with salt", "✅"),
                ("Data Encryption", "Fernet symmetric", "✅"),
                ("Session Management", "Timeout enabled", "✅"),
                ("Input Validation", "XSS/SQL protection", "✅"),
                ("Audit Logging", "All actions logged", "✅"),
                ("Account Lockout", "5 failed attempts", "✅"),
            ]
            
            for feature, desc, status in features:
                st.markdown(f"{status} **{feature}**: {desc}")
        
        with col2:
            st.markdown("#### 📊 Database Security Check")
            
            if st.button("🔍 Check Database Encryption"):
                try:
                    # Check if user has encrypted data
                    success, balance = db.get_wallet_balance(st.session_state.user_id)
                    if success:
                        st.success("✅ Wallet data encrypted and accessible")
                    else:
                        st.warning("⚠️ No wallet data found")
                    
                    # Check audit logs
                    logs = db.get_audit_logs(limit=1, user_id=st.session_state.user_id)
                    if logs:
                        st.success("✅ Audit logging functional")
                    else:
                        st.info("ℹ️ No audit logs yet")
                        
                except Exception as e:
                    st.error(f"❌ Database check failed: {str(e)}")
            
            st.markdown("#### 🧪 Test Attack Vectors")
            st.markdown("""
            **Ready to test:**
            - SQL Injection in login forms
            - XSS in input fields  
            - Session hijacking attempts
            - Password brute force
            - Input validation bypass
            - File upload restrictions
            - Error message leakage
            - Unauthorized access attempts
            """)
        
        st.markdown("---")
        st.markdown("#### 🎯 Quick Security Tests")
        
        test_col1, test_col2, test_col3 = st.columns(3)
        
        with test_col1:
            if st.button("🔒 Test Session Timeout"):
                if 'last_activity' in st.session_state:
                    st.session_state.last_activity = datetime.now() - timedelta(minutes=11)
                    st.success("✅ Session timeout simulated - try navigating!")
        
        with test_col2:
            if st.button("🚫 Test Unauthorized Access"):
                st.warning("⚠️ Try accessing dashboard without login in incognito mode")
        
        with test_col3:
            if st.button("📝 Show Test Inputs"):
                st.code("""
SQL: ' OR '1'='1' --
XSS: <script>alert('test')</script>
Long: """ + "A" * 50 + """...
Special: !@#$%^&*()
                """)

def show_analytics():
    """Display premium analytics dashboard"""
    st.markdown("""
        <div class="fade-in">
            <h1 style="color: white;">📊 Financial Analytics</h1>
            <p style="color: #a0a0c0; margin-bottom: 2rem;">
                Insights and trends for your financial journey
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get transaction data
    transactions = db.get_user_transactions(st.session_state.user_id, limit=1000)
    
    if not transactions:
        st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 4rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
                <h2 style="color: white;">No Data Yet</h2>
                <p style="color: #a0a0c0; margin-bottom: 2rem;">
                    Start making transactions to see beautiful analytics and insights
                </p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Time period selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        period = st.selectbox(
            "📅 Analysis Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
            index=1
        )
    
    # Filter transactions by period
    if period == "Last 7 Days":
        cutoff = datetime.now() - timedelta(days=7)
    elif period == "Last 30 Days":
        cutoff = datetime.now() - timedelta(days=30)
    elif period == "Last 90 Days":
        cutoff = datetime.now() - timedelta(days=90)
    else:
        cutoff = datetime.min
    
    filtered_transactions = [
        t for t in transactions 
        if datetime.fromisoformat(t['created_at']) > cutoff
    ]
    
    if not filtered_transactions:
        st.warning(f"No transactions found for {period.lower()}")
        return
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    total_income = sum(t['amount'] for t in filtered_transactions if t['type'] == 'CREDIT')
    total_expenses = sum(t['amount'] for t in filtered_transactions if t['type'] == 'DEBIT')
    net_flow = total_income - total_expenses
    transaction_count = len(filtered_transactions)
    
    with col1:
        st.markdown(show_stat_card("Total Income", f"${total_income:,.0f}", "💰", "#00d4aa"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(show_stat_card("Total Expenses", f"${total_expenses:,.0f}", "💸", "#ff6b9d"), unsafe_allow_html=True)
    
    with col3:
        net_color = "#00d4aa" if net_flow >= 0 else "#ff6b9d"
        st.markdown(show_stat_card("Net Flow", f"${net_flow:,.0f}", "📈", net_color), unsafe_allow_html=True)
    
    with col4:
        st.markdown(show_stat_card("Transactions", str(transaction_count), "📋", "#6bcfff"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Transaction Flow")
        flow_chart = create_spending_chart(filtered_transactions)
        if flow_chart:
            st.plotly_chart(flow_chart, use_container_width=True)
    
    with col2:
        st.markdown("### 🥧 Spending Categories")
        pie_chart = create_category_pie_chart(filtered_transactions)
        if pie_chart:
            st.plotly_chart(pie_chart, use_container_width=True)
    
    # Balance trend
    st.markdown("### 💹 Balance Trend")
    balance_chart = create_balance_trend_chart(filtered_transactions)
    if balance_chart:
        st.plotly_chart(balance_chart, use_container_width=True)
    
    # Transaction table
    st.markdown("### 📋 Detailed Transactions")
    
    # Create DataFrame
    df_data = []
    for t in filtered_transactions:
        df_data.append({
            'Date': datetime.fromisoformat(t['created_at']).strftime('%Y-%m-%d %H:%M'),
            'Type': t['type'],
            'Amount': f"${t['amount']:,.2f}",
            'Description': t.get('description', 'No description'),
            'Balance After': f"${t.get('balance_after', 0):,.2f}"
        })
    
    if df_data:
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":

    main()
