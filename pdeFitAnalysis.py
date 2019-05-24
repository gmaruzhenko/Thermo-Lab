import pickle
import numpy as np

with open("PDE_fit_results.pickle", 'rb') as f:
    results = pickle.load(f)

print(results)