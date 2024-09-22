# Set up and run this Streamlit App
import streamlit as st
import pandas as pd
# from helper_functions import llm # <--- Not needed anymore. The helper function is now directly called by `customer_query_handler` 🆕
from logics.customer_query_handler import process_user_message
from helper_functions.utility import check_password  


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Check if the password is correct.  
if not check_password():  
    st.stop()

# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App")


form = st.form(key="form")
form.subheader("Prompt")

# Initialize session state to store previous user input
if 'previous_prompt' not in st.session_state:
    st.session_state.previous_prompt = ""

# Initialize course_details
if 'course_details' not in st.session_state:
    st.session_state.course_details = None


user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    if user_prompt == st.session_state.previous_prompt:
        st.write("Same input as before, regenerating response...")
    else:
        st.toast(f"User Input Submitted - {user_prompt}") # This flashes a prompt to display the question asked
        st.session_state.previous_prompt = user_prompt

     # Get the response and course details
    try:
        response, course_details = process_user_message(user_prompt)
        
        # Fallback if response or course_details is None
        if response is None:
            response = "No response was generated."

        if course_details is None:
            course_details = []
            
        st.write(response)
        # Store course details in session state
        st.session_state.course_details = course_details

    except Exception as e:
        st.write(f"An error occurred: {e}")
    
    print(f"User Input is {user_prompt}")
    print(f'Reponse: {response}')
    
st.markdown('---')

st.subheader('List of Revelant Courses')

# Check if course details are available before displaying the DataFrame
if st.session_state.course_details:
    df = pd.DataFrame(st.session_state.course_details)
    st.dataframe(df)
else:
    st.write("No course details found yet.")

