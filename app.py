import streamlit as st
import pandas as pd
from analyzer import analyze_finances
from llm_helper import get_financial_advice

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Finance Advisor", layout="wide")

st.title("💰 AI Finance Advisor")

# =========================
# SESSION STATE (CHAT MEMORY)
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_data" not in st.session_state:
    st.session_state.user_data = None

# =========================
# USER INPUT (2 COLUMN UI)
# =========================
st.subheader("👤 User Profile")

col1, col2 = st.columns(2)

with col1:
    salary = st.number_input("💰 Monthly Salary", min_value=0)
    age = st.number_input("🎂 Age", min_value=18, max_value=100)

with col2:
    savings = st.number_input("🏦 Current Savings")

# =========================
# EXPENSES
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

col3, col4 = st.columns(2)

with col3:
    loans = st.number_input("💳 Loan EMI (monthly)")
    cc_dues = st.number_input("💳 Credit Card Dues")

with col4:
    health_insurance = st.number_input("🛡 Health Insurance (yearly)")
    term_insurance = st.number_input("🛡 Term Insurance (yearly)")

# =========================
# GOALS
# =========================
st.subheader("🎯 Financial Goals")

goal = st.text_area("Your goals (house, car, retirement, etc.)")

# =========================
# ANALYZE BUTTON
# =========================
if st.button("🚀 Analyze"):

    result = analyze_finances(salary, expense_data)

    st.subheader("📊 Analysis")
    st.write(f"Total Expenses: ₹{result['total_expense']}")
    st.write(f"Savings: ₹{result['savings']}")

    for insight in result["insights"]:
        st.write("👉", insight)

    # 📊 Chart
    if expense_data:
        df = pd.DataFrame(list(expense_data.items()), columns=["Category", "Amount"])
        st.subheader("📊 Expense Breakdown")
        st.bar_chart(df.set_index("Category"))

    # Prepare data
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

    st.session_state.user_data = data

    # AI Advice
    with st.spinner("🤖 Generating financial advice..."):
        advice = get_financial_advice(data)

    st.subheader("🤖 AI Advice")
    st.write(advice)

# =========================
# CHAT SECTION (IMPROVED)
# =========================
st.subheader("💬 Financial Chat Assistant")

user_query = st.text_input("Ask anything about your finances")

if user_query and st.session_state.user_data:

    st.session_state.chat_history.append({"role": "user", "content": user_query})

    # Build conversation context
    full_context = ""
    for chat in st.session_state.chat_history:
        full_context += f"{chat['role']}: {chat['content']}\n"

    chat_prompt = f"""
    You are a smart financial advisor.

    User data:
    {st.session_state.user_data}

    Conversation so far:
    {full_context}

    Rules:
    - Do NOT repeat answers
    - Be clear and practical
    - Give personalized suggestions
    """

    with st.spinner("Thinking..."):
        response = get_financial_advice({"custom_prompt": chat_prompt})

    st.session_state.chat_history.append({"role": "assistant", "content": response})

# =========================
# DISPLAY CHAT (CHAT UI)
# =========================
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])