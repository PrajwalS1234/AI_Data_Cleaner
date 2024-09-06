import streamlit as st
import pandas as pd
import re

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Customize the main content background and padding */
    .reportview-container {
        background-color: #f0f2f6;
        padding: 1rem;
    }

    /* Customize the sidebar background and font color */
    .sidebar .sidebar-content {
        background-color: #ffffff;
        color: #000000;
    }

    /* Make headers bold and change font size */
    h1, h2, h3, h4 {
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: #333333;
    }

    /* Customize buttons */
    .stButton>button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        border-radius: 12px;
        padding: 10px 20px;
    }

    /* Customize the dataframe/table look */
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid #ddd;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    /* Add hover effects to buttons */
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }

    /* Add custom font for the entire app */
    body {
        font-family: 'Helvetica Neue', sans-serif;
    }

    </style>
    """, unsafe_allow_html=True)

apply_custom_styles()



# Title and instructions
st.title("Automating Data Cleaning")
st.write("This app allows you to clean and preprocess your dataset. Please enter the Google Drive link to your CSV file.")

# Function to convert ratio
def convert_ratio(x):
    if x not in ['inf', '-inf', 'nan', 'Nan']:
        try:
            percentage = round(float(x) * 100, 2)
            return percentage
        except ValueError:
            return x
    else:
        return x

# Function to replace symbols like '%' in the data
def replace_symbol(x):
    x = str(x)
    if '%' in str(x):
        x = x.replace('%', '').replace(' ', '')
        return x
    else:
        return x

# Function to check if a value is not numeric
def not_numeric(x):
    if x not in ['inf', '-inf', 'NaN', 'nan']:
        try:
            float(x)
            return False
        except:
            return True
    else:
        return True

# Function to replace commas and clean data
def replacecomma(x):
    if isinstance(x, str):
        x = x.replace(',', '').replace('RU', '0')
        return x
    else:
        return x

# Input for Google Drive link
df_link = st.text_input("Please enter the Google Drive link to your dataset (.csv):")

# Checking if the link is valid and extracting the file ID
if df_link:
    # Extracting the Google Drive file ID from the provided link
    file_id_pattern = r"[-\w]{25,}"
    file_id_match = re.search(file_id_pattern, df_link)
    
    if file_id_match:  # Only proceed if a valid file ID is found
        file_id = file_id_match.group()
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        st.write(f"Downloading dataset from: {download_url}")

        # Downloading and loading the CSV file
        try:
            df = pd.read_csv(download_url)
            st.success("File downloaded and loaded successfully!")
            
            # Display basic info about the dataset
            st.write("Dataset Information:")
            st.write(df.info())

            # Handling null values
            for col in df.columns:
                if df[col].dtype in ["int64", "float64"]:
                    if df[col].isnull().sum() != 0:
                        st.write(f"We have no ticed that you have null values in your {col} column")
                        choice = st.radio(f"How would you like to handle null values in {col}?", 
                                          ("Mean", "Median", "Drop these entries"))
                        
                        if choice == "Mean":
                            df[col].fillna(df[col].mean(), inplace=True)
                        elif choice == "Median":
                            df[col].fillna(df[col].median(), inplace=True)
                        elif choice == "Drop these entries":
                            df.dropna(subset=[col], inplace=True)

            # Show the cleaned data
            st.write("Cleaned Data Preview:")
            st.dataframe(df.head())

            # Option to download the cleaned dataset
            csv = df.to_csv(index=False)
            st.download_button(label="Download Cleaned Dataset", data=csv, file_name='cleaned_data.csv', mime='text/csv')

        except Exception as e:
            st.error(f"An error occurred while downloading the file: {e}")
    else:
        st.write("Please enter a valid Google Drive link.")
