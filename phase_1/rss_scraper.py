"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

rss_scraper.py

Scrapes from the present to the future using RSS feeds.
"""

import csv
from urllib import urlopen
from bs4 import BeautifulSoup as BS
from past_scraper import element_14_page_getter

def main():

    """
    Main function. Call whatever functions below that are necessary.
    """

    element_14_rss_scraper()

def element_14_rss_scraper():

    """
    Scrapes the Element14 Jive RSS feed.
    """

    rss_url = "http://www.element14.com/community/view-browse-feed.jspa?browseSite=content&browseViewID=content&userID=-1&query=freescale&filterID=all~objecttype~objecttype%5Bthread%5D&filterID=all~language~language%5Bcpl%5D"

    # Parses the XML and gets each thread.
    xml = urlopen(rss_url).read()
    soup = BS(xml, "xml")
    threads = soup.find_all("item")
    urls = []
    for thread in threads:
        urls.append(thread.find("guid").get_text())

    # Gets the snippets.
    snippets = []
    for url in urls:
        subsnippets = element_14_page_getter(url)
        for subsnippet in subsnippets:
            snippets.append(subsnippet)

    # Removes commas in preparation for writing to a CSV file.
    element_14_snippets = []
    for snippet in snippets:
        snippet[0].replace(",", "")
        element_14_snippets.append(snippet)

    # Writes the text and metadata to a CSV file.
    with open("element_14_rss_snippets.csv", "wb") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Snippet", "URL", "Day", "Month", "Year"])
        for snippet in element_14_snippets:
            try:
                csv_writer.writerow(snippet)
            except UnicodeEncodeError:
                print "UnicodeEncodeError thrown. Skipped offending snippet (probably unimportant)."
                continue

if __name__ == "__main__":
    main()
