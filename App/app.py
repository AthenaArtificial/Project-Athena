from flask import Flask, render_template
from chitchatbot_Plato import ChatBot
import speech_recognition as sr
import pyttsx3

tts_engine = pyttsx3.init()
app = Flask(__name__, static_folder='./static', template_folder='./templates')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/plato")
def plato_route():
    return render_template('plato.html')


@app.route("/load_plato")
def load_plato():
    plato_chatbot = ChatBot()
    plato_gpt = GPTPlato()

    """Speech to text"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = recognizer.listen(source)
        try:
            inp = recognizer.recognize_google(audio)
            print(f"You said : {inp}")
            chatbot_response = plato_chatbot.chat(inp)
            print("Response:", chatbot_response)
            if chatbot_response:
                tts_engine.say(chatbot_response)
                tts_engine.runAndWait()
            else:
                plato_gpt.generate(inp)
        except:
            tts_engine.say("Sorry could not recognize what you said")
            tts_engine.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)
