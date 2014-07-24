"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

.py


"""

import csv
from nltk.tokenize.punkt import PunktSentenceTokenizer as ST

csv_filename = raw_input()

groups = {0: [], 1: [], 2: [], 3: [], 4: []}

with open(csv_filename, "rb") as f:
    csv_reader = csv.reader(f)
    tokenizer = ST()
    counter = 0
    for row in csv_reader:
        if counter == 0:
            counter += 1
            continue
        sentiments = str(row[-1])
        snippets = tokenizer.tokenize(row[0])
        for i in range(len(sentiments)):
            groups[int(sentiments[i])].append(snippets[i])

score_classes = {}
for group in groups:
    if groups[group]:
        score_classes[group] = groups[group]

for score in score_classes:
    with open("value_" + str(score) + ".csv", "wb") as f:
        writer = csv.writer(f)
        for snippet in score_classes[score]:
            writer.writerow([snippet])
