import streamlit as st
import subprocess
import backend
import time

def send_data_to_dummy(user):
    with open('dummy.txt', 'w') as f:
        f.write(str(user))
    # create socket connection
    time.sleep(2)
    bash_command = ["streamlit", "run", "userapp.py", "--server.port", "8502"]    
    result = subprocess.Popen(bash_command)
    # send user data to userapp.py

st.sidebar.title("Instagram")
page = st.sidebar.radio("Navigation", ("register", "login"))

if page == 'register':
    st.title("Instagram Sign Up")
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    profile_name = st.text_input("Profile Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    bio = st.text_area("Bio")
    account_type = st.radio("Account Type", ("regular", "business"))

    if st.button("Sign Up"):
        if fname and lname and profile_name and email and password and bio and account_type:
            backend.create_user(fname, lname, profile_name, email, password, bio, account_type)
            st.success("User signed up successfully!")
            response = send_data_to_dummy(backend.authenticate_user(email, password))
        else:
            st.error("Please fill all the fields.")

elif page == 'login':
    st.title("Instagram Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            user = backend.authenticate_user(email, password)
            if user:
                st.success("User authenticated successfully!")
                response = send_data_to_dummy(user)
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please fill all the fields.")
