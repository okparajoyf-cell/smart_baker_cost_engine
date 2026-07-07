import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Smart Baker Cost Engine", page_icon="🎂", layout="wide")
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
currency_symbol = st.sidebar.selectbox("Preferred Currency", ["₦ (NGN)", "L$ (LRD)", "$ (USD)", "£ (GBP)", "€ (EUR)"])
currency = currency_symbol.split()[0]
hourly_rate = st.sidebar.number_input(f"Your Hourly Labor Rate ({currency})", min_value=0, value=3000, step=500)

# Layout Split
main_col, worksheet_col = st.columns([1, 1], gap="large")

with main_col:
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

    # Packaging & Extras
    st.header("📦 Packaging & Extras")
    packaging_cost = st.number_input(f"Boxes, Boards, Ribbons Total ({currency})", min_value=0.0, value=0.0, step=200.0)

    # Profit Margin Settings
    st.header("📈 Profit Target")
    profit_percentage = st.slider("Desired Profit Margin (%)", min_value=0, max_value=100, value=30, step=5)

with worksheet_col:
    # SIMPLIFIED SECTION: Recipe Ingredients
    st.header("🥣 Simplified Ingredient Costs")
    st.write("Set your estimated cost for a standard portion (like per 100g or per 1 egg), then input how much the recipe uses.")
    
    # Simple setup
    simple_ingredients = [
        {"Ingredient": "Flour", "Cost per 100g": 180.0, "Grams Used in Recipe": 500},
        {"Ingredient": "Margarine/Butter", "Cost per 100g": 700.0, "Grams Used in Recipe": 400},
        {"Ingredient": "Sugar", "Cost per 100g": 200.0, "Grams Used in Recipe": 400},
        {"Ingredient": "Eggs", "Cost per 1 Egg": 140.0, "Number of Eggs Used": 6},
        {"Ingredient": "Flavoring", "Cost per 10ml": 150.0, "Amount Used (ml)": 15},
        {"Ingredient": "Milk", "Cost per 100ml": 250.0, "Amount Used (ml)": 250},
    ]
    df_ingredients = pd.DataFrame(simple_ingredients)
    
    # Render an editable table
    edited_df = st.data_editor(
        df_ingredients,
        column_config={
            "Ingredient": st.column_config.TextColumn("Ingredient", disabled=True),
            "Cost per 100g": st.column_config.NumberColumn(f"Cost per Unit ({currency})"),
            "Grams Used in Recipe": st.column_config.NumberColumn("Amount Used"),
            "Cost per 1 Egg": st.column_config.NumberColumn(f"Cost per Unit ({currency})"),
            "Number of Eggs Used": st.column_config.NumberColumn("Amount Used"),
            "Cost per 10ml": st.column_config.NumberColumn(f"Cost per Unit ({currency})"),
            "Amount Used (ml)": st.column_config.NumberColumn("Amount Used"),
            "Cost per 100ml": st.column_config.NumberColumn(f"Cost per Unit ({currency})"),
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Clean programmatic math based on row index
    unit_costs = []
    # Flour (per 100g)
    unit_costs.append((edited_df.iloc[0, 1] / 100) * edited_df.iloc[0, 2])
    # Butter (per 100g)
    unit_costs.append((edited_df.iloc[1, 1] / 100) * edited_df.iloc[1, 2])
    # Sugar (per 100g)
    unit_costs.append((edited_df.iloc[2, 1] / 100) * edited_df.iloc[2, 2])
    # Eggs (per single egg)
    unit_costs.append(edited_df.iloc[3, 1] * edited_df.iloc[3, 2])
    # Flavoring (per 10ml)
    unit_costs.append((edited_df.iloc[4, 1] / 10) * edited_df.iloc[4, 2])
    # Milk (per 100ml)
    unit_costs.append((edited_df.iloc[5, 1] / 100) * edited_df.iloc[5, 2])
    
    ingredient_cost = sum(unit_costs)
    st.info(f"💡 **Total Calculated Ingredient Cost:** {currency}{ingredient_cost:,.2f}")

# Calculations Engine
input_data = pd.DataFrame([[tiers, complexity_score, distance]], columns=["tiers", "complexity", "distance"])
predicted_hours = float(ai_brain.predict(input_data)[0])

if icing == "Fondant":
    predicted_hours += 1.5
elif icing == "Ganache":
    predicted_hours += 1.0

labor_cost = predicted_hours * hourly_rate
total_base_cost = labor_cost + ingredient_cost + packaging_cost

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
    st.metric(label="Total Production Cost", value=f"{currency}{total_base_cost:,.2f}")
with res_col2:
    st.metric(label="Target Profit Value", value=f"{currency}{profit_earned:,.2f}", delta=f"{profit_percentage}% Margin")
    st.metric(label="Final Retail Selling Price", value=f"{currency}{selling_price:,.2f}")

st.success("✨ Premium recipe-costed quote successfully generated!")
