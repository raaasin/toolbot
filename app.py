import streamlit as st
import google.generativeai as genai
#Gemini API key
genai.configure(api_key="AIzaSyDWflxCyU3_pSzXjW-k91I9G6mvzUQ2q2U")

st.set_page_config(layout="wide")
st.title("Tool Recommendation Tool")

tool_type = st.sidebar.selectbox("Select Tool Type", ("Drill", "Saw", "Grinder", "Other"))

if tool_type == "Drill":
    st.header("Let's find the perfect drill for you!")
    question_text = "What material will you be drilling into (e.g., wood, metal, concrete)?"
    tool_text = "Drill"
elif tool_type == "Saw":
    st.header("Let's find the perfect saw for you!")
    question_text = "What material will you be cutting (e.g., wood, metal, plastic)?"
    tool_text = "Saw"
elif tool_type == "Grinder":
    st.header("Let's find the perfect grinder for you!")
    question_text = "What material will you be grinding (e.g., metal, stone, concrete)?"
    tool_text = "Grinder"
else:
    st.header("Let's find the perfect tool for you!")
    question_text = "What kind of tool are you looking for?"
    tool_text = "Tool"

def get_message(message):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(message, stream=True)
    response.resolve()
    return response

with st.form("tool_questions"):
    material = st.text_input(question_text)
    if tool_type != "Tool":
        hole_size = st.number_input("What size holes do you need to drill (in millimeters)?")
        corded_or_cordless = st.radio("Do you prefer a corded or cordless tool?", ("Corded", "Cordless"))
    budget = st.slider("What is your budget range?", min_value=50, max_value=500, step=50)
    submit_button = st.form_submit_button("Submit")

if submit_button:
    st.write("**Reviewing your answers...**")
    st.write(f"Material: {material}")
    if tool_type != "Tool":
        st.write(f"Hole size: {hole_size} mm")
        st.write(f"Corded/cordless: {corded_or_cordless}")
    st.write(f"Budget: ${budget}")

    st.write(f"**Based on your needs, here are some recommended {tool_text}s:**")

    if tool_type != "Tool":
        message = f"Provide a {tool_text.lower()} for this Material: {material}\nHole size: {hole_size} mm\nCorded/cordless: {corded_or_cordless}\nBudget: ${budget}"
    else:
        message = f"which tool should i buy and what model? for this requirements: {material}\nBudget: ${budget}"

    answer = get_message(message)

    for chunk in answer:
        st.markdown(f"<p style='font-size:16px;'>{chunk.text}</p>", unsafe_allow_html=True)
       