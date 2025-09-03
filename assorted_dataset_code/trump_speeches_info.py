# some info for trump speeches
with open("speeches.txt", "r") as f:
    data = f.read()

data = data.replace(" ", "")

print(len(data), len(data.split()))