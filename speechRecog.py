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
#print(r.recognize_google())
harvard = sr.AudioFile('.\\Audios_denuncias\\audio_files_harvard.wav')
with harvard as source:
  audio = r.record(source)

#print(type(audio))
print(r.recognize_google(audio))#imprime audio a texto

