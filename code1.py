import streamlit as st
import json

st.title("💰 Expense Tracker")

if "expenses" not in st.session_state:
    try:
        with open("expenses.json", "r") as file:
            st.session_state.expenses = json.load(file)
    except:
        st.session_state.expenses = []

with st.form("expense_form"):
    category = st.text_input("Category")
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0)

    submit = st.form_submit_button("Add Expense")

    if submit:
        expense = {
            "category": category,
            "description": description,
            "amount": amount
        }

        st.session_state.expenses.append(expense)

        with open("expenses.json", "w") as file:
            json.dump(st.session_state.expenses, file, indent=4)

        st.success("Expense added successfully!")

st.subheader("Expenses")

st.table(st.session_state.expenses)

total = sum(expense["amount"] for expense in st.session_state.expenses)

st.write("Total Expense:", total)
