import gpt_2_simple as gpt2
import tensorflow as tf
from chitchatbot_Plato import ChatBot
import speech_recognition as sr
import pyttsx3

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
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, checkpoint_dir="Plato/checkpoint")
        answers = gpt2.generate(sess, length=100, include_prefix=False, temperature=0.1, top_k=1, top_p=0.9,
                               model_dir="Plato/models", sample_dir="Plato/samples", checkpoint_dir="Plato/checkpoint",
                               run_name='run1', prefix=inp, return_as_list=True)
        answer_to_say = answers[0]
        print(answer_to_say)
        tts_engine.say(answer_to_say)
        tts_engine.runAndWait()