#!/usr/bin/python2

import requests
import csv
from bs4 import BeautifulSoup

BASE_URL = "http://bioguide.congress.gov/biosearch/biosearch1.asp"
OUTPUT = "bios.csv"
HEADER = ['NAME', 'BIO_LINK', 'BIRTH-DEATH', 'POSITION', 'PARTY', 'STATE', 'CONGRESS-NUM']
RANGE = 115 # 114 meetings, include 0th

def get_people(congress_num):
    " Get biography link for all congress people in a session. """
    url = BASE_URL
    payload = {"congress" : str(congress_num)}
    req = requests.post(url, payload)
    soup = BeautifulSoup(req.text)
    # links = soup.find_all(href=True)
    # links.pop() # last link on page is 'Search Again'
    trs = soup.find_all('table')[1].find_all('tr')
    people = []
    for i, tr in enumerate(trs):
        if i:
            tds = tr.find_all('td')
            link = tds[0].a
            if link:
                href, name = link.get('href'), link.text
                person = [name, \
                        href, \
                        tds[1].text, \
                        tds[2].text, \
                        tds[3].text, \
                        tds[4].text,  \
                        tds[5].text  \
                ]
                people.append(person)
    return people

def get_people_all():
    """ Get bio links for members of every congress. """
    all_people = []
    all_people.append(HEADER)
    for n in xrange(RANGE):
        print n
        all_people.extend(get_people(n))
    return all_people

def write(data, file):
    """ Write data to CSV. """
    with open(file, "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for line in data:
            writer.writerow([unicode(s).encode("utf-8") for s in line])

def main():
    people = get_people_all()
    write(people, OUTPUT)

if __name__ == '__main__':
    main()
