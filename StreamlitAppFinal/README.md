# Customer Lifetime Value (CLV) Calculator – Streamlit App

## Overview

This interactive Streamlit app helps users estimate Customer Lifetime Value (CLV) based on inputs like customer behavior, product type, and financial assumptions. It supports both individual customer analysis and batch processing via CSV upload. The app also provides decision-support messages based on the calculated CLV and acquisition cost.

## Setup and Run Instructions

### Requirements

Ensure you have the following packages installed:

- Python 3.7 or higher
- streamlit >= 1.20
- pandas >= 1.4
- numpy >= 1.21
- matplotlib >= 3.5
- plotly >= 5.5

### Running the App Locally

1. Clone this repository or download the files.
2. Navigate to the project folder:



## App Features

### Single Customer CLV Calculation

- User inputs:
- Customer name
- Product type
- Age, average order value, purchase frequency, customer lifespan
- Retention rate, discount rate, and optional acquisition cost
- App outputs:
- Calculated Customer Lifetime Value
- Investment recommendation (based on CLV vs CAC)
- Year-by-year CLV breakdown chart
- Running list of saved customer names and CLVs in the sidebar

### Batch CLV Calculation via CSV Upload

- Upload a `.csv` file containing the following columns:
- AOV, Frequency, Retention, Lifespan, Discount
- App calculates CLV for each row
- Returns a data table with CLV values and option to download results

### Customer CLV Comparison

- Input two CLVs manually
- App identifies which customer is more valuable

## References and Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
- [Customer Lifetime Value - Investopedia](https://www.investopedia.com/terms/c/customer_lifetime_value.asp)

## Visual Examples

**Main App Interface**  
_Screenshot placeholder_

**CLV Charts Output**  
_Screenshot placeholder_

**CSV Upload and Table Preview**  
_Screenshot placeholder_

---

Created for the Elements of Computing II final portfolio project.
