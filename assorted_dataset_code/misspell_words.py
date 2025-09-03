# fake typos on words based on keyboard positioning
from random import shuffle, choice
# dict written by gpt:
keyboard_adj_list_letters = {
    'q': ['w', 'a'],
    'w': ['q', 'e', 'a', 's'],
    'e': ['w', 'r', 's', 'd'],
    'r': ['e', 't', 'd', 'f'],
    't': ['r', 'y', 'f', 'g'],
    'y': ['t', 'u', 'g', 'h'],
    'u': ['y', 'i', 'h', 'j'],
    'i': ['u', 'o', 'j', 'k'],
    'o': ['i', 'p', 'k', 'l'],
    'p': ['o', 'l'],

    'a': ['q', 'w', 's', 'z'],
    's': ['w', 'e', 'a', 'd', 'z', 'x'],
    'd': ['e', 'r', 's', 'f', 'x', 'c'],
    'f': ['r', 't', 'd', 'g', 'c', 'v'],
    'g': ['t', 'y', 'f', 'h', 'v', 'b'],
    'h': ['y', 'u', 'g', 'j', 'b', 'n'],
    'j': ['u', 'i', 'h', 'k', 'n', 'm'],
    'k': ['i', 'o', 'j', 'l', 'm'],
    'l': ['o', 'p', 'k'],

    'z': ['a', 's', 'x'],
    'x': ['s', 'd', 'z', 'c'],
    'c': ['d', 'f', 'x', 'v'],
    'v': ['f', 'g', 'c', 'b'],
    'b': ['g', 'h', 'v', 'n'],
    'n': ['h', 'j', 'b', 'm'],
    'm': ['j', 'k', 'n']
}


with open("unigram_freq.csv", "r") as f:
    lines = f.read().splitlines()[1:30000]

words, counts = zip(*[i.split(",") for i in lines])
print(words[:5], counts[:5])

w2 = []
for i in range(len(words)):
    # make 2 misspelled versions of this word
    indicies = list(range(len(words[i])))
    for j in indicies[:choice([2, 3, 3, 3])]:
        w = list(words[i])
        nearby = choice(keyboard_adj_list_letters[w[j]])
        w[j] = nearby
        w2.append("".join(w))
with open("misspelled_wprds.txt", "w") as f:
    print(*w2, file=f, sep="\n")

