import os
import streamlit as st
import base64
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Uber", layout="wide")

# Main function
def main():
    st.markdown("<h1 style='text-align: center;'>DATA UBER - Dwell in data verity</h1>", unsafe_allow_html=True)
    st.sidebar.title("COLUMBUS - The Explorer")

    # File upload
    uploaded_file = st.sidebar.file_uploader("📂 Upload your CSV dataset", type='csv')
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded!")
    else:
        st.info("Please upload a CSV file to begin.")
        return

    # Data Overview
    st.sidebar.subheader("📊 Data Description")
    if st.sidebar.checkbox("Show preview"):
        number = st.number_input("Select number of rows", value=5, step=1, max_value=len(df))
        st.dataframe(df.head(number))

    if st.sidebar.checkbox("Show column names"):
        st.write(df.columns.tolist())

    if st.sidebar.checkbox("Show data shape"):
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        dim = st.radio("Dimension", ("Rows", "Columns"))
        st.write(df.shape[0] if dim == "Rows" else df.shape[1])

    if st.sidebar.checkbox("Select columns to view"):
        selected_columns = st.multiselect("Columns", df.columns.tolist())
        st.dataframe(df[selected_columns])

    if st.sidebar.checkbox("Show summary statistics"):
        st.write(df.describe().T)

    # Data Cleaning
    st.sidebar.subheader("🧹 Data Cleaning")
    if st.sidebar.checkbox("Remove empty rows"):
        df.dropna(inplace=True)
        st.success("Empty rows removed.")

    if st.sidebar.checkbox("Remove empty columns"):
        df.dropna(axis=1, inplace=True)
        st.success("Empty columns removed.")

    if st.sidebar.checkbox("Convert to best fit data types"):
        df = df.convert_dtypes()
        st.success("Converted to best fit data types.")

    if st.sidebar.button("Show data types"):
        st.write(df.dtypes)

    if st.sidebar.checkbox("Remove outliers"):
        col = st.selectbox("Select column", options=df.select_dtypes(include='number').columns.tolist())
        if col:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            df = df[(df[col] >= q1 - 1.5 * iqr) & (df[col] <= q3 + 1.5 * iqr)]
            st.success(f"Outliers removed from {col}")
            st.dataframe(df)

    # Visualization
    st.sidebar.subheader("📈 Data Visualization")
    plot_type = st.sidebar.selectbox("Plot type", ["area", "bar", "line"])
    plot_cols = st.multiselect("Select columns for plotting", options=df.select_dtypes(include='number').columns.tolist())

    if st.button("Generate Plot"):
        if plot_cols:
            st.success(f"Showing {plot_type} chart for {plot_cols}")
            plot_data = df[plot_cols]
            if plot_type == "area":
                st.area_chart(plot_data)
            elif plot_type == "bar":
                st.bar_chart(plot_data)
            elif plot_type == "line":
                st.line_chart(plot_data)
        else:
            st.warning("Please select at least one numeric column to plot.")

    # Download cleaned data
    st.sidebar.subheader("⬇️ Download Cleaned Dataset")
    if not df.empty:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.sidebar.markdown(
            f'<a href="data:file/csv;base64,{b64}" download="CleanFile.csv">Download CSV</a>',
            unsafe_allow_html=True
        )

    # About
    st.sidebar.header("ℹ️ About")
    if st.sidebar.button("About"):
        st.sidebar.markdown("""
        **Author**: Rajat Pandey  
        **License**: Public Domain  
        **Year**: 2020
        """)

# Hide Streamlit style
hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
