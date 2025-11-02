"""
Custom UI components for SecureVault Pro
Beautiful, reusable components with glassmorphism effects
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

def show_logo():
    """Display the SecureVault Pro logo"""
    st.markdown("""
        <div class="logo-container">
            <div class="logo-text">🔐 SecureVault Pro</div>
            <div class="logo-tagline">Your Wealth, Secured & Simplified</div>
        </div>
    """, unsafe_allow_html=True)

def show_hero_section():
    """Display the landing page hero section"""
    st.markdown("""
        <div class="hero-section fade-in">
            <div class="hero-title">🔐 SecureVault Pro</div>
            <div class="hero-subtitle">Your Wealth, Secured & Simplified</div>
            <p style="color: #6e6e8f; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                Experience next-generation financial management with bank-grade security,
                beautiful design, and intelligent insights. Your financial future starts here.
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_feature_cards():
    """Display feature cards on landing page"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
                <h3 style="color: white; margin-bottom: 1rem;">Bank-Grade Security</h3>
                <p style="color: #a0a0c0; line-height: 1.5;">
                    256-bit encryption, bcrypt hashing, and multi-layer protection 
                    keep your financial data absolutely secure.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: white; margin-bottom: 1rem;">Lightning Fast</h3>
                <p style="color: #a0a0c0; line-height: 1.5;">
                    Instant transactions with real-time updates and notifications.
                    Experience seamless financial management.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: white; margin-bottom: 1rem;">Smart Analytics</h3>
                <p style="color: #a0a0c0; line-height: 1.5;">
                    AI-powered insights and beautiful visualizations help you
                    make informed financial decisions.
                </p>
            </div>
        """, unsafe_allow_html=True)

def show_balance_card(balance, change_percent=None):
    """Display the main balance card with gradient background"""
    change_html = ""
    if change_percent is not None:
        color = "#00d4aa" if change_percent >= 0 else "#ff6b9d"
        arrow = "↑" if change_percent >= 0 else "↓"
        change_html = f'<div style="margin-top: 1rem;"><span style="color: rgba(255,255,255,0.8);"><span style="color: {color};">{arrow} {abs(change_percent):.1f}%</span> vs last month</span></div>'
    
    balance_html = f"""
        <div class="balance-card fade-in">
            <div class="balance-label">Total Balance</div>
            <div class="balance-amount">${balance:,.2f}</div>
            {change_html}
        </div>
    """
    
    st.markdown(balance_html, unsafe_allow_html=True)

def show_stat_card(title, value, icon="📊", color="#667eea"):
    """Display a statistics card"""
    return f"""
        <div class="stat-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div class="stat-value" style="color: {color};">{value}</div>
            <div class="stat-label">{title}</div>
        </div>
    """

