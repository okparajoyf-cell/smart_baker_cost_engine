import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Smart Baker Cost Engine", page_icon="🎂", layout="centered")
st.title("🎂 Smart Baker Cost & Profit Engine")
st.write("A simple, practical analytics framework for international micro-bakers.")

# Sidebar Settings (Includes Liberian Dollar as Default)
st.sidebar.header("🌐 Global Configurations")
currency_symbol = st.sidebar.selectbox("Preferred Currency", ["L$ (LRD)", "₦ (NGN)", "$ (USD)", "£ (GBP)", "€ (EUR)"])
currency = currency_symbol.split()[0]
hourly_rate = st.sidebar.number_input(f"Your Hourly Labor Rate ({currency})", min_value=0, value=500, step=100)

# Client Info
st.header("👤 Client & Order Information")
col_client1, col_client2 = st.columns(2)
with col_client1:
    customer_name = st.text_input("Customer Name", placeholder="e.g., Jane Doe")
with col_client2:
    delivery_date = st.date_input("Delivery Date", min_value=datetime.today())

# Main Form - Order Details & Labor Input
st.header("📋 Order Specifications")
col1, col2 = st.columns(2)
with col1:
    tiers = st.slider("Number of Tiers", min_value=1, max_value=5, value=1)
    icing = st.selectbox("Icing Finish", ["Buttercream", "Fondant", "Whipped Cream", "Ganache"])
with col2:
    # NEW MANUAL LABOR INPUT (Replaced the AI prediction)
    labor_hours = st.number_input("Hours Spent (From baking to packaging)", min_value=0.0, value=2.0, step=0.5, help="Type the exact hours you worked on this order.")
    distance = st.number_input("Delivery Distance (km)", min_value=0, value=0)

# SIMPLE INGREDIENT COST BOXES
st.header("🥣 Money Spent on Ingredients (For This Cake)")
st.write("Type in the exact amount you spent on the ingredients used for this specific order.")

col_ing1, col_ing2 = st.columns(2)
with col_ing1:
    cost_flour = st.number_input(f"Flour Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_butter = st.number_input(f"Butter / Margarine Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_sugar = st.number_input(f"Sugar Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
with col_ing2:
    cost_eggs = st.number_input(f"Eggs Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_milk_flavor = st.number_input(f"Milk & Flavoring Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_packaging = st.number_input(f"Boxes, Boards & Ribbons ({currency})", min_value=0.0, value=0.0, step=50.0)

# Totals Calculation
ingredient_cost = cost_flour + cost_butter + cost_sugar + cost_eggs + cost_milk_flavor + cost_packaging
labor_cost = labor_hours * hourly_rate
total_base_cost = labor_cost + ingredient_cost

# Profit Margin Settings
st.header("📈 Profit Target")
profit_percentage = st.slider("Desired Profit Margin (%)", min_value=0, max_value=100, value=30, step=5)

if profit_percentage < 100:
    selling_price = total_base_cost / (1 - (profit_percentage / 100))
else:
    selling_price = total_base_cost * 2
profit_earned = selling_price - total_base_cost

# Display Results
st.write("---")
st.header("💰 Price Analytics Breakdown")

if customer_name:
    st.subheader(f"Custom Quote for: **{customer_name}**")
    st.caption(f"Scheduled Delivery: {delivery_date.strftime('%B %d, %Y')}")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(label="Your Inputted Labor Time", value=f"{labor_hours:.1f} Hours")
    st.metric(label="Total Production Cost", value=f"{currency}{total_base_cost:,.2f}", help="Labor + Ingredients + Packaging")
with res_col2:
    st.metric(label="Target Profit Value", value=f"{currency}{profit_earned:,.2f}", delta=f"{profit_percentage}% Margin")
    st.metric(label="Final Retail Selling Price", value=f"{currency}{selling_price:,.2f}")

st.success("✨ Premium recipe-costed quote successfully generated!")
