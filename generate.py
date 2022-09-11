import argparse
import pickle
from model import Model


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str)
parser.add_argument('--prefix', type=str, default="")
parser.add_argument('--length', type=int)
params = parser.parse_args()


prefix = params.prefix.split(" ")
if (params.prefix == ""):
    prefix = []
n = params.length

with open(params.model, "rb") as f:
    model : Model() = pickle.load(f)

print(*model.generate(prefix, n))