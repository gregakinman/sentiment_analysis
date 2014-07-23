"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

snippet_labeler.py

Labels the text snippets with their sentiment values.
"""

import csv, subprocess, pdb, os, run_core_nlp
from bs4 import BeautifulSoup as BS
from nltk.tokenize.punkt import PunktSentenceTokenizer as ST

def main():

    """
    Operates on a .csv file in the current directory that contains sentences with commas removed, as well as other
    labeled data items about those sentences. Creates a new .csv file that has the sentiment values appended to the
    original data (i.e., in a new rightmost column).
    """

    # Gets the input and output filenames from the user and asks to proceed.
    print "\nPlease enter the name of the input .csv file:\n"
    input_filename = raw_input()
    print "\nOkay, now please enter the desired output .csv filename:\n"
    output_filename = raw_input()
    print "\nThanks! The file will be passed to the CoreNLP software.\nThe output .csv file will be placed in the current directory.\n"

    # Gets just the text snippets from the input .csv file and puts them into .txt files to be passed to CoreNLP.
    filenames = csv_to_txt(input_filename)
    print "\nThe text data is prepared to be passed to CoreNLP. There's about to be a lot of console output; ignore it. Type c and hit enter/return to continue.\n"
    pdb.set_trace()

    # Runs CoreNLP.
    run_core_nlp.main()

    # Parses NLP's .xml output to label the sentences.
    xml_to_csv(filenames, input_filename, output_filename)

def csv_to_txt(input_filename):

    """
    Turns the snippets in the .csv file into a form that's easily passable to CoreNLP.

    Input:
    1. input_filename:      str: the name of the .csv file that contains the text data.

    Output:
    1. filenames:           list of strs: the paths to the files containing the text snippets
    """

    # Pulls the text snippets out of the .csv file into a data structure.
    snippets = []
    with open(input_filename, "rb") as f:
        file_reader = csv.reader(f)
        tokenizer = ST()
        for row in file_reader:
            subsnippet = row[0]
            subsnippets = tokenizer.tokenize(subsnippet)
            snippets.append(subsnippets)

    # Makes a dump folder.
    subdirectory = "snippet_files"
    try:
        os.mkdir(subdirectory)
    except Exception:
        pass

    # Dumps the text to files in the dump folder.
    counter = 1
    filenames = []
    for snippet in snippets:
        filename = "snippet_file_" + str(counter) + ".txt"
        filepath = os.path.join(subdirectory, filename)
        filenames.append(filepath)
        with open(filepath, "wb") as f:
            for sentence in snippet:
                f.write(sentence + "\n")
        counter += 1

    # Assembles the list of filepaths so CoreNLP knows where to look.
    with open("filenames.txt", "wb") as f:
        for filepath in filenames:
            f.write(filepath + "\n")

    return filenames

def xml_to_csv(filenames, input_filename, output_filename):

    """
    Writes the output .csv file given the labeled sentences.

    1. filenames:          str: the filepaths of the files containing the sentences
    2. input_filename:     str: the name of the input .csv file
    3. output_filename:    str: the desired name of the output .csv file
    """

    # Parses the .xml files to get all the sentiment values into a list.
    sentiment_values = []
    for filepath in filenames:
        soup = BS(open(filepath + ".xml", "rb"), "xml")
        xml_sentences = soup.find_all("sentence")
        intermediate_values = []
        for sentence in xml_sentences:
            intermediate_values.append(sentence["sentimentValue"].encode("ascii"))
        concatenated_values = ""
        for value in intermediate_values:
            concatenated_values += value
        sentiment_values.append(concatenated_values)
    sentiment_values = sentiment_values[1:]

    # Creates the output .csv file, appending the sentiment values to it with a new rightmost column.
    with open(input_filename, "rb") as f:
        with open(output_filename, "wb") as g:
            input_reader = csv.reader(f)
            output_writer = csv.writer(g)
            # Adds the new column label to the end of the first row.
            full_file = []
            row = next(input_reader)
            row.append("Sentiment")
            full_file.append(row)
            # Adds the sentiment values to the rightmost column.
            for row, value in zip(input_reader, sentiment_values):
                row.append(value)
                full_file.append(row)
            output_writer.writerows(full_file)

if __name__ == "__main__":
    main()
