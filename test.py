from streamlit_server_state import server_state, server_state_lock
import streamlit as st

ADMIN_PASSWORD = "991152"

if "MESSAGES" not in server_state:
    with server_state_lock["MESSAGES"]:
        server_state["MESSAGES"] = []

    with server_state_lock["PASSWORD"]:
        server_state["PASSWORD"] = "281022"
    
    with server_state_lock["IMAGE"]:
        server_state["IMAGE"] = None

def adminView():
    new_password = st.sidebar.text_input("New Password")
    confirm_password = st.sidebar.text_input("Confirm Password")
    change_btn = st.sidebar.button("Change")

    if change_btn:
        if new_password == confirm_password:
            with server_state_lock["PASSWORD"]:
                server_state["PASSWORD"] = new_password
            st.success("Password Changed Successfully!")
        else:
            st.error("Passwords Do Not Match!")

def userView():
    name = st.sidebar.text_input("Name", value="Unknown")
    col1, col2 = st.columns(2)

    with col1:
        message = st.text_area("Message")
        send_btn = st.button("Send", key=1)
    
    with col2:
        camera_input = st.camera_input("Take Picture")
        send_camera_btn = st.button("Send", key=2)
    
    if send_btn:
        if message != "":
            with server_state_lock["MESSAGES"]:
                server_state["MESSAGES"] = server_state["MESSAGES"] + [{"NAME": name, "MESSAGE": message}]
    
    if send_camera_btn:
        with server_state_lock["IMAGE"]:
            server_state["IMAGE"] = {"NAME": name, "IMAGE": camera_input}

def display():
    col1, col2 = st.columns(2)
    with col1:
        if len(server_state["MESSAGES"]) > 0:
            message_str = ""
            for message in reversed(server_state["MESSAGES"]):
                message_str += f"{message['MESSAGE']} - {message['NAME']}\n"
            st.text_area("", message_str)
    with col2:
        if server_state["IMAGE"] is not None:
            col2.image(server_state["IMAGE"]["IMAGE"], server_state["IMAGE"]["NAME"])

password_input = st.sidebar.text_input("Password")

if password_input:
    if password_input == ADMIN_PASSWORD:
        adminView()
    elif password_input == server_state["PASSWORD"]:
        userView()
        display()