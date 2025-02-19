#IMPORTS
import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Data Sweeper", page_icon="✨", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #eef2f7;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #2575fc, #6a11cb);
    }
    .stSubheader {
        color: #6a11cb;
        font-size: 24px;
        font-weight: bold;
    }
    .stTitle {
        color: #2575fc;
        font-size: 36px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("Data Sweeper ⚡")
st.write("🚀 Transform, clean, and visualize your data effortlessly. Supports CSV & Excel formats!")

# File uploader
uploaded_files = st.file_uploader("📂 Upload CSV or Excel file(s) ", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file format: {file_ext}")
            continue
        
        st.write(f"**📌 File:** {file.name} ({file.size / 1024:.2f} KB)")
        st.write("🔍 **Preview of Data**")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑 Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")
            
            with col2:
                if st.button("🔄 Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")
        
        # Column Selection
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect("Choose columns to retain", df.columns, default=df.columns)
        df = df[columns]
        
        # Data Visualization
        st.subheader("📊 Data Insights & Visualization")
        if st.checkbox("🔎 Show Summary Statistics"):
            st.write(df.describe())
        
        if st.checkbox("📉 Generate Visualizations"):
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                fig = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}")
                st.plotly_chart(fig)
            else:
                st.warning("⚠️ No numeric columns found for visualization.")
        
        # Data Conversion & Download
        st.subheader("💾 Convert & Download Data")
        conversion_type = st.radio("Convert to:", ['CSV', 'Excel'], key=file.name)
        if st.button("📥 Convert & Download"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
        
        # Progress Bar Simulation
        with st.spinner("Processing... 🔄"):
            for i in range(100):
                time.sleep(0.01)
                st.progress(i + 1)

st.success("🎉 Data Cleaning & Optimization Complete! 🚀")
