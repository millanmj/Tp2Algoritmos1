#speech recognition
#pip install SpeechRecognition
#pip install PyAudio
import speech_recognition as sr
r = sr.Recognizer()
"""
Dado que SpeechRecognition se envía con una clave de API predeterminada
para Google Web Speech API, puede comenzar a usarla de inmediato. Por este 
motivo, utilizaremos la Web Speech API en este tp.
"""

def audio_a_texto (ruta_archivo:str):
  prueba = sr.AudioFile(ruta_archivo)
  with prueba as source:
    audio = r.record(source)
  denuncia = (r.recognize_google(audio,language='es-ES'))
  return denuncia


def main():

 denuncia_1 = audio_a_texto(".\\Audios_denuncias\\denuncia1.wav")
 print(denuncia_1)

main()