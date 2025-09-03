# clean the code for trump speeches
import json

with open("Trump_Labeled_Combined_Rev_Speeches_Final_9-24-2024.json", "r") as f:
    a = json.load(f)
with open("trump_speeches.txt", "w") as f:
    for i in range(len(a["transcript"])):
        print(a["transcript"][str(i)], file=f)
