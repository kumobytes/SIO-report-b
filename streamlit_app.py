import streamlit as st
import pandas as pd
from data_processing import process_data

st.title('SIO report processor')

st.subheader('Input CSV')

uploaded_file = st.file_uploader("Choose a file", type=["csv"])

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

if st.button("Process file"):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        processed_df = process_data(df)
        st.write("Here is your report:")
        st.dataframe(processed_df)

        csv = convert_df_to_csv(processed_df)
        st.download_button(
                label="Download Processed Data as CSV",
                data=csv,
                file_name='processed_data.csv',
                mime='text/csv'
            )
    else:
        st.write("Please upload a file before processing.")