import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from database import run_query

# Page config - Sidebar locked to expanded state
st.set_page_config(page_title="FinTrack Pro", page_icon="💳", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for modern UI, fixed sidebar, and COMPACT SLIM login container
st.markdown("""
<style>
    /* Persistent Sidebar adjustments */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        padding-top: 20px;
        min-width: 270px !important;
        max-width: 270px !important;
    }
    
    /* Sleek, Slim Centered Login Card - FIXED WIDTH FOR PERFECT COMPACT LOOK */
    .login-box {
        background-color: #1E293B;
        padding: 30px 25px;
        border-radius: 12px;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.3);
        color: white;
        max-width: 360px;
        margin: 0 auto;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    .inc-dec-btn {
        margin-top: 28px;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if "menu" not in st.session_state:
    st.session_state.menu = "📊 Dashboard Matrix"

# --- SMART MONEY FIELD COMPONENT WITH + / - UI BUTTONS ---
def smart_money_input(label, key_prefix, default_val=0.0):
    state_key = f"{key_prefix}_val"
    if state_key not in st.session_state:
        st.session_state[state_key] = float(default_val)
        
    col_input, col_dec, col_inc = st.columns([6, 1, 1])
    
    with col_input:
        val = st.number_input(label, value=st.session_state[state_key], step=1.0, key=f"{key_prefix}_raw")
        st.session_state[state_key] = val
        
    with col_dec:
        st.markdown("<div class='inc-dec-btn'></div>", unsafe_allow_html=True)
        if st.button("➖", key=f"{key_prefix}_minus"):
            st.session_state[state_key] = max(0.0, st.session_state[state_key] - 100.0)
            st.rerun()
            
    with col_inc:
        st.markdown("<div class='inc-dec-btn'></div>", unsafe_allow_html=True)
        if st.button("➕", key=f"{key_prefix}_plus"):
            st.session_state[state_key] = st.session_state[state_key] + 100.0
            st.rerun()
            
    return st.session_state[state_key]

# --- APP FLOW ---
if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Using center column to hold the slim login box perfectly
    _, center_col, _ = st.columns([1.5, 1.2, 1.5])
    
    with center_col:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-top:0; font-size: 24px;'>🔐 FinTrack Pro</h2>", unsafe_allow_html=True)
        
        action = st.radio("Choose Action", ["Login", "Register"], horizontal=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        u = st.text_input("Username", key="auth_user")
        p = st.text_input("PIN / Password", type="password", key="auth_pass")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if action == "Login":
            if st.button("Proceed & Login"):
                res = run_query("SELECT * FROM users WHERE username=? AND password=?", (u, p), "one")
                if res:
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success(f"Verified! Welcome back.")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        else:
            if st.button("Proceed & Register"):
                if u and p:
                    try:
                        run_query("INSERT INTO users VALUES (?, ?)", (u, p))
                        st.success("Success! Go to Login now.")
                    except:
                        st.error("Username already taken.")
                else:
                    st.error("Fields cannot be blank.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- PERMANENT SIDEBAR NAVIGATION (NO AUTO-HIDE) ---
    with st.sidebar:
        st.markdown(f"<h3 style='color: white; text-align: center;'>👤 {st.session_state.username}</h3>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        menu_options = [
            "📊 Dashboard Matrix",
            "💸 Track Expenses",
            "🎯 Savings Goals",
            "📈 Stock Portfolio",
            "🤝 P2P Bill Splitter"
        ]
        
        for name in menu_options:
            if st.button(name, use_container_width=True):
                st.session_state.menu = name
                st.rerun()
                
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # --- PAGES ---
    user = st.session_state.username

    # 1. DASHBOARD MATRIX
    if st.session_state.menu == "📊 Dashboard Matrix":
        st.title(f"📊 {user}'s Live Matrix Dashboard")
        st.markdown("Your financial ecosystem summarized in one screen.")
        
        expenses = run_query("SELECT type, category, description, amount, date FROM expenses WHERE username=?", (user,), "all")
        goals = run_query("SELECT goal_name, target_amount, current_amount FROM savings WHERE username=?", (user,), "all")
        stocks = run_query("SELECT ticker, buy_price FROM stocks WHERE username=?", (user,), "all")
        p2p_active = run_query("SELECT friend_name, description, amount FROM p2p WHERE username=? AND is_split != 'Settled'", (user,), "all")
        
        df_exp = pd.DataFrame(expenses, columns=['Type', 'Category', 'Description', 'Amount', 'Date'])
        total_inc = df_exp[df_exp['Type'] == 'Income']['Amount'].sum() if not df_exp.empty else 0.0
        total_exp = df_exp[df_exp['Type'] == 'Expense']['Amount'].sum() if not df_exp.empty else 0.0
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Income", f"₹{total_inc:,.2f}")
        c2.metric("Total Expenses", f"₹{total_exp:,.2f}")
        c3.metric("Active Savings Goals", len(goals))
        c4.metric("Tracked Stock Positions", len(stocks))
        
        st.markdown("---")
        
        m1, m2 = st.columns(2)
        with m1:
            st.subheader("📝 Recent Transactions Breakdown")
            if expenses:
                st.dataframe(df_exp.tail(5), use_container_width=True)
            else:
                st.info("No expense entries tracked yet.")
                
            st.subheader("🤝 P2P Active Pending Dues")
            if p2p_active:
                df_p2p = pd.DataFrame(p2p_active, columns=['Friend Name', 'Context / Description', 'Amount Due'])
                st.dataframe(df_p2p, use_container_width=True)
            else:
                st.info("No active pending splits found.")

        with m2:
            st.subheader("🎯 Savings Target Milestones")
            if goals:
                for g_name, target, current in goals:
                    pct = min(1.0, current / target) if target > 0 else 0.0
                    st.write(f"**{g_name}** ({current} / {target})")
                    st.progress(pct)
            else:
                st.info("No active saving milestones configured.")
                
            st.subheader("📈 Real-time Stock Trackers")
            if stocks:
                for ticker, b_price in stocks:
                    try:
                        t_data = yf.Ticker(ticker)
                        c_price = t_data.history(period="1d")['Close'].iloc[-1]
                        currency_label = "$" if t_data.info.get('currency') == "USD" else "₹"
                    except:
                        c_price = b_price
                        currency_label = "₹"
                    st.write(f"**{ticker}** ➡️ Buy: {currency_label}{b_price} | Live: {currency_label}{c_price:.2f}")
            else:
                st.info("No assets added to stock tracking engines.")

    # 2. TRACK EXPENSES (DYNAMIC FIX INTEGRATED)
    elif st.session_state.menu == "💸 Track Expenses":
        st.title("💸 Global Expense Logger")
        
        # Radio toggle with key to enforce state changes
        t_type = st.radio("Transaction Type", ["Expense", "Income"], horizontal=True, key="transaction_type_toggle")
        
        # Dynamic Placeholders based on choice
        if t_type == "Expense":
            cat_placeholder = "e.g., Food, Travel, Medical, Subscriptions"
            desc_placeholder = "e.g., Zomato Dinner, Uber Ride, Netflix"
        else:
            cat_placeholder = "e.g., Salary, Stipend, Freelance, Pocket Money"
            desc_placeholder = "e.g., Monthly Salary, Project Advance, Cash from Dad"
            
        # Using suffix key mapping to split state instantly on click
        cat = st.text_input(f"Category * (Mandatory - {cat_placeholder})", key=f"cat_{t_type}").strip()
        desc = st.text_input(f"Specific Description * (Mandatory - {desc_placeholder})", key=f"desc_{t_type}").strip()
        amt = smart_money_input("Amount", f"amt_{t_type}")
        
        if st.button("Log Transaction"):
            if not cat:
                st.error("🚨 Action Denied: Category field is mandatory.")
            elif not desc:
                st.error("🚨 Action Denied: Description field is mandatory.")
            elif amt <= 0:
                st.error("🚨 Action Denied: Capital amount must be greater than 0.")
            else:
                run_query("INSERT INTO expenses (username, type, category, description, amount, date) VALUES (?, ?, ?, ?, ?, ?)",
                          (user, t_type, cat, desc, amt, str(date.today())))
                st.success(f"Success! {t_type} entry managed under Category: '{cat}'.")
                st.rerun()

    # 3. SAVINGS GOALS
    elif st.session_state.menu == "🎯 Savings Goals":
        st.title("🎯 Goal Progression Room")
        
        with st.form("new_goal_form"):
            st.subheader("Create a New Target Goal")
            g_name = st.text_input("Goal Milestone Name")
            t_amt = st.number_input("Target Amount Required", min_value=0.0, value=0.0, step=100.0)
            if st.form_submit_button("Initiate Goal Milestone"):
                if g_name and t_amt > 0:
                    run_query("INSERT INTO savings (username, goal_name, target_amount, current_amount) VALUES (?, ?, ?, 0.0)", (user, g_name, t_amt))
                    st.success(f"Goal Asset '{g_name}' activated successfully.")
                    st.rerun()
                    
        st.markdown("---")
        st.subheader("Active Goals Matrix")
        goals = run_query("SELECT id, goal_name, target_amount, current_amount FROM savings WHERE username=?", (user,), "all")
        
        if goals:
            for g_id, g_name, target, current in goals:
                col_info, col_action = st.columns([1, 1])
                with col_info:
                    pct = min(1.0, current / target) if target > 0 else 0.0
                    st.markdown(f"### **{g_name}**")
                    st.write(f"Allocation Progress: **₹{current:,.2f}** out of **₹{target:,.2f}**")
                    st.progress(pct)
                with col_action:
                    add_amt = smart_money_input(f"Deposit Capital into '{g_name}'", f"goal_inc_{g_id}")
                    if st.button("Confirm Deposit", key=f"dep_btn_{g_id}"):
                        if add_amt > 0:
                            new_amt = current + add_amt
                            run_query("UPDATE savings SET current_amount=? WHERE id=?", (new_amt, g_id))
                            st.success(f"Allocated ₹{add_amt} towards '{g_name}'.")
                            st.rerun()
                st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        else:
            st.info("No active saving targets found.")

    # 4. STOCK PORTFOLIO
    elif st.session_state.menu == "📈 Stock Portfolio":
        st.title("📈 Real-Time Asset Evaluation Suite")
        st.markdown("> **🔍 Symbol Reference Helper:** Look up index assets, global stocks, and national equities via [Yahoo Finance](https://finance.yahoo.com).")
        
        st_ticker = st.text_input("Enter Asset Ticker Symbol").upper().strip()
        st_buy = smart_money_input("Your Purchase Price", "stock_buy_prc")
        
        if st.button("Add to Monitor Matrix"):
            if st_ticker and st_buy > 0:
                try:
                    tk = yf.Ticker(st_ticker)
                    _ = tk.history(period="1d")
                    run_query("INSERT INTO stocks (username, ticker, buy_price) VALUES (?, ?, ?)", (user, st_ticker, st_buy))
                    st.success(f"Asset Position '{st_ticker}' integrated successfully into tracking streams.")
                    st.rerun()
                except:
                    st.error("Verification Failure: Invalid ticker registry on Yahoo Finance.")
                    
        st.markdown("---")
        st.subheader("Current Managed Positions")
        stocks = run_query("SELECT id, ticker, buy_price FROM stocks WHERE username=?", (user,), "all")
        
        if stocks:
            for s_id, ticker, b_price in stocks:
                try:
                    tk_engine = yf.Ticker(ticker)
                    live_price = tk_engine.history(period="1d")['Close'].iloc[-1]
                    currency = "$" if tk_engine.info.get('currency') == "USD" else "₹"
                except:
                    live_price = b_price
                    currency = "₹"
                net_change = live_price - b_price
                color = "green" if net_change >= 0 else "red"
                
                st.markdown(f"**Asset Profile:** `{ticker}` &nbsp;|&nbsp; **Purchase Basis:** `{currency}{b_price:,.2f}` &nbsp;|&nbsp; **Real-time Price:** `<span style='color:{color}; font-weight:bold;'>{currency}{live_price:,.2f}</span>`", unsafe_allow_html=True)
                if st.button("Liquidate Position", key=f"del_stk_{s_id}"):
                    run_query("DELETE FROM stocks WHERE id=?", (s_id,))
                    st.success(f"Tracked data pipeline dropped for {ticker}.")
                    st.rerun()
        else:
            st.info("No equity tokens or structural indices loaded into monitoring matrices.")

    # 5. P2P BILL SPLITTER
    elif st.session_state.menu == "🤝 P2P Bill Splitter":
        st.title("🤝 Peer-to-Peer Expense Separation")
        
        with st.form("p2p_add_form"):
            st.subheader("Log New Peer-to-Peer Ledger Split")
            fr_name = st.text_input("Debtor / Friend's Identity")
            split_desc = st.text_input("Transaction Context Description")
            raw_amount = st.number_input("Total Shared Ledger Capital", min_value=0.0, step=10.0)
            split_choice = st.radio("Apply 50/50 Split Rule Architecture?", ["Yes - Divide Evenly (50/50)", "No - Charge Full Value to Friend"], horizontal=True)
            
            if st.form_submit_button("Register Debt Entry"):
                if fr_name and split_desc and raw_amount > 0:
                    final_charge = raw_amount / 2 if "Yes" in split_choice else raw_amount
                    is_split_flag = "Yes" if "Yes" in split_choice else "No"
                    run_query("INSERT INTO p2p (username, friend_name, description, amount, is_split) VALUES (?, ?, ?, ?, ?)",
                              (user, fr_name, split_desc, final_charge, is_split_flag))
                    st.success("Transaction successfully structured into active ledgers.")
                    st.rerun()
        
        st.markdown("---")
        
        # Section 1: Active Dues Room
        st.subheader("🔴 Active Pending Dues")
        active_dues = run_query("SELECT id, friend_name, description, amount, is_split FROM p2p WHERE username=? AND is_split != 'Settled'", (user,), "all")
        
        if active_dues:
            for d_id, f_name, d_desc, d_amt, s_flag in active_dues:
                col_txt, col_btn = st.columns([3, 1])
                with col_txt:
                    st.write(f"👉 Account **{f_name}** owes you **₹{d_amt:,.2f}** for context *'{d_desc}'* (Split Type: {s_flag})")
                with col_btn:
                    if st.button("✅ Settle Up", key=f"settle_{d_id}"):
                        run_query("UPDATE p2p SET is_split = 'Settled' WHERE id = ?", (d_id,))
                        st.success(f"Balance cleared for account user: {f_name}.")
                        st.rerun()
        else:
            st.info("All accounts balanced! No active pending dues.")
            
        st.markdown("---")
        
        # Section 2: Permanent Settled History Log
        st.subheader("🟢 Settled History Log (Audit Trail)")
        settled_dues = run_query("SELECT friend_name, description, amount FROM p2p WHERE username=? AND is_split = 'Settled'", (user,), "all")
        if settled_dues:
            df_settled = pd.DataFrame(settled_dues, columns=['Friend Identity', 'Description / Context', 'Amount Received'])
            st.dataframe(df_settled, use_container_width=True)
        else:
            st.text("No archived historical settlements logged yet.")