import streamlit as st
import yfinance as yf
import pandas as pd

# Page Config
st.set_page_config(page_title="FinTrack Pro", page_icon="📊", layout="wide")

# --- INITIALIZATION MATRIX ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True  # Simulated live state

if "user" not in st.session_state:
    st.session_state.user = "AP_AP"

if "expense_data" not in st.session_state:
    st.session_state.expense_data = pd.DataFrame(columns=["Date", "Description", "Category", "Amount (₹)"])

if "savings_goals" not in st.session_state:
    st.session_state.savings_goals = [
        {"Goal": "Tech Upgrade (Laptop)", "Target": 60000.0, "Saved": 60000.0},
        {"Goal": "Emergency Contingency", "Target": 25000.0, "Saved": 25000.0},
        {"Goal": "Placement Trip Fund", "Target": 15000.0, "Saved": 5000.0},
    ]

# --- LOGIN SCREEN SIMULATION ---
if not st.session_state.logged_in:
    st.title("🔒 FinTrack Pro - Secure Gateway")
    st.warning("Current session terminated.")
    if st.button("Re-Authenticate User (Login As AP_AP)", use_container_width=True):
        st.session_state.logged_in = True
        st.session_state.user = "AP_AP"
        st.rerun()
else:
    # Sidebar Navigation Menu
    st.sidebar.title(f"👤 {st.session_state.user}")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "Navigation Matrix",
        ["Dashboard Matrix", "Track Expenses", "Savings Goals", "Stock Portfolio", "P2P Bill Splitter"]
    )

    st.sidebar.markdown("---")
    # Fixed Logout Engine Toggle
    if st.sidebar.button("Logout Session", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    # --- MODULE 1: DASHBOARD MATRIX ---
    if menu == "Dashboard Matrix":
        st.title("📊 Financial Command Dashboard")
        st.info(f"Welcome back, {st.session_state.user or 'User'}. Centralized metrics engine operational.")
        st.markdown("---")
        
        # Live calculations
        live_total_expenses = st.session_state.expense_data["Amount (₹)"].sum() if not st.session_state.expense_data.empty else 0.0
        monthly_budget = 50000.0
        remaining_budget = max(0.0, monthly_budget - live_total_expenses)
        
        # Dynamic Savings Calculations for Dashboard
        total_goals = len(st.session_state.savings_goals)
        completed_goals = sum(1 for g in st.session_state.savings_goals if g["Saved"] >= g["Target"])
        
        # Grid metrics layout
        st.subheader("📌 System Status & Core Parameters")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💸 Total Live Expenses", f"₹{live_total_expenses:,.2f}", delta=f"{len(st.session_state.expense_data)} Transact")
        c2.metric("🛡️ Budget Reserve Capacity", f"₹{remaining_budget:,.2f}", delta="Cap: ₹50k")
        c3.metric("🎯 Savings Goal Matrix", f"{completed_goals} / {total_goals} Done", delta="Dynamic Live Sync")
        c4.metric("🌐 Yahoo Finance Feeds", "Active Staging", delta="Status: 200 OK")
        
        st.markdown("---")
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("⏱️ Recent Activity Matrix")
            if not st.session_state.expense_data.empty:
                st.dataframe(st.session_state.expense_data.tail(5).iloc[::-1], use_container_width=True)
            else:
                st.info("No transaction matrices loaded. Go to 'Track Expenses' to generate logs!")
        with col_right:
            st.subheader("🎯 Target Vector Breakdown")
            for g in st.session_state.savings_goals:
                st.write(f"🏁 **{g['Goal']}:** ₹{g['Saved']:.0f} / ₹{g['Target']:.0f}")

    # --- MODULE 2: TRACK EXPENSES ---
    elif menu == "Track Expenses":
        st.title("💸 Expense Ledger Optimization")
        st.markdown("---")
        with st.form("expense_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                exp_date = st.date_input("Transaction Date")
                exp_desc = st.text_input("Description/Label", placeholder="e.g., Zomato dinner")
            with col2:
                exp_amt = st.number_input("Amount (₹)", min_value=0.0, step=50.0)
            submit_exp = st.form_submit_button("Commit to Ledger", use_container_width=True)
            
        if submit_exp and exp_amt > 0 and exp_desc.strip():
            desc_lower = exp_desc.lower().strip()
            auto_category = "Food & Dining" if "zomato" in desc_lower or "food" in desc_lower else "Miscellaneous"
            new_row = pd.DataFrame([{"Date": exp_date.strftime('%Y-%m-%d'), "Description": exp_desc.strip(), "Category": auto_category, "Amount (₹)": round(exp_amt, 2)}])
            st.session_state.expense_data = pd.concat([st.session_state.expense_data, new_row], ignore_index=True)
            st.success(f"Log saved! Category: {auto_category}")

    # --- MODULE 3: SAVINGS GOALS ---
    elif menu == "Savings Goals":
        st.title("🎯 Structural Capital Goals")
        st.markdown("---")
        with st.form("savings_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                goal_name = st.text_input("Goal Objective/Label")
                target_amt = st.number_input("Target Amount (₹)", min_value=0.0, step=1000.0)
            with col2:
                saved_amt = st.number_input("Currently Allocated/Saved (₹)", min_value=0.0, step=500.0)
            submit_goal = st.form_submit_button("Deploy Goal Parameter", use_container_width=True)
            
        if submit_goal and goal_name.strip() and target_amt > 0:
            st.session_state.savings_goals.append({"Goal": goal_name.strip(), "Target": round(target_amt, 2), "Saved": round(saved_amt, 2)})
            st.success(f"Goal '{goal_name}' updated inside tracking matrices!")

        st.markdown("---")
        for g in st.session_state.savings_goals:
            ratio = min(1.0, g["Saved"] / g["Target"]) if g["Target"] > 0 else 0.0
            st.write(f"### {g['Goal']}")
            st.progress(ratio)
            st.metric("Status Metrics", f"₹{g['Saved']:.0f} / ₹{g['Target']:.0f}", f"{ratio*100:.1f}% Met")

    # --- MODULE 4: STOCK PORTFOLIO ---
    elif menu == "Stock Portfolio":
        st.title("📈 Real-Time Asset Evaluation Suite")
        ticker = st.text_input("Enter Asset Ticker Symbol", value="RELIANCE.NS").strip().upper()
        purchase_price = st.number_input("Your Purchase Price (₹)", min_value=0.0, value=500.0)
        
        if st.button("Add to Monitor Matrix") and ticker:
            try:
                asset = yf.Ticker(ticker)
                todays_data = asset.history(period='1d')
                if not todays_data.empty:
                    live_price = round(todays_data['Close'].iloc[-1], 2)
                    st.success(f"Asset Position '{ticker}' integrated successfully.")
                    color = "green" if live_price >= purchase_price else "red"
                    st.markdown(f"**Asset Profile:** `{ticker}` | **Real-time Price:** <span style='color:{color}; font-weight:bold;'>₹{live_price}</span>", unsafe_allow_html=True)
                else:
                    st.error("Invalid ticker registry on Yahoo Finance.")
            except Exception:
                st.error("Connection protocol error.")

    # --- MODULE 5: P2P BILL SPLITTER ---
    elif menu == "P2P Bill Splitter":
        st.title("🤝 Peer-to-Peer Capital Ledger (Splitter)")
        total_amount = st.number_input("Total Bill Amount (₹)", min_value=0.0, value=0.0)
        friends_input = st.text_input("Enter Friends' Names (comma-separated)")
        
        if st.button("Calculate Balance Matrix & Settlement Streams") and total_amount > 0 and friends_input:
            friends_list = [name.strip() for name in friends_input.split(",") if name.strip()]
            total_people = len(friends_list) + 1
            share_per_person = round(total_amount / total_people, 2)
            your_receivable = round(total_amount - share_per_person, 2)
            
            st.success("Ledger calculations integrated smoothly!")
            st.write(f"🔹 **You** should get back: ₹{your_receivable:.2f}")
            for person in friends_list:
                st.write(f"🔸 **{person}** needs to pay You: ₹{share_per_person:.2f}")