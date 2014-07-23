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
        print "\n" + str(row) + "\n"
        sentiments = str(row[-1])
        print sentiments
        snippets = tokenizer.tokenize(row[0])
        print "\n" + str(snippets) + "\n"
        for i in range(len(sentiments)):
            print i
            groups[int(sentiments[i])].append(snippets[i])

score_classes = {}
for group in groups:
    if groups[group]:
        score_classes[group] = groups[group]

print score_classes
