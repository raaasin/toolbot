import streamlit as st
from creds import key

import google.generativeai as genai
genai.configure(api_key=key)

st.title("Machine Recommendation Tool")

st.header("Let's find the perfect drill for you!")
def get_message(message):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(message, stream=True)
    response.resolve()
    return response

with st.form("drill_questions"):
    material = st.text_input("What material will you be drilling into (e.g., wood, metal, concrete)?")
    hole_size = st.number_input("What size holes do you need to drill (in millimeters)?")
    corded_or_cordless = st.radio("Do you prefer a corded or cordless drill?", ("Corded", "Cordless"))
    budget = st.slider("What is your budget range?", min_value=50, max_value=500, step=50)
    submit_button = st.form_submit_button("Submit")

if submit_button:
    st.write("**Reviewing your answers...**")
    st.write(f"Material: {material}")
    st.write(f"Hole size: {hole_size} mm")
    st.write(f"Corded/cordless: {corded_or_cordless}")
    st.write(f"Budget: ${budget}")

    st.write("**Based on your needs, here are some recommended drills:**")

    message = f"Provide a tool for this Material: {material}\nHole size: {hole_size} mm\nCorded/cordless: {corded_or_cordless}\nBudget: ${budget}"
    answer = get_message(message)

    for chunk in answer:
       st.write(chunk.text)
