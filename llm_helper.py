from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Initialize client safely
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
        You are a smart financial advisor for Indian users.

        RULES:
        - Do NOT repeat points
        - Be concise and practical
        - Give new insights each time
        - Use simple language
        - Personalize based on user data

        User Profile:
        - Age: {data.get('age')}
        - Salary: {data.get('salary')}
        - Savings: {data.get('savings')}

        Expenses:
        {data.get('expenses')}

        Financial Obligations:
        - Loan EMI: {data.get('loans')}
        - Credit Card Dues: {data.get('cc_dues')}

        Insurance:
        - Health: {data.get('health_insurance')}
        - Term: {data.get('term_insurance')}

        Goals:
        {data.get('goals')}

        Give structured output:
        1. Key spending mistakes
        2. Savings improvement plan
        3. Debt reduction strategy
        4. Investment plan (SIP, FD, stocks)
        5. Retirement planning
        """

    # =========================
    # LLM CALL (with safety)
    # =========================
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",   # stable model
            contents=prompt
        )

        return response.text if response.text else "No response generated."

    except Exception as e:
         
        
         return f"ERROR: {str(e)}"
