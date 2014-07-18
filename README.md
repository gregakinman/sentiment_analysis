Sentiment Analysis
===

This is the code for the sentiment analysis project at Freescale. It is maintained by [Greg Kinman](mailto:gregory.kinman@freescale.com). There are three "phases" in the project pipeline:

- Phase 1: scraping the web for text data. Feel free to change the search keywords for scraping to search for buzz about different terms.
- Phase 2: labeling the data with sentiment.
- Phase 3: analyzing the labeled data for patterns and EBI insight. Note that this phase is still under construction.

The subdirectories are titled accordingly.

NOTE:
---

Numerous files are left out (check the .gitignore for more details). The most important and notable of these exclusions is the Stanford CoreNLP software. You will need to separately download the CoreNLP software and place it in the sentiment_analysis/phase_2 directory. Also, some of the filepaths used in commands in this software need to match the version of the CoreNLP software installed. The current supported version is version 3.4, released June 16th, 2014. Either make sure the commands match, or only use version 3.4 of the software. The release history of the software can be found [here](http://nlp.stanford.edu/software/corenlp.shtml#History). The up-to-date repository for the software can be found [here](https://github.com/stanfordnlp/CoreNLP).
