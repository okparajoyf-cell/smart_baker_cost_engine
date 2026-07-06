import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

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
    # Base labor hours calculation
    y_hours = (X_mock["tiers"] * 3.5) + (X_mock["complexity"] * 5.0) + (X_mock["distance"] * 0.05) + np.random.normal(0, 1, num_orders)
    y_hours = np.clip(y_hours, 2, 40)
    
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X_mock, y_hours)
    return model

ai_brain = train_bakery_ai()

# Sidebar Settings
st.sidebar.header("🌐 Global Configurations")
currency_symbol = st.sidebar.selectbox("Preferred Currency", ["₦ (NGN)", "$ (USD)", "£ (GBP)", "€ (EUR)"])
currency = currency_symbol.split()[0]
hourly_rate = st.sidebar.number_input(f"Your Hourly Labor Rate ({currency})", min_value=0, value=3000, step=500)

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

# NEW SECTION: Material & Ingredient Costs
st.header("🥣 Material & Production Costs")
col3, col4 = st.columns(2)
with col3:
    ingredient_cost = st.number_input(f"Ingredients Cost ({currency}) — Flour, Butter, Sugar, etc.", min_value=0.0, value=0.0, step=500.0)
with col4:
    packaging_cost = st.number_input(f"Packaging & Extras ({currency}) — Boxes, Boards, Ribbons", min_value=0.0, value=0.0, step=200.0)

# Calculations
input_data = pd.DataFrame([[tiers, complexity_score, distance]], columns=["tiers", "complexity", "distance"])
predicted_hours = float(ai_brain.predict(input_data)[0])

# Adjust hours slightly based on icing type
if icing == "Fondant":
    predicted_hours += 1.5
elif icing == "Ganache":
    predicted_hours += 1.0

labor_cost = predicted_hours * hourly_rate
material_cost = ingredient_cost + packaging_cost
grand_total = labor_cost + material_cost

# Display Results
st.write("---")
st.header("💰 Price Analytics Breakdown")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(label="Predicted Labor Time", value=f"{predicted_hours:.1f} Hours")
    st.metric(label="Calculated Labor Cost", value=f"{currency}{labor_cost:,.2f}")
with res_col2:
    st.metric(label="Total Material Cost", value=f"{currency}{material_cost:,.2f}")
    st.metric(label="Recommended Grand Total", value=f"{currency}{grand_total:,.2f}")

st.success("✨ Comprehensive quote successfully generated! This ensures your materials are covered and your labor is protected.")
