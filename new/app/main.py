# app/main.py

import streamlit as st
import pandas as pd
import os
import plotly.express as px
from .config import APP_TITLE, UPLOAD_FOLDER, ERP_INTEGRATION_ENABLED, ECOMMERCE_INTEGRATION_ENABLED
from .utils import save_uploaded_file
from integration.erp_integration import integrate_with_erp
from integration.ecommerce_integration import integrate_with_ecommerce

# Set page configuration and title
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# Title and description
st.title(f"📊 {APP_TITLE}")
st.write("Gain insights into your inventory, and integrate with ERP & eCommerce platforms for a seamless experience.")

# Sidebar header
st.sidebar.header("File Upload Section")

# Ensure the uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# File upload logic
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file
    save_path = save_uploaded_file(uploaded_file, UPLOAD_FOLDER)
    
    st.sidebar.success(f"File successfully saved at: {save_path}")

    # Read the uploaded CSV file
    df = pd.read_csv(save_path)

    # Displaying the data
    st.subheader("Uploaded Data Preview")
    st.write("Here is a preview of your inventory data:")
    st.dataframe(df)

    # Displaying basic statistics
    st.subheader("Basic Data Statistics")
    st.write("Some basic statistics of your data:")
    st.write(df.describe())

    # Filter and visualize data
    st.sidebar.subheader("Analysis Options")
    category = st.sidebar.selectbox("Select Item Category", df["Category"].unique())

    # Filter data by selected category
    filtered_df = df[df["Category"] == category]
    st.subheader(f"Data for Category: {category}")
    st.dataframe(filtered_df)

    # Bar Chart for Inventory Count by Location
    st.markdown("### Inventory Count by Location")
    count_chart = px.bar(df, x="Location", y="Count", color="Item", title='Inventory Count by Location',
                         labels={'Location': 'Location', 'Count': 'Inventory Count'},
                         template='plotly_dark')
    st.plotly_chart(count_chart, use_container_width=True)

    # Pie Chart for Total Value Distribution
    st.markdown("### Total Value Distribution")
    value_distribution = df.groupby("Item")["Value"].sum().reset_index()
    pie_chart = px.pie(value_distribution, names='Item', values='Value',
                       title='Total Value Distribution by Item',
                       template='plotly_dark')
    st.plotly_chart(pie_chart, use_container_width=True)

    # Line Chart for Total Count Over Time (Assuming 'Date' column exists)
    if 'Date' in df.columns:
        st.markdown("### Total Inventory Count Over Time")
        line_chart = px.line(df, x="Date", y="Count", color="Category",
                             title='Total Inventory Count Over Time',
                             labels={'Date': 'Date', 'Count': 'Total Inventory Count'},
                             template='plotly_dark')
        st.plotly_chart(line_chart, use_container_width=True)

    # Additional insights
    st.subheader("Insights")
    st.write(f"**Total Count for {category}:** {filtered_df['Count'].sum()}")
    st.write(f"**Total Value for {category}:** ${filtered_df['Value'].sum():,.2f}")

    # ERP Integration (if enabled)
    if ERP_INTEGRATION_ENABLED:
        st.sidebar.subheader("ERP Integration")
        if st.sidebar.button("Integrate with ERP"):
            integration_result = integrate_with_erp(df)
            st.success(f"ERP Integration Result: {integration_result}")

    # eCommerce Integration (if enabled)
    if ECOMMERCE_INTEGRATION_ENABLED:
        st.sidebar.subheader("eCommerce Integration")
        if st.sidebar.button("Integrate with eCommerce"):
            ecommerce_result = integrate_with_ecommerce(df)
            st.success(f"eCommerce Integration Result: {ecommerce_result}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""<hr>
    <small>Developed by Your Name. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)

# Load header from header.html
with open('templates/header.html', 'r') as f:
    header_html = f.read()

st.markdown(header_html, unsafe_allow_html=True)
