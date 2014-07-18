"
Greg Kinman - B48856
Freescale Semiconductor, Inc.

text_processor.R

Processes web-scraped text.
"

setwd("c:/users/b48856/documents/sentiment_analysis/phase_3")

library(tm)

main <- function() {
    
    "
    Driver function for text processing.
    "
    
    test_data <- processor("test_text.csv")
    
}

processor <- function(csv_filename) {
    
    "
    Stems and removes stopwords from the text of the first column of a .csv file.

    Input:
    1. csv_filename:    a string: the name of the tab-delimited .csv file that contains the data

    Output:
    1. final_data:      a data frame: a data frame containing the processed text data and its metadata
    "
    
    # Loads the file data into a data frame.
    original_data <- read.csv(csv_filename)
    
    # Pulls just the text column (the leftmost column) and stems and removes stopwords.
    just_text <- original_data[,1]
    text_corpus <- Corpus(DataframeSource(data.frame(just_text)))
    stemmed_text <- tm_map(text_corpus, stemDocument, language="english")
    
    removed_text <- tm_map(stemmed_text, removeWords, stopwords("english"))
    corpus_dict <- as.character(text_corpus)
    print(corpus_dict)
    new_text <- tm_map(removed_text, stemCompletion, dictionary=corpus_dict)
    #new_text <- tm_map(stemmed_text, removeWords, stopwords("english"))
    
    # Replaces the leftmost column in the original data frame with the processed text.
    metadata <- original_data[,-1]
    new_text_frame <- t(as.data.frame(new_text))
    final_data <- data.frame(new_text_frame, metadata)
    
    return(final_data)
    
}

main()
