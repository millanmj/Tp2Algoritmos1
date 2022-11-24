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

 denuncia_1:str = audio_a_texto(".\\Audios_denuncias\\denuncia1.wav")
 print(denuncia_1)
 denuncia_2:str = audio_a_texto(".\\Audios_denuncias\\denuncia2.wav")
 print(denuncia_2)
 denuncia_3:str =audio_a_texto(".\\Audios_denuncias\\denuncia3.wav")
 print(denuncia_3)
 denuncia_4:str = audio_a_texto(".\\Audios_denuncias\\denuncia4.wav")
 print(denuncia_4)
 denuncia_5:str = audio_a_texto(".\\Audios_denuncias\\denuncia5.wav")
 print(denuncia_5)
 denuncia_6:str = audio_a_texto(".\\Audios_denuncias\\denuncia6.wav")
 print(denuncia_6)
 denuncia_7:str = audio_a_texto(".\\Audios_denuncias\\denuncia7.wav")
 print(denuncia_7)
 denuncia_8:str = audio_a_texto(".\\Audios_denuncias\\denuncia8.wav")
 print(denuncia_8)
 denuncia_9:str = audio_a_texto(".\\Audios_denuncias\\denuncia9.wav")
 print(denuncia_9)
 denuncia_10:str = audio_a_texto(".\\Audios_denuncias\\denuncia10.wav")
 print(denuncia_10)
 denuncia_11:str = audio_a_texto(".\\Audios_denuncias\\denuncia11.wav")
 print(denuncia_11)
 denuncia_12:str = audio_a_texto(".\\Audios_denuncias\\denuncia12.wav")
 print(denuncia_12)






main()