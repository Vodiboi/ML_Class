# convert corpus of shakespeare into single file
import os

files = os.listdir("shakespeare-dataset/text/")

txt = []
for f in files:
    with open(f"shakespeare-dataset/text/{f}", "r") as a:
        txt.append(a.read())

txt = "".join(txt)


def readWordsFromText(blob):
    '''
    ignores fancy characters
    '''
    replaced = "".join([(i.lower() if ("A" <= i and i <= "Z") or ("a" <= i and i <= "z") else " ") for i in blob ])
    words = set(replaced.split())
    return words

words = readWordsFromText(txt)
print(len(words))
words = sorted(words)
with open("shakespeare.txt", "w") as f:
    print(*words, file=f, sep="\n")