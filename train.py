import argparse
import pickle
from model import Model
import os

parser = argparse.ArgumentParser()
parser.add_argument('--input-dir', type=str, default="")
parser.add_argument('--model', type=str)
params = parser.parse_args()
model = Model()

if (params.input_dir == ""):
    text = input()
    model.teach(text)
else :
    with os.scandir(params.input_dir) as files:
        for file in files:
            name = params.input_dir + "/" + file.name
            with open(name, "r", encoding='utf-8') as f:
                s = f.read()
                model.teach(s)


# print(model.ngram)


with open(params.model, "wb") as f:
    pickle.dump(model, f)
