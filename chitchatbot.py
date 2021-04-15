########################
######  AthenaAI  ######
######    2021    ######
########################
##### Chitchat Bot #####
########################

import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle


# load stemmer
stemmer = LancasterStemmer()
# open the json training file
with open("intents/intents.json", "r") as file:
    data = json.load(file)

"""Preprocessing"""
try:
    with open("ml_model/data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except FileNotFoundError:
    # stemming words (just cleaning up words to find the roots)
    words = []
    labels = []
    docs_tag = []
    docs_pattern = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            # pattern
            tokenized_words = nltk.word_tokenize(pattern)  # result looks like ['Is', 'anyone', 'there', '?']
            words.extend(tokenized_words)
            docs_pattern.append(tokenized_words)
            docs_tag.append(intent["tag"])
        # tag
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    labels = sorted(labels)
    words = sorted(list(set([stemmer.stem(w.lower()) for w in words if w != "?"])))  # ['ag', 'ar', 'buy', 'cya', 'day']

    training = []
    output = []

    out_zeros = [0] * len(labels)

    for i, doc_ptns in enumerate(docs_pattern):
        bag = []
        stemmed_words = [stemmer.stem(w.lower()) for w in doc_ptns]
        for w in words:
            bag.append(1) if w in stemmed_words else bag.append(0)

        output_row = out_zeros.copy()
        output_row[labels.index(docs_tag[i])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    '''Save point'''
    with open("ml_model/data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)


"""Tensorflow training"""
tf.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])  # Input layer
net = tflearn.fully_connected(net, 8)  # Hidden layer
net = tflearn.fully_connected(net, 8)  # Hidden layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")  # Output layer
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(inp, word_bank):
    bag = [0] * len(word_bank)

    inp_words = nltk.word_tokenize(inp)
    inp_words = [stemmer.stem(w.lower()) for w in inp_words]

    for x in inp_words:
        for i, w in enumerate(word_bank):
            if w == x:
                bag[i] = 1

    return np.array(bag)


def chat():
    while True:
        inp = input("You: ")
        if inp.lower() == "q":
            break

        results = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(results)
        tag = labels[result_index]

        if results[result_index] > 0.8:
            for t in data["intents"]:
                if t["tag"] == tag:
                    response = random.choice(t["responses"])
                    print(response)
        else:
            print("here plug in the GPT 2")


if __name__ == '__main__':
    chat()