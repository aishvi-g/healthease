import psycopg2 as psy
import streamlit as st
from streamlit_chat import message
from hugchat import hugchat
import random
import pandas as pd

# #Establish connection with postgresql database
# connection = psy.connect(
#     host="localhost",
#     port="5432",
#     database="postgres",
#     user="postgres",
#     password="12345"
# )

# cursor = connection.cursor()

#title and sidebar
st.set_page_config(page_title = "HealthStack Chatbot")

with st.sidebar:
    st.title("HealthStack Chatbot")
    st.markdown('''
    
        Interact with our chatbot to get your queries resolved.

        Our chatbot comes with following funtionlitites:
        - Book / Cancel Appointment
        - View Prescription
        - Set Reminders
        - View Lab reports
        - Explain Medical terms
        
    ''')

    st.write("  Made with lots of LOVE - Team 43")

Start_conversation = ["Hi there! How may I help you?", "Hello! How can I assist you?"]

if st.button('Start Chat'):
    if 'assisstant' not in st.session_state:
        num = random.randint(0, 1)
        st.session_state['assisstant'] = [Start_conversation[num]]
    if 'user' not in st.session_state:
        st.session_state['user'] = [""]

input_container = st.container()
response_container = st.container()
user_input = ""
chatbot = hugchat.ChatBot(cookie_path="cookies.json")

def get_input():
    styl = f"""
            <style>
                .stTextInput {{
                position: fixed;
                bottom: 3rem;
                }}
            </style>
            """
    st.markdown(styl, unsafe_allow_html=True)
    input_text = st.text_input("Enter text : ", "", key=input)
    return input_text

def generate_response(prompt):
    response = chatbot.chat(prompt)
    return response

def display_message(msg, author):
    if author == 'assisstant':
        st.markdown(
            f"""
            <div style="display: flex; align-items: flex-end;">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzcTIKR7kAkhiedvVHIhDzUJD1CDBKbfGnEA&usqp=CAU" alt="User Avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; margin-bottom: 20px;">
                <div style="background-color: black; border-radius: 5px; padding: 10px; margin-bottom: 20px">
                    {msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="display: flex; align-items: flex-end; justify-content: flex-end;">
                <div style="background-color: black; border-radius: 5px; padding: 10px; margin-bottom: 20px">
                    {msg}
                </div>
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLO-twChKTxu7ZNEYI00dH7nv7nOH-8lOcag&usqp=CAU" alt="Bot Avatar" style="width: 40px; height: 40px; border-radius: 50%; margin-left: 10px; margin-bottom: 20px;">
            </div>
            """,
            unsafe_allow_html=True
        )

with input_container:
    user_input = get_input()

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.user.append(user_input)
        st.session_state.assisstant.append(response)
        
    if 'assisstant' in st.session_state and st.session_state['assisstant']:
        for i in range(len(st.session_state['assisstant'])):
            if i != 0:
                display_message(st.session_state['user'][i], 'user')
            display_message(st.session_state['assisstant'][i], 'assisstant')
