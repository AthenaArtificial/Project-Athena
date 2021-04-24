import gpt_2_simple as gpt2
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle

tf.reset_default_graph()

def bag_of_words(inp, word_bank, stemmer):
    bag = [0] * len(word_bank)

    inp_words = nltk.word_tokenize(inp)
    inp_words = [stemmer.stem(w.lower()) for w in inp_words]

    for x in inp_words:
        for i, w in enumerate(word_bank):
            if w == x:
                bag[i] = 1

    return np.array(bag)


class ChatBot:
    def __init__(self):
        self.stemmer = LancasterStemmer()
        self.data = None
        self.words = None
        self.labels = None
        self.training = None
        self.output = None
        with open("Plato/intents/intents.json", "r") as file:
            data = json.load(file)
            self.data = data
        with open("Plato/chitchatbot_models/data.pickle", "rb") as f:
            self.words, self.labels, self.training, self.output = pickle.load(f)

        """Tensorflow model"""
        tf.reset_default_graph()
        self.net = tflearn.input_data(shape=[None, len(self.training[0])])  # Input layer
        self.net = tflearn.fully_connected(self.net, 8)  # Hidden layer
        self.net = tflearn.fully_connected(self.net, 8)  # Hidden layer
        self.net = tflearn.fully_connected(self.net, len(self.output[0]), activation="softmax")  # Output layer
        self.net = tflearn.regression(self.net)
        self.model = tflearn.DNN(self.net)
        self.model.load("Plato/chitchatbot_models/model.tflearn")

    def chat(self, inp: str):
        results = self.model.predict([bag_of_words(inp, self.words, self.stemmer)])[0]
        result_index = np.argmax(results)
        tag = self.labels[result_index]

        if results[result_index] > 0.9:
            for t in self.data["intents"]:
                if t["tag"] == tag:
                    response = random.choice(t["responses"])
                    return response
        else:
            return None
