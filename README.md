Sentiment Analysis
===

This is the code for the sentiment analysis project at Freescale. It is maintained by [Greg Kinman](mailto:gregory.kinman@freescale.com). There are two "phases" in the project pipeline.

- Phase 1: scraping the web for text data.
- Phase 2: labeling the data with sentiment.

Code for mining of the labeled data can be found at [this repository](https://github.com/gregkinman-b48856/sentiment_mining).

Usage:
---

`past_scraper.py` is the script for scraping text data from the web from the past up until the present. (A to-do item is to create a scraper that would continually fetch text data, perhaps via a Google Alerts RSS feed or other method). Currently, it includes functions that scrape the online community on element14.com. Those functions could easily be modified to scrape any other Jive-powered community forum. Of course, the search keywords can also be changed to modify the type of text that is extracted. In its current form, the script outputs a `.csv` file in the working directory with text snippets, URL's, and dates of writing. Run it in the command line with `python past_scraper.py`.

`snippet_labeler.py` is the script for labeling the text data with sentiment values using the Stanford software. Make sure that the Stanford software is installed (see note below) and that a `.csv` file with text data in the format outputted by `past_scraper.py` is in the working directory. Run the script on the command line with `python snippet_labeler.py`. It asks for the names of the input and output `.csv` files, and then runs the operations.

After labeling the text data with sentiment values, load the `.csv` file into R and start text mining.

NOTE:
---

Numerous files are left out (check the .gitignore for more details). The most important and notable of these exclusions is the Stanford CoreNLP software. You will need to separately download the CoreNLP software and place it in the sentiment_analysis/phase_2 directory. Also, some of the filepaths used in commands in this software need to match the version of the CoreNLP software installed. The current supported version is version 3.4, released June 16th, 2014. Either make sure the commands match, or only use version 3.4 of the software. The release history of the software can be found [here](http://nlp.stanford.edu/software/corenlp.shtml#History). The up-to-date repository for the software can be found [here](https://github.com/stanfordnlp/CoreNLP).
