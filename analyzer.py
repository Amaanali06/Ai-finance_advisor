def analyze_finances(salary, expenses):
    total_expense = sum(expenses.values())
    savings = salary - total_expense

    insights = []

    # Savings check
    if savings < salary * 0.2:
        insights.append("⚠️ Your savings are less than 20% of your salary.")
    else:
        insights.append("✅ Good savings habit.")

    # Rent check
    if "rent" in expenses and expenses["rent"] > salary * 0.4:
        insights.append("⚠️ Rent is too high (more than 40% of salary).")

    # Entertainment check
    if "entertainment" in expenses and expenses["entertainment"] > salary * 0.1:
        insights.append("⚠️ Too much spending on entertainment.")

    return {
        "total_expense": total_expense,
        "savings": savings,
        "insights": insights
    }