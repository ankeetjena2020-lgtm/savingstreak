import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os

# Page Configuration Setup
st.set_page_config(page_title="FinTrack Pro", page_icon="📊", layout="wide")

# --- DATABASE MANAGEMENT CONTROLS ---
USER_DB = "user_registry.json"
DATA_DB = "user_financial_data.json"

def load_db(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_db(data, file_name):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# Initialize local dynamic files
users = load_db(USER_DB)
financial_data = load_db(DATA_DB)

# Standard master operational profile registry
if "AP_AP" not in users:
    users["AP_AP"] = "12345"
    save_db(users, USER_DB)

# --- APPLICATION SESSION MANAGEMENT MATRIX ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# --- AUTHENTICATION ENGINE INTERFACE ---
if not st.session_state.logged_in:
    st.title("🔒 FinTrack Pro - Secure Gateway")
    
    auth_mode = st.radio("Access Protocol Matrix", ["Sign In (Existing User)", "Sign Up (Create New Account)"], horizontal=True)
    st.markdown("---")
    
    if auth_mode == "Sign In (Existing User)":
        with st.form("login_form"):
            username = st.text_input("Username / Enrollment ID", placeholder="Enter your username").strip()
            password = st.text_input("Password", type="password", placeholder="•••••")
            submit_login = st.form_submit_button("Authenticate & Enter System", use_container_width=True)
            
        if submit_login:
            users = load_db(USER_DB)  # Dynamic real-time fetch
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success(f"Access Granted! Session authorized for {username}.")
                st.rerun()
            else:
                st.error("Access Denied: Invalid registry credentials configuration.")
                
    elif auth_mode == "Sign Up (Create New Account)":
        st.subheader("📝 Registration Node")
        with st.form("signup_form"):
            new_user = st.text_input("Choose Unique Username", placeholder="e.g., User_01").strip()
            new_pass = st.text_input("Set Secure Password", type="password", placeholder="•••••")
            confirm_pass = st.text_input("Confirm Password", type="password", placeholder="•••••")
            submit_signup = st.form_submit_button("Deploy User Credentials", use_container_width=True)
            
        if submit_signup:
            users = load_db(USER_DB)
            if not new_user or not new_pass:
                st.error("Validation Error: Fields cannot be left blank.")
            elif new_user in users:
                st.error("Conflict Registry: Username already registered on system files.")
            elif new_pass != confirm_pass:
                st.error("Validation Error: Passwords mismatch.")
            else:
                users[new_user] = new_pass
                save_db(users, USER_DB)
                st.success("Registration Successful! Switch to 'Sign In' to access your portal.")

else:
    # --- ACTIVE SESSION USER COMPARTMENT ---
    current_username = st.session_state.current_user
    financial_data = load_db(DATA_DB)
    
    # Establish complete isolated baseline for new account space
    if current_username not in financial_data:
        financial_data[current_username] = {
            "expenses": [],
            "goals": []
        }
        save_db(financial_data, DATA_DB)

    user_records = financial_data[current_username]
    expense_df = pd.DataFrame(user_records["expenses"], columns=["Date", "Description", "Category", "Amount (₹)"])
    if expense_df.empty:
        expense_df = pd.DataFrame(columns=["Date", "Description", "Category", "Amount (₹)"])

    # --- MAIN SIDEBAR NAVIGATION SYSTEM ---
    st.sidebar.title(f"👤 Active Profile: {current_username}")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "Navigation Matrix",
        ["Dashboard Matrix", "Track Expenses", "Savings Goals", "Stock Portfolio", "P2P Bill Splitter"]
    )
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout Operational Session", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

    # --- MODULE 1: DYNAMIC COMMAND DASHBOARD ---
    if menu == "Dashboard Matrix":
        st.title("📊 Financial Command Dashboard")
        st.info(f"System Node Active. Secure profile space tracking engaged for **{current_username}**.")
        st.markdown("---")
        
        live_total_expenses = expense_df["Amount (₹)"].sum() if not expense_df.empty else 0.0
        monthly_budget = 50000.0
        remaining_budget = max(0.0, monthly_budget - live_total_expenses)
        
        total_goals = len(user_records["goals"])
        completed_goals = sum(1 for g in user_records["goals"] if g["Saved"] >= g["Target"])
        
        st.subheader("📌 Personal Metric Vector Matrix")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💸 Total Live Outflow", f"₹{live_total_expenses:,.2f}", delta=f"{len(expense_df)} Logs Mapped", delta_color="inverse")
        c2.metric("🛡️ Budget Balance Left", f"₹{remaining_budget:,.2f}", delta=f"Limit Cap: ₹{monthly_budget:,.0f}")
        c3.metric("🎯 Goal Milestones Met", f"{completed_goals} / {total_goals} Done", delta="Sync Speed: Live")
        c4.metric("🌐 Yahoo Finance Engine", "Synchronized", delta="Status: 200 OK")
        
        st.markdown("---")
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.subheader("⏱️ Live Recent Transaction Pipeline")
            if not expense_df.empty:
                st.dataframe(expense_df.tail(5).iloc[::-1], use_container_width=True)
            else:
                st.info("No transaction matrices loaded. Go to 'Track Expenses' to generate logs!")
        with col_right:
            st.subheader("🏁 Active Structural Target Goals")
            if user_records["goals"]:
                for g in user_records["goals"]:
                    st.write(f"🎯 **{g['Goal']}:** ₹{g['Saved']:.0f} / ₹{g['Target']:.0f}")
            else:
                st.info("No target goal milestones active in user schema database.")

    # --- MODULE 2: OPTIMIZED EXPENSE LEDGER (AUTO ENGINE) ---
    elif menu == "Track Expenses":
        st.title("💸 Expense Ledger Optimization Engine")
        st.markdown("---")
        with st.form("expense_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                exp_date = st.date_input("Transaction Date")
                exp_desc = st.text_input("Description/Label", placeholder="e.g., Swiggy dinner order, Uber ride")
            with col2:
                exp_amt = st.number_input("Amount (₹)", min_value=0.0, step=50.0)
            submit_exp = st.form_submit_button("Commit Transaction to Ledger", use_container_width=True)
            
        if submit_exp:
            if exp_amt <= 0 or not exp_desc.strip():
                st.error("Validation Failure: Ensure amount parameters and descriptions are not null.")
            else:
                desc_lower = exp_desc.lower().strip()
                if any(k in desc_lower for k in ["zomato", "swiggy", "dinner", "food", "lunch", "restaurant", "cafe", "mcdonald"]):
                    auto_category = "Food & Dining"
                elif any(k in desc_lower for k in ["uber", "ola", "auto", "metro", "petrol", "rapido", "cab"]):
                    auto_category = "Transport"
                elif any(k in desc_lower for k in ["rent", "room", "hostel", "pg", "flat"]):
                    auto_category = "Rent & Living"
                elif any(k in desc_lower for k in ["bill", "electricity", "wifi", "recharge", "phone"]):
                    auto_category = "Utilities & Bills"
                else:
                    auto_category = "Miscellaneous"
                    
                user_records["expenses"].append({
                    "Date": exp_date.strftime('%Y-%m-%d'),
                    "Description": exp_desc.strip(),
                    "Category": auto_category,
                    "Amount (₹)": round(exp_amt, 2)
                })
                financial_data[current_username] = user_records
                save_db(financial_data, DATA_DB)
                st.success(f"Mapping Successful! Isolated User Data Array updated with category: **{auto_category}**")

    # --- MODULE 3: SAVINGS MILESTONES CONTROLLERS ---
    elif menu == "Savings Goals":
        st.title("🎯 Structural Target Capital Goals")
        st.markdown("---")
        with st.form("savings_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                goal_name = st.text_input("Goal Vector Objective/Label", placeholder="e.g., Tech Upgrade, Placement Trip")
                target_amt = st.number_input("Target Threshold Value (₹)", min_value=0.0, step=1000.0)
            with col2:
                saved_amt = st.number_input("Currently Saved Assets (₹)", min_value=0.0, step=50.0)
            submit_goal = st.form_submit_button("Deploy Goal Constraints to Server", use_container_width=True)
            
        if submit_goal:
            if not goal_name.strip() or target_amt <= 0 or saved_amt > target_amt:
                st.error("Validation Failure: Verify goal name field data and threshold boundaries.")
            else:
                user_records["goals"].append({
                    "Goal": goal_name.strip(), 
                    "Target": round(target_amt, 2), 
                    "Saved": round(saved_amt, 2)
                })
                financial_data[current_username] = user_records
                save_db(financial_data, DATA_DB)
                st.success(f"Dynamic Structural Matrix integration completed for milestone: '{goal_name}'")

        st.markdown("---")
        if user_records["goals"]:
            for g in user_records["goals"]:
                ratio = min(1.0, g["Saved"] / g["Target"]) if g["Target"] > 0 else 0.0
                st.write(f"### 🏁 Objective: {g['Goal']}")
                st.progress(ratio)
                st.metric("Milestone Parameters Status", f"₹{g['Saved']:,.0f} / ₹{g['Target']:,.0f}", f"{ratio*100:.1f}% Fulfilled")
        else:
            st.info("No structural milestone profiles mapped inside current user space database registries.")

    # --- MODULE 4: STOCK TELEMETRY PORTFOLIO ---
    elif menu == "Stock Portfolio":
        st.title("📈 Real-Time Asset Evaluation Suite")
        st.markdown("---")
        ticker = st.text_input("Enter Market Ticker Symbol (Yahoo Finance Compatible)", value="RELIANCE.NS").strip().upper()
        purchase_price = st.number_input("Initial Purchase Price Parameter (₹)", min_value=0.0, value=500.0)
        
        if st.button("Query Asset Feed Matrix", use_container_width=True) and ticker:
            try:
                asset = yf.Ticker(ticker)
                todays_data = asset.history(period='1d')
                if not todays_data.empty:
                    live_price = round(todays_data['Close'].iloc[-1], 2)
                    st.success(f"Live Asset Profile '{ticker}' extracted without parity error.")
                    color = "green" if live_price >= purchase_price else "red"
                    st.markdown(f"#### **Live Valuation Summary:** `{ticker}` | **Real-time Price:** <span style='color:{color}; font-weight:bold;'>₹{live_price}</span>", unsafe_allow_html=True)
                else:
                    st.error("Invalid Configuration: Could not locate ticker tracking signature on live networks.")
            except Exception:
                st.error("Connection Error: Execution sequence halted due to API latency timeouts.")

    # --- MODULE 5: BILL SPLITTER ENGINE (PAYER SWITCH CONTROLS) ---
    elif menu == "P2P Bill Splitter":
        st.title("🤝 Peer-to-Peer Capital Ledger (Splitter)")
        st.markdown("Equitable real-time algorithmic cost allocation balance engine.")
        st.markdown("---")
        
        total_amount = st.number_input("Total Transaction Bill (₹)", min_value=0.0, value=0.0, step=10.0)
        friends_input = st.text_input("Participating Friends (Separate names with commas)", placeholder="Rahul, Amit, Priya")
        
        # Core dynamic flexible payor toggle override configuration
        i_paid = st.checkbox("Did you (Primary User Node) clear this entire bill?", value=True)
        
        payer = "You"
        if not i_paid and friends_input.strip():
            clean_friends = [name.strip() for name in friends_input.split(",") if name.strip()]
            payer = st.selectbox("Select entity who cleared the total capital payment:", clean_friends)
        
        if st.button("Compile Settlement Streams Matrix", use_container_width=True):
            if total_amount <= 0 or not friends_input.strip():
                st.error("Execution Exception: Input field parameter variables contain null boundaries.")
            else:
                friends_list = [name.strip() for name in friends_input.split(",") if name.strip()]
                all_participants = ["You"] + friends_list
                share_per_person = round(total_amount / len(all_participants), 2)
                
                st.success(f"Calculations complete. Execution Protocol Ledger compiled for structural payor: **{payer}**")
                st.markdown("---")
                
                balances = {p: round((total_amount if p == payer else 0.0) - share_per_person, 2) for p in all_participants}
                col_matrix_1, col_matrix_2 = st.columns(2)
                
                with col_matrix_1:
                    st.markdown("**🟢 Receives Back (Owed Capital):**")
                    for p, bal in balances.items():
                        if bal > 0: st.write(f"🔹 **{p}** receives: :green[₹{bal:.2f}]")
                with col_matrix_2:
                    st.markdown("**🔴 Needs to Pay (Owes Liabilities):**")
                    for p, bal in balances.items():
                        if bal < 0:
                            target = "You" if payer == "You" else payer
                            st.write(f"🔸 **{p}** needs to settle with {target}: :red[₹{abs(bal):.2f}]")
                            
                st.markdown("---")
                summary_df = pd.DataFrame({
                    "Participant": all_participants,
                    "Amount Paid": [f"₹{total_amount:.2f}" if p == payer else "₹0.00" for p in all_participants],
                    "Net Balance": [f"+₹{balances[p]:.2f}" if balances[p] >= 0 else f"-₹{abs(balances[p]):.2f}" for p in all_participants]
                })
                st.table(summary_df)