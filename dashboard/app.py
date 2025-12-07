import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="Dynamic Crypto Dashboard", layout="wide")
DATA_PATH = os.path.join("data", "live.csv")

print(f"Step 1 ✅ : Starting to load data from: {DATA_PATH}")

# ---------------------------
# Load data
# ---------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_data(DATA_PATH)
print(f"Step 2 ✅ : Data loaded successfully with shape: {df.shape}")
print(f"Step 2a ✅ : Columns detected: {list(df.columns)}")
print(df.head())

# ---------------------------
# Extract numeric columns
# ---------------------------
numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
if not numeric_cols:
    st.error("No numeric columns found in data!")
    st.stop()
print(f"Step 3 ✅ : Numeric columns detected: {numeric_cols}")

# ---------------------------
# UI: Dropdowns / Slider
# ---------------------------
st.title("📊 Dynamic Crypto Dashboard")

col1, col2, col3, col4 = st.columns([3,3,2,2])
with col1:
    y_col = st.selectbox(
        "Column to Plot (Y-axis)", 
        options=numeric_cols, 
        index=numeric_cols.index("market_cap") if "market_cap" in numeric_cols else 0
    )
with col2:
    sort_col = st.selectbox(
        "Column to Sort By", 
        options=numeric_cols, 
        index=numeric_cols.index("market_cap") if "market_cap" in numeric_cols else 0
    )
with col3:
    sort_order = st.selectbox("Sort Order", options=["Descending", "Ascending"])
with col4:
    top_n = st.slider("Top N Coins", min_value=1, max_value=20, value=10, step=1)

print(f"Step 4 ✅ : User selections -> Y-axis: {y_col}, Sort by: {sort_col}, Order: {sort_order}, Top N: {top_n}")

# ---------------------------
# Prepare plot data
# ---------------------------
# Sort the data on sort_column
sorted_df = df.sort_values(by=sort_col, ascending=(sort_order == "Ascending"))
# take top N rows
sorted_df = sorted_df.head(top_n)

print("Step 5 ✅ : Data prepared for plotting")
print(sorted_df.head())

# if "name" in df.columns:
#     plot_df = sorted_df[["name", y_col, sort_col]].dropna()
#     ascending = True if sort_order == "Ascending" else False
#     plot_df = plot_df.sort_values(sort_col, ascending=ascending).head(top_n)
#     print(f"Step 5 ✅ : Plotting top {top_n} coins")

#     # ---------------------------
#     # Plot
#     # ---------------------------
#     fig = px.bar(
#         plot_df, 
#         x="coin", 
#         y=y_col, 
#         title=f"{y_col} by Coin (Top {top_n} sorted by {sort_col})"
#     )
#     st.plotly_chart(fig, use_container_width=True)
# else:
#     st.warning("Data does not contain a 'coin' column to plot!")

plot_df = sorted_df[["name", y_col]].fillna(0)

# Plot
fig = px.bar(
    plot_df,
    x="name",
    y=y_col,
    title=f"{y_col} by Coin",
    text=y_col
)
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
st.plotly_chart(fig, use_container_width=True)