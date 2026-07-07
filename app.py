import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Smart Baker Cost Engine", page_icon="🎂", layout="centered")
st.title("🎂 Smart Baker Cost & Profit Engine")
st.write("An intelligent analytics framework for international micro-bakers.")

@st.cache_resource
def train_bakery_ai():
    np.random.seed(42)
    num_orders = 200
    X_mock = pd.DataFrame({
        "tiers": np.random.choice([1, 2, 3, 4], size=num_orders, p=[0.5, 0.3, 0.15, 0.05]),
        "complexity": np.random.choice([1, 2, 3], size=num_orders, p=[0.6, 0.3, 0.1]),
        "distance": np.random.uniform(0, 40, size=num_orders)
    })
    y_hours = (X_mock["tiers"] * 3.5) + (X_mock["complexity"] * 5.0) + (X_mock["distance"] * 0.05) + np.random.normal(0, 1, num_orders)
    y_hours = np.clip(y_hours, 2, 40)
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_mock, y_hours)
    return model

ai_brain = train_bakery_ai()

# Sidebar Settings (Includes Liberian Dollar)
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

# Main Form - Order Details
st.header("📋 Order Specifications")
col1, col2 = st.columns(2)
with col1:
    tiers = st.slider("Number of Tiers", min_value=1, max_value=5, value=1)
    icing = st.selectbox("Icing Finish", ["Buttercream", "Fondant", "Whipped Cream", "Ganache"])
with col2:
    complexity_label = st.selectbox("Design Complexity", ["Simple", "Detailed", "Elaborate"])
    distance = st.number_input("Delivery Distance (km)", min_value=0, value=0)

complexity_mapping = {"Simple": 1, "Detailed": 2, "Elaborate": 3}
complexity_score = complexity_mapping[complexity_label]

# ULTRA-SIMPLE INGREDIENT COST BOXES
st.header("🥣 Money Spent on Ingredients (For This Cake)")
st.write("Just type in the exact amount you spent on the ingredients used for this specific order.")

col_ing1, col_ing2 = st.columns(2)
with col_ing1:
    cost_flour = st.number_input(f"Flour Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_butter = st.number_input(f"Butter / Margarine Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_sugar = st.number_input(f"Sugar Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
with col_ing2:
    cost_eggs = st.number_input(f"Eggs Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_milk_flavor = st.number_input(f"Milk & Flavoring Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_packaging = st.number_input(f"Boxes, Boards & Ribbons ({currency})", min_value=0.0, value=0.0, step=50.0)

ingredient_cost = cost_flour + cost_butter + cost_sugar + cost_eggs + cost_milk_flavor + cost_packaging

# Profit Margin Settings
st.header("📈 Profit Target")
profit_percentage = st.slider("Desired Profit Margin (%)", min_value=0, max_value=100, value=30, step=5)

# Calculations Engine
input_data = pd.DataFrame([[tiers, complexity_score, distance]], columns=["tiers", "complexity", "distance"])
predicted_hours = float(ai_brain.predict(input_data)[0])

if icing == "Fondant":
    predicted_hours += 1.5
elif icing == "Ganache":
    predicted_hours += 1.0

labor_cost = predicted_hours * hourly_rate
total_base_cost = labor_cost + ingredient_cost

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
    st.metric(label="Predicted Labor Time", value=f"{predicted_hours:.1f} Hours")
    st.metric(label="Total Production Cost", value=f"{currency}{total_base_cost:,.2f}", help="Labor + Ingredients + Packaging")
with res_col2:
    st.metric(label="Target Profit Value", value=f"{currency}{profit_earned:,.2f}", delta=f"{profit_percentage}% Margin")
    st.metric(label="Final Retail Selling Price", value=f"{currency}{selling_price:,.2f}")

st.success("✨ Premium recipe-costed quote successfully generated!")
