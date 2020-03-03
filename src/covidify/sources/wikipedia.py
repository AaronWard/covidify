#!/usr/bin/env python3

from bs4 import BeautifulSoup
import wikipedia


def fetch_wiki(article):
    data = wikipedia.page(article).html()
    soup = BeautifulSoup(data, 'lxml')
    table = soup.find_all('table')[1] # Wuhan coronavirus situation in mainland China as of 24:00 CST
    rows = table.find_all('tr')

    all_headers = list()
    data = list()

    for header_row in rows[1:2]: # get headers, but structure the code by using an loop
        headers = header_row.find_all('th')

        for header in headers:
            # prepare the text from each header ot make it more consistent
            all_headers.append(' '.join(header.text.strip().split('\n')).replace(' (', '').lower())

    for row in rows[2:]: # skip first two table header rows
        columns = [x.text.split('\n')[0] for x in row.find_all('td')]

        # clean [note n] things
        columns = [(column if not '[note ' in column else '') for column in columns]
        data.append(columns)

    data.pop() # remove the ['Notes:'] row

    return all_headers, data


# use this function to get the data
def get(article = 'Timeline of the 2019–20 coronavirus outbreak'):
    article = fetch_wiki(article)
    return prepare_data(article)