def show_transaction_card(transaction):
    """Display a transaction card"""
    transaction_type = "CREDIT" if transaction['type'] == 'CREDIT' else "DEBIT"
    icon = "💰" if transaction['type'] == 'CREDIT' else "💸"
    amount_color = "#00d4aa" if transaction['type'] == 'CREDIT' else "#ff6b9d"
    card_class = "transaction-credit" if transaction['type'] == 'CREDIT' else "transaction-debit"
    
    # Format date
    try:
        date_obj = datetime.fromisoformat(transaction['created_at'])
        formatted_date = date_obj.strftime('%b %d, %Y at %I:%M %p')
    except:
        formatted_date = transaction['created_at']
    
    st.markdown(f"""
        <div class="transaction-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                        <strong style="color: white;">{transaction_type}</strong>
                        {f'<span style="color: #a0a0c0; margin-left: 0.5rem;">to {transaction["recipient_username"]}</span>' if transaction.get('recipient_username') else ''}
                        {f'<span style="color: #a0a0c0; margin-left: 0.5rem;">from {transaction["source"]}</span>' if transaction.get('source') else ''}
                    </div>
                    <div style="color: #a0a0c0; font-size: 0.875rem;">
                        {transaction.get('description', 'No description')}
                    </div>
                    <div style="color: #6e6e8f; font-size: 0.75rem; margin-top: 0.25rem;">
                        {formatted_date}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="color: {amount_color}; font-weight: 700; font-size: 1.1rem;">
                        ${transaction['amount']:,.2f}
                    </div>
                    <div style="color: #6e6e8f; font-size: 0.75rem;">
                        Balance: ${transaction.get('balance_after', 0):,.2f}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_quick_actions():
    """Display quick action buttons"""
    col1, col2, col3, col4 = st.columns(4)
    
    actions = []
    
    with col1:
        if st.button("💰 Add Money", use_container_width=True, key="quick_add"):
            actions.append("add_money")
    
    with col2:
        if st.button("💸 Send Money", use_container_width=True, key="quick_send"):
            actions.append("send_money")
    
    with col3:
        if st.button("📜 History", use_container_width=True, key="quick_history"):
            actions.append("history")
    
    with col4:
        if st.button("📊 Analytics", use_container_width=True, key="quick_analytics"):
            actions.append("analytics")
    
    return actions

def create_spending_chart(transactions):
    """Create a beautiful spending chart"""
    if not transactions:
        return None
    
    # Prepare data
    df_data = []
    for t in transactions:
        date_obj = datetime.fromisoformat(t['created_at'])
        df_data.append({
            'Date': date_obj.date(),
            'Amount': t['amount'] if t['type'] == 'CREDIT' else -t['amount'],
            'Type': t['type'],
            'Description': t.get('description', 'No description')
        })
    
    df = pd.DataFrame(df_data)
    
    # Create chart
    fig = go.Figure()
    
    # Add credit transactions
    credit_data = df[df['Type'] == 'CREDIT']
    if not credit_data.empty:
        fig.add_trace(go.Scatter(
            x=credit_data['Date'],
            y=credit_data['Amount'],
            mode='markers+lines',
            name='Income',
            line=dict(color='#00d4aa', width=3),
            marker=dict(size=8, color='#00d4aa')
        ))
    
    # Add debit transactions
    debit_data = df[df['Type'] == 'DEBIT']
    if not debit_data.empty:
        fig.add_trace(go.Scatter(
            x=debit_data['Date'],
            y=debit_data['Amount'],
            mode='markers+lines',
            name='Expenses',
            line=dict(color='#ff6b9d', width=3),
            marker=dict(size=8, color='#ff6b9d')
        ))
    
    # Update layout
    fig.update_layout(
        title="Transaction Flow",
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        )
    )
    
    return fig

def create_balance_trend_chart(transactions):
    """Create balance trend chart"""
    if not transactions:
        return None
    
    # Sort transactions by date
    sorted_transactions = sorted(transactions, key=lambda x: x['created_at'])
    
    dates = []
    balances = []
    
    for t in sorted_transactions:
        dates.append(datetime.fromisoformat(t['created_at']))
        balances.append(t.get('balance_after', 0))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=balances,
        mode='lines+markers',
        name='Balance',
        line=dict(
            color='#667eea',
            width=3,
            shape='spline'
        ),
        marker=dict(size=6, color='#667eea'),
        fill='tonexty',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    fig.update_layout(
        title="Balance Trend",
        xaxis_title="Date",
        yaxis_title="Balance ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)'
        )
    )
    
    return fig

def create_category_pie_chart(transactions):
    """Create spending by category pie chart"""
    if not transactions:
        return None
    
    # Group by source/recipient for categories
    categories = {}
    for t in transactions:
        if t['type'] == 'DEBIT':
            category = t.get('recipient_username', 'Transfer')
            categories[category] = categories.get(category, 0) + t['amount']
    
    if not categories:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=list(categories.keys()),
        values=list(categories.values()),
        hole=0.4,
        marker=dict(
            colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
            line=dict(color='#1a1a2e', width=2)
        )
    )])
    
    fig.update_layout(
        title="Spending by Category",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255,255,255,0.1)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1
        )
    )
    
    return fig

def show_loading_skeleton():
    """Display loading skeleton animation"""
    st.markdown("""
        <div style="padding: 2rem;">
            <div class="skeleton" style="height: 60px; margin-bottom: 1rem;"></div>
            <div class="skeleton" style="height: 40px; margin-bottom: 1rem;"></div>
            <div class="skeleton" style="height: 40px; margin-bottom: 1rem;"></div>
            <div class="skeleton" style="height: 30px; width: 60%;"></div>
        </div>
    """, unsafe_allow_html=True)

def show_success_animation():
    """Display success animation"""
    st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <div style="font-size: 4rem; animation: pulse 1s infinite;">✅</div>
            <h3 style="color: #00d4aa; margin-top: 1rem;">Success!</h3>
        </div>
    """, unsafe_allow_html=True)

def show_welcome_message(username, last_login=None):
    """Display welcome message with user info"""
    last_login_text = ""
    if last_login:
        try:
            login_time = datetime.fromisoformat(last_login)
            last_login_text = f"Last login: {login_time.strftime('%b %d, %Y at %I:%M %p')}"
        except:
            last_login_text = f"Last login: {last_login}"
    
    st.markdown(f"""
        <div class="fade-in" style="margin-bottom: 2rem;">
            <h1 style="color: white; margin-bottom: 0.5rem;">
                Welcome back, {username}! 👋
            </h1>
            <p style="color: #a0a0c0; margin-top: 0.5rem;">
                {last_login_text} • <span class="badge badge-success">Verified</span>
            </p>
        </div>
    """, unsafe_allow_html=True)