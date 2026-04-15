from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
from google import genai
import os

# 🔐 Use environment variable (for deployment safety)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_financial_advice(data):

    # =========================
    # CHAT MODE (Follow-up Q&A)
    # =========================
    if "custom_prompt" in data:
        prompt = data["custom_prompt"]

    # =========================
    # MAIN ANALYSIS MODE
    # =========================
    else:
        prompt = f"""
        You are a financial advisor for Indian users.

        User Profile:
        - Age: {data['age']}
        - Salary: {data['salary']}
        - Savings: {data['savings']}

        Expenses:
        {data['expenses']}

        Financial Obligations:
        - Loan EMI: {data['loans']}
        - Credit Card Dues: {data['cc_dues']}

        Insurance:
        - Health: {data['health_insurance']}
        - Term: {data['term_insurance']}

        Goals:
        {data['goals']}

        Give:
        1. Spending mistakes
        2. Savings improvement plan
        3. Debt reduction strategy
        4. Investment plan (SIP, FD, stocks)
        5. Retirement planning based on age
        """

    # =========================
    # LLM CALL
    # =========================
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text