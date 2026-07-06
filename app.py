import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# 1. Page Configuration
st.set_page_config(page_title="Smart Baker Cost Engine", page_icon="🎂", layout="centered")
st.title("🎂 Smart Baker Cost & Profit Engine")
st.write("An intelligent analytics framework for international micro-bakers.")

# 2. Re-train the AI Brain in the background (using our robust dataset rules)
@st.cache_resource
def train_bakery_ai():
    np.random.seed(42)
    num_orders = 200
    X_mock = pd.DataFrame({
        "tiers": np.random.choice([1, 2, 3, 4], size=num_orders, p=[0.5, 0.3, 0.15, 0.05]),
        "icing_type_Buttercream": np.random.choice([1, 0], size=num_orders, p=[0.6, 0.4]),
        "icing_type_Fondant": np.random.choice([0, 1], size=num_orders, p=[0.6, 0.4]),
        "complexity_Intricate": np.random.choice([0, 1], size=num_orders, p=[0.8, 0.2]),
        "complexity_Moderate": np.random.choice([0, 1], size=num_orders, p=[0.6, 0.4]),
        "complexity_Simple": np.random.choice([1, 0], size=num_orders, p=[0.6, 0.4]),
        "delivery_distance_km": np.random.randint(0, 40, size=num_orders)
    })
    y_mock = 2.0 + (X_mock["tiers"] - 1) * 2.5 + (X_mock["icing_type_Fondant"] * 3.0) + (X_mock["complexity_Intricate"] * 5.0)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_mock, y_mock)
    return model, X_mock.columns

cake_ai_model, feature_columns = train_bakery_ai()

# 3. Sidebar: International Settings (Simulating Database Profile)
st.sidebar.header("🌍 International Settings")
currency = st.sidebar.selectbox("Preferred Currency", ["₦ (NGN)", "$ (USD)", "₵ (GHS)", "L$ (LRD)"])
currency_symbol = currency.split()[0]
hourly_rate = st.sidebar.number_input(f"Your Hourly Labor Rate ({currency_symbol})", value=3000)

# 4. Main Form: Order Customization
st.header("📋 New Order Details")
col1, col2 = st.columns(2)

with col1:
    tiers = st.slider("Number of Tiers", min_value=1, max_value=4, value=1)
    icing = st.selectbox("Icing Finish", ["Buttercream", "Fondant"])

with col2:
    complexity = st.selectbox("Design Complexity", ["Simple", "Moderate", "Intricate"])
    distance = st.number_input("Delivery Distance (km)", min_value=0, value=0)

# 5. Process Frontend Inputs for the AI
input_row = pd.DataFrame([{
    "tiers": tiers,
    "delivery_distance_km": distance,
    "icing_type_Buttercream": 1 if icing == "Buttercream" else 0,
    "icing_type_Fondant": 1 if icing == "Fondant" else 0,
    "complexity_Intricate": 1 if complexity == "Intricate" else 0,
    "complexity_Moderate": 1 if complexity == "Moderate" else 0,
    "complexity_Simple": 1 if complexity == "Simple" else 0
}])
input_row = input_row.reindex(columns=feature_columns, fill_value=0)

# 6. Calculate Prediction and Dynamic Pricing Metrics
predicted_hours = cake_ai_model.predict(input_row)[0]
labor_cost = predicted_hours * hourly_rate
delivery_cost = distance * 200
suggested_total = labor_cost + delivery_cost

st.markdown("---")
st.header("⚡ AI-Driven Pricing Insights")

m1, m2, m3 = st.columns(3)
m1.metric("Predicted Labor", f"{predicted_hours:.1f} Hours")
m2.metric("Calculated Labor Cost", f"{currency_symbol}{labor_cost:,.2f}")
m3.metric("Recommended Price", f"{currency_symbol}{suggested_total:,.2f}")

st.success("✨ Predictive quote successfully generated! This ensures your margins remain protected against hidden labor leaks.")
