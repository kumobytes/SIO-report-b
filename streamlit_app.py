import streamlit as st
import pandas as pd
from data_processing import process_data

# title element
st.title('SIO report processor')

# instruction element
st.subheader('Input CSV')

# streamlit function - creates a widget that reads a file
uploaded_file = st.file_uploader("Choose a file", type=["csv"])

# for the output button - although st.dataframe below also allows csv download... just to make it easier
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Process data using function in data_processing
if st.button("Process file"):
    # handling odd cases, let's assume no one's going to upload other types of files...
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        processed_df = process_data(df)
        # text element
        st.write("Here is your report:")
        # gives a preview of the output
        st.dataframe(processed_df)

        # converts the dataset into a csv
        csv = convert_df_to_csv(processed_df)
        # download
        st.download_button(
                label="Download Processed Data as CSV",
                data=csv,
                file_name='processed_data.csv',
                mime='text/csv'
            )
    else:
        st.write("Please upload a file before processing.")