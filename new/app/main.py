import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Advanced Reporting & Dashboards",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Advanced Reporting & Dashboards")
st.write("Gain insights into your inventory and supply chain performance by uploading your data.")

# Sidebar header
st.sidebar.header("File Upload Section")

# Create an 'uploads' directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File upload logic
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file to the 'uploads' directory
    save_path = os.path.join("uploads", uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

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
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x="Location", y="Count", hue="Item")
    plt.title('Inventory Count by Location')
    plt.xlabel('Location')
    plt.ylabel('Inventory Count')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    st.pyplot(plt)

    # Pie Chart for Total Value Distribution
    st.markdown("### Total Value Distribution")
    value_distribution = df.groupby("Item")["Value"].sum().reset_index()
    
    plt.figure(figsize=(8, 8))
    plt.pie(value_distribution['Value'], labels=value_distribution['Item'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Total Value Distribution by Item')
    st.pyplot(plt)

    # Line Chart for Total Count Over Time (Assuming 'Date' column exists)
    if 'Date' in df.columns:
        st.markdown("### Total Inventory Count Over Time")
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x="Date", y="Count", hue="Category")
        plt.title('Total Inventory Count Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Inventory Count')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(plt)

    # Additional insights
    st.subheader("Insights")
    st.write(f"**Total Count for {category}:** {filtered_df['Count'].sum()}")
    st.write(f"**Total Value for {category}:** ${filtered_df['Value'].sum():,.2f}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""<hr>
    <small>Developed by Your Name. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)
