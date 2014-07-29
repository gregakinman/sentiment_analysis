"""
Greg Kinman - B48856
Freescale Semiconductor, Inc.

past_scraper.py

Scrapes the web from the past to the present.
"""

import nltk, csv, pdb
from urllib import urlopen
from datetime import datetime
from bs4 import BeautifulSoup as BS
from nltk.tokenize.punkt import PunktSentenceTokenizer as ST

GLOBAL_KEYWORDS = ["freescale", "i.mx", "kinetis", "qoriq", "riotboard", "riot board"]

def main():

    """
    Driver function. Call whatever functions from below that are necessary.
    """

    element_14_scraper()

def element_14_scraper():

    """
    Scrapes element14.com for text about Freescale.
    """

    base_url_1 = "http://www.element14.com/community/content?filterID=all~objecttype~objecttype%5Bthread%5D&filterID=al"
    base_url_2 = "l~language~language%5Bcpl%5D&ICID=menubar_content_discussions&query="

    element_14_snippets = []
    start_index = 0
    # Searches the online forum using each global keyword (which is probably actually an unrealistic thing to do...).
    for keyword in GLOBAL_KEYWORDS:
        print "\nSearching for keyword '" + keyword + "'...\n"
        at_end = False
        page_counter = 0
        # While not on the last search results page:
        while not at_end:
            url = base_url_1 + base_url_2 + keyword + "&start=" + str(start_index)
            if at_element_14_end(url):
               at_end = True
            # Gets the URLs for each thread in the page of search results.
            post_urls = element_14_post_url_getter(url)
            url_counter = 0
            for post_url in post_urls:
                # Grabs text snippets and metadata from the thread.
                subsnippets = element_14_page_getter(post_url)
                for snippet in subsnippets:
                    element_14_snippets.append(snippet)
                print "URL " + str(url_counter) + " scraped."
                url_counter += 1
            start_index += 20
            page_counter += 1
            print "\nSearch results page " + str(page_counter) + " scraped.\n"

    # Removes duplicates.
    element_14_snippets = dict((inner_list[0], inner_list) for inner_list in element_14_snippets).values()

    print "\nElement 14 domain scrape completed. " + str(len(element_14_snippets)) + " snippets found."

    # Gets the text snippets and prepares them for writing to a file.
    unformatted_element_14_snippets = element_14_scraper()
    element_14_snippets = []
    for snippet in unformatted_element_14_snippets:
        snippet[0].replace(",", "")
        element_14_snippets.append(snippet)

    # Writes the text and metadata to a CSV file.
    with open("element_14_past_snippets.csv", "wb") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Snippet", "URL", "Day", "Month", "Year"])
        for snippet in element_14_snippets:
            try:
                csv_writer.writerow(snippet)
            except UnicodeEncodeError:
                print "UnicodeEncodeError thrown. Skipped offending snippet (probably unimportant)."
                continue

def at_element_14_end(url):

    """
    Tests whether all the result pages have been scraped already.

    Input:
    1. url:         str: the URL of the page of search results

    Output:
    1. end_flag     bool: tells if all the result pages have been scraped already or not
    """

    end_flag = False

    html = urlopen(url).read()
    soup_bowl = BS(html)
    div_tags = soup_bowl.find_all("div")

    # The end page has been hit if there is a div tag in the page source code with class attribute value "j-empty".
    for div in div_tags:
        if div.has_attr("class"):
            if "j-empty" in div["class"]:
                end_flag = True

    return end_flag

def element_14_post_url_getter(url):

    """
    Given a search results page URL, returns a list of URL's to the individual forum posts.

    Input:
    1. url:     str: the URL of the page of search results
    """

    html = urlopen(url).read()
    soup = BS(html)

    # All the forum post titles are in td tags with CSS classes "j-td-title."
    post_urls = []
    forum_posts = soup.find_all(class_="j-td-title")
    for post in forum_posts:
        link_tag = post.find("a")
        link_url = link_tag["href"]
        post_urls.append(link_url)

    return post_urls

def element_14_page_getter(url):

    """
    Gets text snippets for each page in a thread.

    Input:
    1. url:             str: the url of the first page in the thread

    Output:
    1. post_snippets:   list of unicode's: the text snippets from the page
    """

    # Standardizes the URL for looping.
    new_url_base = url.split("/l/", 1)[0] + "?start="
    new_url_tail = "&tstart=0"

    at_end = False
    start = 0
    post_snippets = []
    while not at_end:
        # Checks if the last page has been reached already.
        page_url = new_url_base + str(start) + new_url_tail
        html = urlopen(page_url).read()
        if html.count("jive-rendered-content") < 3:
            at_end = True

        page_snippets = element_14_snippet_getter(page_url)

        for snippet in page_snippets:
            post_snippets.append(snippet)

        start += 15

    return post_snippets

