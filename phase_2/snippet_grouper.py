"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

snippet_grouper.py

Groups snippets by sentiment score for group analysis.
"""

import csv, pdb
from nltk.tokenize.punkt import PunktSentenceTokenizer as ST

def main():

    """
    Main function.
    """

    print "\nPlease name the .csv file in which the text data resides:\n"
    csv_filename = raw_input()
    print "\nThanks! The text will be placed, sentence by sentence, into filenames of form value_#.csv. Hit 'c' and enter/return to continue.\n"
    pdb.set_trace()

    grouper(csv_filename)

def grouper(csv_filename):

    """
    Groups text snippets into their sentiment score classes.

    Input:
    1. csv_filename:    str: the name of the .csv file in which the text data resides.
    """

    groups = {0: [], 1: [], 2: [], 3: [], 4: []}

    with open(csv_filename, "rb") as f:
        csv_reader = csv.reader(f)
        tokenizer = ST()
        counter = 0
        # Tokenizes each row and splits up the tokens into groups.
        for row in csv_reader:
            if counter == 0:
                counter += 1
                continue
            sentiments = str(row[-1])
            snippets = tokenizer.tokenize(row[0])
            for i in range(len(sentiments)):
                groups[int(sentiments[i])].append(snippets[i])

    # Writes the new groups to their own separate groups.
    score_classes = {}
    for group in groups:
        if groups[group]:
            score_classes[group] = groups[group]
    for score in score_classes:
        with open("value_" + str(score) + ".csv", "wb") as f:
            writer = csv.writer(f)
            for snippet in score_classes[score]:
                writer.writerow([snippet])

if __name__ == "__main__":
    main()
