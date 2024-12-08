import streamlit as st
import base64
import gspread
from google.oauth2.service_account import Credentials
import random


# Función para cargar la imagen y convertirla a Base64
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Ruta de tu imagen
image_path = "/Users/cesarperez/Desktop/Life/Python Projects/amigosecreto/pythonProject1/background.JPEG"
image_base64 = get_base64_image(image_path)

# CSS para el fondo
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.8); /* Fondo semi-transparente para la barra lateral */
}}

/* Style input boxes */
input[type="text"], textarea {{
    background: white !important; /* Make the background white */
    color: black !important; /* Font color inside the input fields */
    border: 2px solid #cccccc !important; /* Add a subtle border */
    padding: 10px !important; /* Add padding for better spacing */
    font-size: 16px !important; /* Increase font size */
    border-radius: 5px !important; /* Rounded corners */
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow */
}}

[data-testid="stAppViewContainer"] label {{
    font-size: 80px !important; /* Force font size */
    font-weight: 700 !important; /* Use numeric weight for bold */
    color: white !important;
    line-height: 1.2 !important; /* Adjust spacing for readability */
}}

/* Optional: Override any inline styles applied to labels */
label {{
    all: unset; /* Reset inline styles */
    font-size: 80px !important;
    font-weight: 900 !important;
    color: black !important;
    line-height: 1.2 !important;
}}
</style>
"""

# Aplicar el CSS
st.markdown(page_bg, unsafe_allow_html=True)

# Google Sheets setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SERVICE_ACCOUNT_FILE = "/Users/cesarperez/Desktop/amigosecreto app/amigo-secreto-111-0ab2a59d84ac.json"

# Authorize and connect to Google Sheets
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPE
)
client = gspread.authorize(credentials)

# Open the Google Sheet by name
SHEET_NAME = "amigoDB"  # Replace with your sheet name
sheet = client.open(SHEET_NAME).sheet1  # Use the first sheet

# Title and description
st.title("O melhor AMIGO SECRETO da historia mundial")
st.text("Seja bemvindo ao melhor amigo secreto. ")
st.text("Deixa aqui o teu nome, os 3 desejos e o teu e-mail para saber quem vai ser o teu secret friend.")

# Input Form
name = st.text_input("Nombre", placeholder="Escribe tu nombre")
email = st.text_input("Email", placeholder="Escribe tu email")
wishes = st.text_area("Desejos", placeholder="Escribe un mensaje o tus ideas de regalo")

# Submit Button
if st.button("Enviar"):
    if name and email and wishes:
        # Add the participant's data to the Google Sheet
        sheet.append_row([name, email, wishes])
        st.success(f"Obrigado, {name}! Sua inscrição foi registrada.")
    else:
        st.error("Por favor, preencha todos os campos.")

# Fetch all participants from the Google Sheet
rows = sheet.get_all_records()
st.subheader("Participantes Registrados")
for row in rows:
    st.text(f"🎉 {row['name']} ")

# Perform Matching
if len(rows) >= 6 and st.button("Sortear Amigo Secreto"):
    # Fetch the names from the sheet
    nombres = [row["name"] for row in rows]

    # Shuffle and match participants
    random.shuffle(nombres)
    matches = {}
    for i in range(len(nombres)):
        giver = nombres[i]
        receiver = nombres[(i + 1) % len(nombres)]  # Last person gives to the first
        matches[giver] = receiver

    # Display the matches
    st.subheader("Resultados do Sorteio")
    for giver, receiver in matches.items():
        st.text(f"{giver} 🎁 vai dar um presente para {receiver}")

