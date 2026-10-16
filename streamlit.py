import streamlit as st

st.title("Student Details Form")

st.write("Enter your details below")

# Label and text box
name = st.text_input("Enter your Name")
email = st.text_input("Enter your Email")
qualification = st.text_input("Enter your Qualification")

# Button
if st.button("Submit"):
    st.success("Details submitted successfully!")

    st.write("Name:", name)
    st.write("Email:", email)
    st.write("Qualification:", qualification)