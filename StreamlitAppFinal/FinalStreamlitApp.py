# Bring in the tools we need for the app to work
import streamlit as st  # The main app framework
import pandas as pd #Imports pandas and allows it to be reffered to as pd
import numpy as np  # Helps us do math with numbers
import matplotlib.pyplot as plt # Makes graphs and charts
import plotly.express as px # Makes interactive charts

# If we haven't created a spot to store past customer results yet, do it now
if "saved_customers" not in st.session_state:
    st.session_state["saved_customers"] = []  # this will hold dictionaries like {"name": ___, "clv": ___}



# Set how the app looks and feels when it loads
st.set_page_config(
    page_title="CLV Calculator",  # The tab title at the top of the browser
    layout="centered"             # Keep everything centered on the page
)
# Add a big title at the top of the app
st.title("📊 Customer Lifetime Value (CLV) Calculator")

# Write a little intro so users know what this is
st.markdown("""
Welcome! This app helps you figure out how valuable a customer is to your business 
based on their behavior and what kind of product you're selling.

Just fill out the info below, and we will do the math for you!
""")

# Start a form so all the inputs are grouped together nicely
with st.form(key='clv_form'):
    
    # Ask for the customer's name so we can label their CLV
    customer_name = st.text_input(
        "Customer Name",
        help="Give your customer a name so we can keep track of them!"
    )

    # Ask what kind of product we're working with
    product_type = st.selectbox(
        "Select Product Type",
        ["Subscription", "One-Time Purchase", "Luxury", "Consumable"],
        help="Different products affect how often people buy and how long they stay."
    )

    # Ask how old the customer is
    age = st.number_input(
        "Customer Age",
        min_value=10,
        max_value=100,
        value=30,
        help="Age might affect how long they stay a customer. Be honest!"
    )

    # Ask how much money they usually spend per order
    aov = st.number_input(
        "Average Order Value ($)",
        min_value=0.0,
        value=50.0,
        help="On average, how much does the customer spend in one purchase?"
    )

    # Ask how many times they buy in a year
    frequency = st.slider(
        "Purchases per Year",
        min_value=1,
        max_value=100,
        value=12,
        help="How many times per year does the customer make a purchase?"
    )

    # Ask how long they usually stick around
    lifespan = st.slider(
        "Customer Lifespan (years)",
        min_value=1,
        max_value=20,
        value=5,
        help="How many years will they likely remain a customer?"
    )

    # Ask what % of customers usually come back each year
    retention_rate = st.slider(
        "Retention Rate (0 to 1)",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.05,
        help="80% means 8 out of 10 customers stay year to year."
    )

    # Ask for a discount rate, which is used in finance math to bring future money to today’s value
    discount_rate = st.number_input(
        "Discount Rate (0 to 1)",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.01,
        help="Used to calculate the present value of future revenue. Usually 0.1 (10%)."
    )

    # Ask if they want to enter their Customer Acquisition Cost
    cac = st.number_input(
        "Customer Acquisition Cost (Optional)",
        min_value=0.0,
        value=0.0,
        help="How much did it cost you to get this customer?"
    )

    # Add a submit button so nothing runs until they click it
    submitted = st.form_submit_button("Calculate CLV")

