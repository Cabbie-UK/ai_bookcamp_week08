import streamlit as st
import pandas as pd
from helper_functions.utility import check_password

# Check if the password is correct.  
if not check_password():  
    st.stop()

df = pd.read_json('./data/courses-full.json', orient='index')
df_reset = df.reset_index(drop=True)

st.dataframe(df_reset)