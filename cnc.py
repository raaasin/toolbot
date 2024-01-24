import streamlit as st
import time
import google.generativeai as genai

genai.configure(api_key="AIzaSyDWflxCyU3_pSzXjW-k91I9G6mvzUQ2q2U")  
cnc_name = ""
material = ""
operation = ""
additional_criteria = ""
answer1=""
answer=""

# Set Streamlit page configurations
st.set_page_config(
    page_title="CNC Selection Guide",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)
def get_message(message):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(message, stream=True)
    response.resolve()
    return response

# Custom CSS for light mode
st.markdown(
    """
    <style>
        body {
            color: #000000;
            background-color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for 'page'
if 'page' not in st.session_state:
    st.session_state.page = 0

# Function to handle page navigation
def next_page():
    st.session_state.page += 1

# Page 1: CNC Name
if st.session_state.page == 0:
    st.title("CNC Selection Guide")
    cnc_name = st.text_input("Name of the CNCs where you plan to use it?")
    if st.button("Next"):
        next_page()

# Page 2: Material
elif st.session_state.page == 1:
    material = st.text_input("What is the main material for the operation? (e.g., steel, aluminum, plastic)")
    if st.button("Next"):
        next_page()

# Page 3: Operation
elif st.session_state.page == 2:
    operation = st.text_input("What kind of operation do you want to use it for? (e.g., Milling, Drilling)")
    if st.button("Next"):
        next_page()

# Page 4: Additional Criteria
elif st.session_state.page == 3:
    additional_criteria = st.text_input("Any additional criteria that are important to you? (e.g., budget, timeline)")
    if st.button("Next"):
        next_page()

# Page 5: Answer
elif st.session_state.page == 4:
    st.title("Thanks for your input :)")
    message = f"i want to use it at {cnc_name} for this Material: {material} for this operation ${operation}, with additional criteria ${additional_criteria} just provide the name of the cnc thats it nothing else please"
    st.write("Processing... Please wait.")
    
    with st.spinner("Finding the best tool for you..."):
        answer = get_message(message)
    st.write("Done!")
    if st.button("Next"):
        next_page()


# Page 6: Recommendation
elif st.session_state.page == 5:
    st.title("Recommendation")
    
    st.write("Based on your input, here's a potential recommendation:")
    for chunk in answer:
        st.markdown(f"<p style='font-size:16px;'>{chunk.text}</p>", unsafe_allow_html=True)

    st.write("**Important considerations:")
    message1 = f"Can you provide important considerations for {answer}"
    answer1 = get_message(message1)

    for chunk in answer1:
        st.markdown(f"<p style='font-size:16px;'>{chunk.text}</p>", unsafe_allow_html=True)

st.write("---")  # Separator for scrolling
