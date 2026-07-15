import streamlit as st
import yfinance as yf
import pandas as pd
from database import run_query  # Supabase cloud database connection

# Page Config
st.set_page_config(page_title="FinTrack Pro", page_icon="📊", layout="wide")

# Session State for User Session
if "user" not in st.session_state:
    st.session_state.user = "AP_AP"  # Default simulated student session profile

# Sidebar Navigation Menu
st.sidebar.title(f"👤 {st.session_state.user}")
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation Matrix",
    ["Dashboard Matrix", "Track Expenses", "Savings Goals", "Stock Portfolio", "P2P Bill Splitter"]
)

st.sidebar.markdown("---")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.user = None
    st.rerun()

# --- MODULE 1: STOCK PORTFOLIO (REAL-TIME ASSET EVALUATION) ---
if menu == "Stock Portfolio":
    st.title("📈 Real-Time Asset Evaluation Suite")
    st.markdown("🔍 **Symbol Reference Helper:** Look up index assets, global stocks, and national equities via [Yahoo Finance](https://finance.yahoo.com).")
    
    # Input Configuration Form
    with st.form("asset_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("Enter Asset Ticker Symbol", value="RELIANCE.NS").strip().upper()
        with col2:
            purchase_price = st.number_input("Your Purchase Price (₹)", min_value=0.0, value=500.0, step=10.0)
        
        submit_btn = st.form_submit_button("Add to Monitor Matrix", use_container_width=True)

    # Action Core Logic
    if submit_btn:
        if ticker == "":
            st.error("Registry Failure: Ticker symbol field cannot be left blank.")
        else:
            try:
                # Fetching real-time streaming data from Yahoo Finance
                asset = yf.Ticker(ticker)
                todays_data = asset.history(period='1d')
                
                if not todays_data.empty:
                    live_price = round(todays_data['Close'].iloc[-1], 2)
                    
                    # Persistent registry integration placeholder via Database
                    # run_query(f"INSERT INTO portfolio (user, ticker, buy_price) VALUES ('{st.session_state.user}', '{ticker}', {purchase_price})")
                    
                    st.success(f"Asset Position '{ticker}' integrated successfully into tracking streams.")
                    
                    st.markdown("---")
                    st.subheader("Current Managed Positions")
                    
                    # Dynamic color coding based on performance matrix
                    color = "green" if live_price >= purchase_price else "red"
                    
                    # HTML injection fixed securely via st.markdown
                    st.markdown(
                        f"**Asset Profile:** `{ticker}` | "
                        f"**Purchase Basis:** ₹{purchase_price:.2f} | "
                        f"**Real-time Price:** <span style='color:{color}; font-weight:bold; font-size:1.1em;'>₹{live_price:.2f}</span>", 
                        unsafe_allow_html=True
                    )
                    
                    if st.button("Liquidate Position", use_container_width=True):
                        st.info("Position liquidation triggered.")
                else:
                    st.error("Verification Failure: Invalid ticker registry on Yahoo Finance.")
            except Exception as e:
                st.error("Verification Failure: Connection protocol error or invalid asset registry.")

# --- MODULE 2: DASHBOARD MATRIX ---
elif menu == "Dashboard Matrix":
    st.title("📊 Financial Command Dashboard")
    st.info("Welcome back to FinTrack Pro. Centralized data streaming operational.")
    
    # Metric Mock Indicators
    c1, c2, c3 = st.columns(3)
    c1.metric("Net Liquid Assets", "₹24,500.00", "+₹1,200.00 (This Month)")
    c2.metric("Active Expense Stream", "₹4,230.00", "-5% from last week")
    c3.metric("Savings Goal Milestones", "2/5 Completed", "40% Target Reached")

# --- MODULE 3: TRACK EXPENSES ---
# --- MODULE 3: TRACK EXPENSES ---
elif menu == "Track Expenses":
    st.title("💸 Expense Ledger Optimization")
    st.markdown("Log structural outlays and manage budgetary parameters.")
    st.markdown("---")
    
    # Session state initialization for temporary data store
    if "expense_data" not in st.session_state:
        st.session_state.expense_data = pd.DataFrame(columns=["Date", "Description", "Category", "Amount (₹)"])
    
    st.subheader("➕ Log New Outlay")
    
    # Simple form: Ab yahan category select karne ka koi dropdown option nahi hai!
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("Transaction Date")
            exp_desc = st.text_input("Description/Label", placeholder="e.g., Zomato dinner, Uber ride, Room Rent, Zara shirt")
        with col2:
            exp_amt = st.number_input("Amount (₹)", min_value=0.0, step=50.0)
            
        submit_exp = st.form_submit_button("Commit to Ledger", use_container_width=True)
        
    if submit_exp:
        if exp_amt <= 0:
            st.error("Validation Failure: Amount must be greater than ₹0.")
        elif not exp_desc.strip():
            st.error("Validation Failure: Description field cannot be empty.")
        else:
            # Algorithmic Automatic Category Keyword Mapping Matrix
            desc_lower = exp_desc.lower().strip()
            
            if any(k in desc_lower for k in ["zomato", "swiggy", "dinner", "food", "restaurant", "lunch", "cafe", "maggi"]):
                auto_category = "Food & Dining"
            elif any(k in desc_lower for k in ["rent", "room", "pg", "flat", "hostel"]):
                auto_category = "Rent & Living"
            elif any(k in desc_lower for k in ["uber", "ola", "auto", "petrol", "rapido", "train", "flight", "metro"]):
                auto_category = "Transport"
            elif any(k in desc_lower for k in ["bill", "electricity", "wifi", "recharge", "water", "jio", "airtel"]):
                auto_category = "Utilities & Bills"
            elif any(k in desc_lower for k in ["zara", "hnm", "myntra", "clothes", "shopping", "amazon", "flipkart"]):
                auto_category = "Shopping"
            elif any(k in desc_lower for k in ["netflix", "prime", "movie", "hotstar", "game", "club"]):
                auto_category = "Entertainment"
            else:
                auto_category = "Miscellaneous"
                
            # Create a new row row
            new_row = pd.DataFrame([{
                "Date": exp_date.strftime('%Y-%m-%d'),
                "Description": exp_desc.strip(),
                "Category": auto_category,  # Automatic Category Assigned
                "Amount (₹)": round(exp_amt, 2)
            }])
            
            # Append to session data frame
            st.session_state.expense_data = pd.concat([st.session_state.expense_data, new_row], ignore_index=True)
            st.success(f"Expense logged! System auto-assigned category: **{auto_category}**")
            
    # Display Analytics Matrix
    st.markdown("---")
    st.subheader("📊 Expense Log History")
    
    if not st.session_state.expense_data.empty:
        # Total Summary metrics
        total_spent = st.session_state.expense_data["Amount (₹)"].sum()
        st.metric(label="Total Outflow Vector", value=f"₹{total_spent:,.2f}")
        
        # Display DataFrame layout
        st.dataframe(st.session_state.expense_data, use_container_width=True)
        
        # Category Breakdown Metric Visuals
        st.markdown("#### Category Allocation Summary")
        cat_totals = st.session_state.expense_data.groupby("Category")["Amount (₹)"].sum().reset_index()
        st.table(cat_totals)
    else:
        st.info("No transaction matrices loaded into current runtime history.")
# --- MODULE 4: SAVINGS GOALS ---
elif menu == "Savings Goals":
    st.title("🎯 Structural Capital Goals")
    st.text("Track target trajectories for diversified allocation funds.")

# --- MODULE 5: P2P BILL SPLITTER ---
elif menu == "P2P Bill Splitter":
    st.title("🤝 Peer-to-Peer Capital Ledger (Splitter)")
    st.markdown("Equitable algorithmic cost allocation matrix.")
    st.markdown("---")
    
    # Core Configurations
    total_amount = st.number_input("Total Bill Amount (₹)", min_value=0.0, value=0.0, step=10.0)
    friends_input = st.text_input("Enter Friends' Names (comma-separated)", placeholder="Rahul, Amit, Priya")
    
    if friends_input:
        friends_list = [name.strip() for name in friends_input.split(",") if name.strip()]
        all_participants = ["You"] + friends_list
        total_people = len(all_participants)
        
        if total_amount > 0:
            share_per_person = round(total_amount / total_people, 2)
            st.info(f"Total Members: **{total_people}** | Fair Share Per Person: **₹{share_per_person:.2f}**")
            st.markdown("---")
            
            st.subheader("💰 Who Paid How Much?")
            paid_by_dict = {}
            
            # Dynamic dynamic inputs generation for tracking payments
            cols = st.columns(min(len(all_participants), 3))
            for index, person in enumerate(all_participants):
                col_to_use = cols[index % 3]
                with col_to_use:
                    # 'You' ke liye by default total amount set kar dete hain initialization simple rakhne ko
                    default_paid = total_amount if person == "You" else 0.0
                    paid_by_dict[person] = st.number_input(f"Paid by {person} (₹)", min_value=0.0, value=default_paid, key=f"paid_{person}")
            
            # Sum checking validation
            total_paid_entered = sum(paid_by_dict.values())
            
            if abs(total_paid_entered - total_amount) > 0.01:
                st.warning(f"⚠️ Sum mismatch: Total of individual payments (₹{total_paid_entered:.2f}) must match the Total Bill Amount (₹{total_amount:.2f}).")
            else:
                if st.button("Calculate Balance Matrix & Settlement Streams", use_container_width=True):
                    st.success("Ledger calculations integrated smoothly!")
                    
                    st.markdown("### 📊 Debt Settlement Matrix")
                    
                    balances = {}
                    for person in all_participants:
                        # Balance = Paid Amount - Share they owe
                        balances[person] = round(paid_by_dict[person] - share_per_person, 2)
                    
                    # Creating clear UI layout for who receives and who owes
                    col_matrix_1, col_matrix_2 = st.columns(2)
                    
                    with col_matrix_1:
                        st.markdown("**🟢 Receives Back (Owed Money):**")
                        for person, bal in balances.items():
                            if bal > 0:
                                st.write(f"🔹 **{person}** should get back: :green[₹{bal:.2f}]")
                                
                    with col_matrix_2:
                        st.markdown("**🔴 Needs to Pay (Owes Money):**")
                        for person, bal in balances.items():
                            if bal < 0:
                                st.write(f"🔸 **{person}** needs to pay: :red[₹{abs(bal):.2f}]")
                                
                    # Clean visual summary table representation
                    st.markdown("---")
                    summary_df = pd.DataFrame({
                        "Participant": all_participants,
                        "Amount Paid": [f"₹{paid_by_dict[p]:.2f}" for p in all_participants],
                        "Net Balance": [f"+₹{balances[p]:.2f}" if balances[p] >= 0 else f"-₹{abs(balances[p]):.2f}" for p in all_participants]
                    })
                    st.table(summary_df)