import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Global Baker Cost Engine", page_icon="🎂", layout="centered")
st.title("🎂 Smart Baker Cost & Profit Engine")
st.write("A simple, practical pricing assistant for bakers worldwide.")

# SIDEBAR: Truly Global Currency Setup
st.sidebar.header("🌐 Global Configurations")
currency_choice = st.sidebar.selectbox(
    "Preferred Currency", 
    ["L$ (LRD)", "₦ (NGN)", "$ (USD)", "₵ (GHS)", "£ (GBP)", "€ (EUR)", "Other (Type Custom Symbol)"]
)

if currency_choice == "Other (Type Custom Symbol)":
    currency = st.sidebar.text_input("Enter your Currency Symbol (e.g., KSh, Le, R)", value="¤")
else:
    currency = currency_choice.split()[0]

hourly_rate = st.sidebar.number_input(f"Your Hourly Labor Rate ({currency})", min_value=0, value=500, step=100)

# SECTION 1: Client Info
st.header("👤 Client & Order Information")
col_client1, col_client2 = st.columns(2)
with col_client1:
    customer_name = st.text_input("Customer Name", placeholder="e.g., Jane Doe")
with col_client2:
    delivery_date = st.date_input("Delivery Date", min_value=datetime.today())

# SECTION 2: Order Specifications
st.header("📋 Order Specifications")
col1, col2 = st.columns(2)
with col1:
    tiers = st.slider("Number of Tiers", min_value=1, max_value=5, value=1)
    icing = st.selectbox("Icing Finish Type", ["Buttercream", "Fondant", "Whipped Cream", "Ganache", "Other"])
with col2:
    labor_hours = st.number_input("Hours Spent (Baking to Packaging)", min_value=0.0, value=2.0, step=0.5)
    distance = st.number_input("Delivery Distance (km) - Optional", min_value=0, value=0)

# SECTION 3: Streamlined Cost Inputs
st.header("🥣 Material & Production Costs")
st.write("Type in exactly what you spent to produce this specific cake:")

col_ing1, col_ing2 = st.columns(2)
with col_ing1:
    cost_flour = st.number_input(f"Flour Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_butter = st.number_input(f"Butter / Margarine Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    cost_sugar = st.number_input(f"Sugar Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
with col_ing2:
    cost_eggs = st.number_input(f"Eggs Cost ({currency})", min_value=0.0, value=0.0, step=50.0)
    # FIX: Explicit spot for icing ingredients/decorations
    cost_icing_decor = st.number_input(f"Icing & Decorating Materials ({currency})", min_value=0.0, value=0.0, step=50.0, help="Buttercream ingredients, whipped cream, fondant, sprinkles etc.")
    cost_packaging = st.number_input(f"Boxes, Boards & Ribbons ({currency})", min_value=0.0, value=0.0, step=50.0)

# Math calculations
ingredient_cost = cost_flour + cost_butter + cost_sugar + cost_eggs + cost_icing_decor + cost_packaging
labor_cost = labor_hours * hourly_rate
total_base_cost = labor_cost + ingredient_cost

# SECTION 4: Profit Margin
st.header("📈 Profit Target")
profit_percentage = st.slider("Desired Profit Margin (%)", min_value=0, max_value=100, value=30, step=5)

if profit_percentage < 100:
    selling_price = total_base_cost / (1 - (profit_percentage / 100))
else:
    selling_price = total_base_cost * 2
profit_earned = selling_price - total_base_cost

# SECTION 5: Final Breakdown Display
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
