Sentiment Analysis
===

This is the code for the sentiment analysis project at Freescale. There are two "phases" in the project pipeline.

- Phase 1: scraping the web for text data.
- Phase 2: labeling the data with sentiment and preparing it for analysis.

Code for mining & analysis of the labeled data can be found in [this repository](https://github.com/gregkinman-b48856/sentiment_mining).

Usage:
---

Vendor products like Adobe Social are useful for mining and analyzing large, homogeneous datasets such as those found on Twitter (a one-stop shop for millions of text snippets). This project, however, is focused on mining smaller, more industry-specific, more heterogeneous datasets, such as element14.com, circuitcellar.com, wired.com, etc. This creates an issue: mining these more "boutique" places on the web requires much more overhead than mining a site like Twitter, as there is less data per site, and the data is more difficult to extricate from its surrounding structure. How does one scrape enough data? How does one make sure the data actually concerns customer opinion of Freescale, its products, and its competitors and their products? The answer is by doing more work in creating web scraping software from the bottom up. Web scraping is very manual in nature, and trying to extract data from sometimes-messy HTML structure can be painful. It's hard and just has to be done.

This repository includes a web scraper that should work for most, if not all, Jive-powered online communities. The HTML structure of any Jive-powered community should be uniform. In `phase_1/past_scraper.py`, simply change the base URL and customize the `main()` function to point the code towards whatever Jive-powered community threads are desired, according to whatever custom search parameters are chosen (the `GLOBAL_KEYWORDS` global variable). A good choice for the URL would be the URL for the community's search results page when the search query is "Freescale".

`phase_1/past_scraper.py` scrapes everything currently on the site in question. It's intended to be used as a single-pass scraper to see what has been said on online up to the present moment.

`phase_1/rss_scraper.py` scrapes from a Jive RSS feed of the community forum. It should be run periodically, as the feed shows the 10 most recent threads (periodicity to be determined by the user according to the time frequency of occurrence of posts).

Copy the outputted `.csv` file of the text data to `phase_2.` Each row of this `.csv` file has the following columns, in order: `Snippet`, `URL`, `Day`, `Month`, `Year` (of writing).

Run `phase_2/snippet_labeler.py` on the `.csv` file to append another column on each row, `Sentiment`, that contains the sentiment score for each text snippet, on a scale of 0 to 4, 0 being very negative, 2 being neutral, and 4 being very positive. This is the scoring method that the SentimentPipeline on the Stanford CoreNLP software uses. `phase_2/snippet_labeler.py` calls `phase_2/run_core_nlp.py` to spawn a JVM in a system subprocess on which the Stanford software runs. It's been tested and works on both Windows 7 and OS X platforms; by extension it should work on a Linux platform such as a server, since Linux and OS X systems share the Unix shell.

To group the snippets into different `.csv` files according to sentiment value, run the `phase_2/snippet_grouper.py` script. At that point, the data is ready for mining.

Happy scraping! [Email me](mailto:gregakinman@gmail.com) with questions.

NOTE:
---

Numerous files are left out (check the .gitignore for more details). The most important and notable of these exclusions is the Stanford CoreNLP software. You will need to separately download the CoreNLP software and place it in the `sentiment_analysis/phase_2` directory. Also, some of the filepaths used in commands in `phase_2/run_core_nlp.py` need to match the version of the CoreNLP software installed. The current supported version is version 3.4, released June 16th, 2014. Either make sure the commands match, or only use version 3.4 of the software. The release history of the software can be found [here](http://nlp.stanford.edu/software/corenlp.shtml#History). The up-to-date repository for the software can be found [here](https://github.com/stanfordnlp/CoreNLP).
