import pickle
with open("dump", "rb") as f:
    slt = pickle.load(f)
print(slt)