def element_14_snippet_getter(url, keywords=GLOBAL_KEYWORDS):

    """
    Given a URL and keywords, returns a list of text snippets including those keywords.

    Inputs:
    1. url:         str: the desired URL
    2. keywords:    list of str's: defaults to global_keywords defined in main(); the desired keywords

    Output:
    1. snippets:    list of unicode's: the desired text snippets
    """

    # Pulls clean text from the URL, devoid of HTML.
    try:
        html = urlopen(url).read()
    except UnicodeError:
        print "UnicodeError thrown. Skipped offending URL (probably not in English and thus unanalyzable)."
        return []
    soup = BS(html)
    raw = nltk.clean_html(html)

    # We don't want propaganda written by Freescale employees.
    if ("FreescaleTools_and_Software" in raw) or ("GregC" in raw) or ("MAb" in raw):
        return []

    # Finds all HTML subtrees that tell us the date of writing of each post.
    post_data = soup.find_all(class_="j-post-author")

    # Finds all HTML subtrees comprising the posts themselves.
    posts = soup.find_all(class_="jive-rendered-content")

    snippets = []
    tokenizer = ST()
    dates = []
    # Assembles the dates of writing of each post.
    for post_datum in post_data:
        date_posted = date_getter(post_datum)
        dates.append(date_posted)
    # For each post in the page, grabs the text and metadata.
    for i in range(len(posts)):
        text = posts[i].get_text()
        # Splits the text into its individual sentences so that we can pick the ones we like.
        intermediate_snippets = tokenizer.tokenize(text)
        # Grabs text containing keywords, as well as sentences preceding and following those with keywords.
        for j in range(len(intermediate_snippets)):
            for word in keywords:
                snippet = intermediate_snippets[j]
                if (word in snippet.lower()) and ("http" not in snippet.lower()):
                    offset = 1
                    for k in range(j, len(intermediate_snippets)):
                        if word not in intermediate_snippets[k].lower():
                            break
                        else:
                            offset += 1
                    if j == 0:
                        subsnippet = intermediate_snippets[j:offset]
                    else:
                        subsnippet = intermediate_snippets[j-1:j+offset]
                    # Puts the individual sentences back together.
                    tokens = []
                    for sentence in subsnippet:
                        stripped = sentence.lstrip().rstrip().encode("UTF-8")
                        tokens.append(stripped)
                    for token in tokens:
                        try:
                            if len(token) < 1500:
                                snippets.append([token, url, dates[i][0], dates[i][1], dates[i][2]])
                        except IndexError:
                            continue

    return snippets

def date_getter(soup):

    """
    Returns a formatted date hidden in nasty unformatted HTML.

    Input:
    1. soup:        a BeautifulSoup object: the HTML subtree in question

    Output:
    1. date_posted: tuple: the date the post was written in (d, m, y) format
    """

    # Removes an unwanted span subtree from the mother subtree, since all it is is junk.
    unwanted = soup.find_all(class_="j-thread-replyto")
    if unwanted:
        unwanted[0].extract()

    # Extracts the author. Accounts for varying edge cases (boy, are there edge cases in Jive's code).
    author = soup.find_all("a")
    if author:
        author = author[0].get_text()
    else:
        author = soup.find_all("strong")[0].get_text()

    # Cleans up the date string extracted.
    date_posted = date_string_cleaner(soup, author)

    return date_posted

def date_string_cleaner(soup, author):

    """
    Formats the unformatted date string into a nice tuple.

    Inputs:
    1. soup:    a BeautifulSoup object: the HTML subtree in questions
    2. author:  unicode: the author of the post, which is irrelevant for Element14, and thus needs to be removed
    """

    # Cleans it up.
    date_and_author = soup.get_text()
    date_posted_unformatted = date_and_author.replace(author, "")
    date_posted_unformatted = date_posted_unformatted.replace(",", "")

    # Uses the datetime module to format the date nicely into a tuple.
    try:
        datetime_object = datetime.strptime(date_posted_unformatted.lstrip().rstrip(), "%b %d %Y %I:%M %p")
    except ValueError:
        # This error shouldn't ever be thrown anymore. But, if it does, we want to know why the hell why.
        pdb.set_trace()
    date_posted = (datetime_object.day, datetime_object.month, datetime_object.year)

    return date_posted

# This is necessary because we only want this script called explicitly from the command line (for now).
if __name__ == "__main__":
    main()
