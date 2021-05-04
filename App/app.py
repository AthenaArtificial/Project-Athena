import tensorflow as tf
import gpt_2_simple as gpt2
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


@app.route("/harry_potter")
def harry_potter_route():
    return render_template('harry_potter.html')


@app.route("/katniss_everdeen")
def katniss_everdeen_route():
    return render_template('katniss_everdeen.html')


@app.route("/load_plato")
def load_plato():
    load_character("Plato")
    return render_template('plato.html')


@app.route("/load_harry")
def load_harry_potter():
    load_character("Harry_Potter")
    return render_template('harry_potter.html')


@app.route("/load_katniss")
def load_katniss_everdeen():
    load_character("Katniss_Everdeen")
    return render_template('katniss_everdeen.html')


def load_character(character: str):
    tts_engine = pyttsx3.init()
    plato_chatbot = ChatBot()

    """Speech to text"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = recognizer.listen(source)
        inp = recognizer.recognize_google(audio)
        print(f"You said : {inp}")
        chatbot_response = plato_chatbot.chat(inp)
        print(chatbot_response)
        if chatbot_response:
            tts_engine.say(chatbot_response)
            tts_engine.runAndWait()
        else:
            tf.reset_default_graph()
            # tf.reset_default_graph()
            sess = gpt2.start_tf_sess()
            gpt2.load_gpt2(sess, checkpoint_dir=f"{character}/checkpoint")
            answers = gpt2.generate(sess, length=100, include_prefix=False, temperature=0.1, top_k=1, top_p=0.9,
                                    model_dir=f"{character}/models", sample_dir=f"{character}/samples",
                                    checkpoint_dir=f"{character}/checkpoint",
                                    run_name='run1', prefix=inp, return_as_list=True)
            answer_to_say = answers[0]
            print(answer_to_say)
            tts_engine.say(answer_to_say)
            tts_engine.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)