########################
######  AthenaAI  ######
######    2021    ######
########################
#### Speech To Text ####
########################

import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak Anything :")
    audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said : {}".format(text))
    except Exception as e:
        print("Sorry could not recognize what you said")