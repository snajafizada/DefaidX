import streamlit as st

def show_contact():
    st.markdown(
        """
        <h1 style='font-size:42px;color:#A970FF;font-weight:bold;'>
            Contact Us
        </h1>
        <p style='font-size:16px;color:#E0E0E0;line-height:1.6;'>
            We'd love to hear from you!
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <label style='font-weight:bold; color:#FFFFFF; font-size:16px;'>Your Name</label>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("", key="contact_name")

    st.markdown(
        """
        <label style='font-weight:bold; color:#FFFFFF; font-size:16px;'>Your Email</label>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("", key="contact_email")

    st.markdown(
        """
        <label style='font-weight:bold; color:#FFFFFF; font-size:16px;'>Message</label>
        """,
        unsafe_allow_html=True,
    )
    st.text_area("", key="contact_message")

    st.button("Submit")
