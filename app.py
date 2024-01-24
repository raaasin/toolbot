import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyDWflxCyU3_pSzXjW-k91I9G6mvzUQ2q2U")  

st.set_page_config(layout="wide")
st.title("CNC Machine Recommendation Tool")
#machine types def
cnc_machine_type = st.sidebar.selectbox("Select CNC Machine Type", (
    "Mill",
    "Lathe",
    "Router",
    "Plasma Cutter",
    "Waterjet Cutter",
    "Laser Cutter",
    "3D Printer",
    "Wire EDM",
    "Sinker EDM",
    "Turn-Mill",
    "Other"
))

if cnc_machine_type == "Mill":
    st.header("Let's find the perfect mill for you!")
    question_text = "What materials will you be milling (e.g., aluminum, steel, wood)?"
    machine_text = "Mill"
elif cnc_machine_type == "Lathe":
    st.header("Let's find the perfect lathe for you!")
    question_text = "What materials will you be turning (e.g., aluminum, steel, wood)?"
    machine_text = "Lathe"
elif cnc_machine_type == "Router":
    st.header("Let's find the perfect router for you!")
    question_text = "What materials will you be routing (e.g., wood, plastic, aluminum)?"
    machine_text = "Router"
elif cnc_machine_type == "Plasma Cutter":
    st.header("Let's find the perfect plasma cutter for you!")
    question_text = "What materials will you be cutting with the plasma cutter?"
    machine_text = "Plasma Cutter"
elif cnc_machine_type == "Waterjet Cutter":
    st.header("Let's find the perfect waterjet cutter for you!")
    question_text = "What materials will you be cutting with the waterjet cutter?"
    machine_text = "Waterjet Cutter"
elif cnc_machine_type == "Laser Cutter":
    st.header("Let's find the perfect laser cutter for you!")
    question_text = "What materials will you be cutting with the laser cutter?"
    machine_text = "Laser Cutter"
elif cnc_machine_type == "3D Printer":
    st.header("Let's find the perfect 3D printer for you!")
    question_text = "What materials will you be using with the 3D printer?"
    machine_text = "3D Printer"
elif cnc_machine_type == "Wire EDM":
    st.header("Let's find the perfect wire EDM machine for you!")
    question_text = "What materials will you be using with the wire EDM machine?"
    machine_text = "Wire EDM"
elif cnc_machine_type == "Sinker EDM":
    st.header("Let's find the perfect sinker EDM machine for you!")
    question_text = "What materials will you be using with the sinker EDM machine?"
    machine_text = "Sinker EDM"
elif cnc_machine_type == "Turn-Mill":
    st.header("Let's find the perfect turn-mill machine for you!")
    question_text = "What materials will you be using with the turn-mill machine?"
    machine_text = "Turn-Mill"
elif cnc_machine_type == "Other":
    st.header("Let's find the perfect machine for you!")
    question_text = "What specific machine type are you looking for?"
    machine_text = "Other"


with st.form("cnc_questions"):
    material = st.text_input(question_text)
    
    if cnc_machine_type in ["Mill", "Lathe", "Router"]:
        workpiece_size = st.text_input("What are the dimensions of your workpiece?")
        precision = st.selectbox("What level of precision do you require?", ["High", "Medium", "Low"])
    
    elif cnc_machine_type == "Plasma Cutter":
        cutting_thickness = st.number_input("What thickness of material will you cut?")
        gas_type = st.selectbox("What type of gas will you use?", ["Oxygen", "Nitrogen", "Air"])
    
    elif cnc_machine_type == "Waterjet Cutter":
        abrasive_type = st.selectbox("What type of abrasive will you use?", ["Garnet", "Aluminum Oxide", "Other"])
        waterjet_power = st.slider("Select the waterjet power", min_value=50, max_value=500, step=50)
    
    elif cnc_machine_type == "Laser Cutter":
        laser_power = st.slider("Select the laser power", min_value=20, max_value=200, step=10)
        cutting_material = st.multiselect("What materials will you cut?", ["Wood", "Acrylic", "Metal", "Other"])
    
    elif cnc_machine_type == "3D Printer":
        printing_technology = st.selectbox("Select printing technology", ["FDM", "SLA", "SLS", "DLP", "Other"])
        printing_material = st.multiselect("What materials will you use for printing?", ["PLA", "ABS", "Resin", "Other"])
    
    elif cnc_machine_type == "Wire EDM":
        edm_material = st.text_input("What material will you be working with?")
        edm_tolerance = st.number_input("What level of tolerance do you need?")
    
    elif cnc_machine_type == "Sinker EDM":
        sinker_material = st.text_input("What material will you be using with the sinker EDM machine?")
        sinker_depth = st.number_input("What maximum depth will you be working on?")
    
    elif cnc_machine_type == "Turn-Mill":
        turnmill_operations = st.multiselect("What operations will you perform?", ["Turning", "Milling", "Drilling", "Other"])
        turnmill_material = st.text_input("What material will you be working with?")
    
    elif cnc_machine_type == "Other":
        other_specifics = st.text_area("Please specify any additional details or specific requirements.")
    
    budget = st.slider("What is your budget range?", min_value=5000, max_value=500000, step=5000)
    submit_button = st.form_submit_button("Submit")

def get_message(message):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(message, stream=True)
    response.resolve()
    return response

if submit_button:
    st.write("**Reviewing your answers...**")
    st.write(f"Material: {material}")
    st.write(f"Budget: ${budget}")

    st.write(f"**Based on your needs, here are some recommended {machine_text}s:**")

    message = f"Provide a CNC {machine_text.lower()} for this Material: {material}\nBudget: ${budget}"  

    answer = get_message(message)  

    for chunk in answer:
        st.markdown(f"<p style='font-size:16px;'>{chunk.text}</p>", unsafe_allow_html=True)

