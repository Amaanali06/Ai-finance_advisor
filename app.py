import streamlit as st
from analyzer import analyze_finances
from llm_helper import get_financial_advice

st.title("💰 AI Finance Advisor")

# =========================
# USER INPUT
# =========================

st.subheader("👤 User Profile")

salary = st.number_input("Monthly Salary", min_value=0)
age = st.number_input("Age", min_value=18, max_value=100)
savings = st.number_input("Current Savings")

# =========================
# DYNAMIC EXPENSES
# =========================

st.subheader("💸 Expenses")

expense_data = {}

num_expenses = st.number_input("Number of expense categories", min_value=1, step=1)

for i in range(int(num_expenses)):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(f"Expense Name {i+1}", key=f"name_{i}")
    with col2:
        value = st.number_input(f"Amount {i+1}", key=f"value_{i}")

    if name:
        expense_data[name] = value

# =========================
# FINANCIAL DETAILS
# =========================

st.subheader("🏦 Financial Details")

loans = st.number_input("Loan EMI (monthly)")
cc_dues = st.number_input("Credit Card Dues")

health_insurance = st.number_input("Health Insurance (yearly)")
term_insurance = st.number_input("Term Insurance (yearly)")

# =========================
# GOALS
# =========================

st.subheader("🎯 Financial Goals")

goal = st.text_area("Your goals (house, car, retirement, etc.)")

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze"):

    # Run rule engine
    result = analyze_finances(salary, expense_data)

    st.subheader("📊 Analysis")
    st.write(f"Total Expenses: ₹{result['total_expense']}")
    st.write(f"Savings: ₹{result['savings']}")

    for insight in result["insights"]:
        st.write(insight)

    # Prepare data for AI
    data = {
        "salary": salary,
        "age": age,
        "expenses": expense_data,
        "savings": savings,
        "loans": loans,
        "cc_dues": cc_dues,
        "health_insurance": health_insurance,
        "term_insurance": term_insurance,
        "goals": goal
    }

    # Store in session (for chat use)
    st.session_state["user_data"] = data

    # Get AI advice
    advice = get_financial_advice(data)

    st.subheader("🤖 AI Advice")
    st.write(advice)

# =========================
# CHAT SECTION
# =========================

st.subheader("💬 Ask Follow-up Questions")

user_query = st.text_input("Ask anything about your finances")

if user_query and "user_data" in st.session_state:

    chat_prompt = f"""
    You are a financial advisor.

    User data:
    {st.session_state['user_data']}

    Answer this:
    {user_query}
    """

    chat_response = get_financial_advice({"custom_prompt": chat_prompt})

    st.write("🤖", chat_response)