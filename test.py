from streamlit_server_state import server_state, server_state_lock
import streamlit as st
import random

if "count" not in server_state:
    with server_state_lock["count"]:
        server_state["count"] = []

btn = st.button("Add")
if btn:
    with server_state_lock["count"]:
        server_state["count"] = server_state["count"] + [random.randint(0, 100)]

st.write(server_state["count"])