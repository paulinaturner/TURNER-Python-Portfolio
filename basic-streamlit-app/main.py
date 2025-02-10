
import streamlit as st
import pandas as pd
st.title("Welcome to my Streamlit app!")
st.write("This website allows you to navigate through different datasets like the penguins dataset.")
df = pd.read_csv("data/penguins.csv")
st.write(df)
bill_length_mm = st.slider ("Choose a bill length.",
            min_value = df["bill_length_mm"].min(),
            max_value = df["bill_length_mm"].max(),
            )
st.write(f"Bill lengths es under {bill_length_mm}")
st.dataframe(df[df["bill_length_mm"] <= bill_length_mm]) 
