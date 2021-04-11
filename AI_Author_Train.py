########################
######  AthenaAI  ######
######    2021    ######
########################

import gpt_2_simple as gpt2
import os
import requests

"""
It will download a machine learning model, the model is like an empty brain you can train on,
one thing to note is every time you want to train on a new author, you will need to create a new folder,
then put this AI_Author_Train.py script in it and run the script to re-download the model,
because you can't use Nietzsche's brain to train on Shakespeare isn't it, you need a new and empty model.
"""
model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
    print(f"Downloading {model_name} model...")
    gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

author_path = "Authors/"
file_name = "shakespeare.txt"  # Name of the book you want to train.
file = author_path + file_name

sess = gpt2.start_tf_sess()
gpt2.finetune(sess, file, model_name=model_name, steps=1500)   # steps is max number of training steps

gpt2.generate(sess)