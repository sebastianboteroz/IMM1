import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Convierte de Texto a Audio")
image = Image.open('tomyjerry.jpg')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Esrcibe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '  
         ' Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. ' 
         ' Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '  
         ' la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. ' 
         '  '
         ' Franz Kafka.'
        )

# Mensaje llamativo estilizado
st.markdown(
    """
    <div style="background-color: #F0EDFF; border-left: 5px solid #6C5CE7; padding: 12px 16px; border-radius: 6px; margin-top: 15px; margin-bottom: 15px;">
        <span style="font-size: 18px; font-weight: bold; color: #2D3436;">
            🎧 ¿Quieres escucharlo en voz alta?
        </span>
        <p style="margin: 4px 0 0 0; color: #000000; font-size: 14px;">
            Copia el texto de arriba y pégalo en el recuadro a continuación.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

text = st.text_area("Ingrese El texto a escuchar.")

tld='com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang=="Español" :
    lg='es'
if option_lang=="English" :
    lg='en'

def text_to_speech(text, tld,lg):
    tts = gTTS(text,lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

# CSS para cambiar el color del botón a morado
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: #6C5CE7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #5A49E0;
        color: white;
    }
    div.stButton > button:focus {
        background-color: #6C5CE7;
        color: white;
        box-shadow: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Convertir a Audio"):
     result, output_text = text_to_speech(text, 'com',lg)
     audio_file = open(f"temp/{result}.mp3", "rb")
     audio_bytes = audio_file.read()
     st.markdown(f"## Tú audio:")
     st.audio(audio_bytes, format="audio/mp3", start_time=0)

     with open(f"temp/{result}.mp3", "rb") as f:
         data = f.read()

     def get_binary_file_downloader_html(bin_file, file_label='File'):
         bin_str = base64.b64encode(data).decode()
         href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
         return href
     st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