# This code only runs if the user clicks the "Calculate CLV" button
if submitted:
    
    # Checking that AOV, frequency, and lifespan are positive so we don't do math with bad inputs
    if aov > 0 and frequency > 0 and lifespan > 0:
        
        # Calculating CLV using the discounted formula if retention is valid
        try:
            # CLV = (AOV × Frequency × Retention) / (1 + Discount Rate - Retention)
            clv = (aov * frequency * retention_rate) / (1 + discount_rate - retention_rate)

            # Multiplying by lifespan to spread it across the number of years
            clv = clv * lifespan

        except ZeroDivisionError:
            # If something goes wrong with dividing by 0, stop and show an error
            st.error("Oops! The formula broke because of a bad discount or retention rate.")
            clv = None

    else:
        # If any inputs were invalid, show this
        st.error("Please make sure AOV, frequency, and lifespan are greater than zero.")
        clv = None
    if clv is not None:
        # Show the calculated CLV, formatted with commas and two decimal places
        st.subheader("🧮 Estimated Customer Lifetime Value")
        st.metric(label="CLV (Total Revenue per Customer)", value=f"${clv:,.2f}")

        # Save this customer's name and CLV if a name was given
        if customer_name:
            # Save the info to session state
            st.session_state["saved_customers"].append({
                "name": customer_name,
                "clv": clv
            })

        # Figure out what we should do with this customer based on how valuable they are
        if cac > 0:
            # If the user gave us CAC, compare it to the CLV
            if clv >= 3 * cac:
                message = "✅ You should definitely invest in this customer."
            elif clv >= 1.5 * cac:
                message = "⚠️ You should consider investing in this customer."
            else:
                message = "❌ You should not invest in this customer."
        else:
            # If no CAC is given, just use fixed dollar amounts
            if clv >= 1000:
                message = "✅ You should definitely invest in this customer."
            elif clv >= 300:
                message = "⚠️ You should consider investing in this customer."
            else:
                message = "❌ You should not invest in this customer."

        # Show the message in a big, bold way
            st.markdown(f"### {message}")
        
            # Creating a list of CLV for each year based on linear growth
            yearly_clv = []
            for year in range(1, lifespan + 1):
                year_value = (aov * frequency * retention_rate) / (1 + discount_rate - retention_rate)
                yearly_clv.append(year_value)

            # Turning it into a DataFrame so labels work correctly
            clv_df = pd.DataFrame({
                "Year": list(range(1, lifespan + 1)),
                "CLV": yearly_clv
            })

            # Line chart that shows CLV accumulation over the years
            st.subheader("📈 CLV Accumulation Over Years")
            st.line_chart(clv_df.set_index("Year").cumsum())  # ← this line accumulates the value over time

# Let users upload a CSV file with customer info to calculate CLVs for many people at once
st.subheader("📂 Optional: Upload a CSV to Batch-Calculate CLVs")

uploaded_file = st.file_uploader("Upload your customer data (CSV). Make sure it has AOV, Frequency, Retention, Discount and Lifespan columns.", type=["csv"])

# If the user uploads a file, read and process it
if uploaded_file is not None:
    try:
        # Reading the file using pandas
        df = pd.read_csv(uploaded_file)

        # Checking that the needed columns are actually in the file
        required_cols = ["AOV", "Frequency", "Retention", "Lifespan", "Discount"]
        if all(col in df.columns for col in required_cols):
            
            # Create a new column in the table for CLV values
            df["CLV"] = (df["AOV"] * df["Frequency"] * df["Retention"]) / (1 + df["Discount"] - df["Retention"])
            df["CLV"] = df["CLV"] * df["Lifespan"]

            # Show the first few rows of the updated table
            st.write("✅ Calculated CLVs for your data:")
            st.dataframe(df)

            # Let the user download the new table with CLV column
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="clv_results.csv",
                mime="text/csv"
            )

        else:
            # If the file is missing important columns, give a heads-up
            st.error("Your file is missing one or more of these columns: AOV, Frequency, Retention, Lifespan, Discount")
    
    except Exception as e:
        st.error(f"Something went wrong reading the file: {e}")

# Creating an expandable section to compare two different customer profiles
with st.expander("🆚 Compare Two Customers (Optional)"):
    st.markdown("Try different inputs to compare two customer types side-by-side!")

    # Letting users enter the CLVs manually or reuse the formula later
    clv1 = st.number_input("Enter CLV for Customer A", min_value=0.0, value=500.0)
    clv2 = st.number_input("Enter CLV for Customer B", min_value=0.0, value=1000.0)

    # Showing which customer is more valuable
    if clv1 > clv2:
        st.success("🎯 Customer A has a higher lifetime value.")
    elif clv2 > clv1:
        st.success("🎯 Customer B has a higher lifetime value.")
    else:
        st.info("🤝 Both customers have equal lifetime value.")

        # Show the list of saved customer CLVs in the sidebar
st.sidebar.subheader("📋 Saved Customers")

# Loop through the saved entries and display them
if st.session_state["saved_customers"]:
    for entry in st.session_state["saved_customers"]:
        st.sidebar.write(f"**{entry['name']}** — CLV: ${entry['clv']:,.2f}")
else:
    st.sidebar.write("No customers saved yet.")


# Adding a nice footer so users know who made the app
st.markdown("---")
st.markdown("📘 **About this app:** Created for a Elements of Computing II project. Built with love using Streamlit.")
st.markdown("🔗 [Visit Streamlit](https://streamlit.io) to learn how to build your own interactive apps!")
