#!/usr/bin/python2

import csv
import re
import requests
import threading
from bs4 import BeautifulSoup

BASE_URL = "http://bioguide.congress.gov/biosearch/biosearch1.asp"
OUTPUT = lambda x : "bios_{}.csv".format(x)
HEADER = ['NAME', 'BIO_LINK', 'BIRTH-DEATH', 'POSITION', 'PARTY', 'STATE', 'CONGRESS-NUM', 'MATCH_STRING', 'DEGREE', 'SCHOOL', 'GRAD_YEAR', 'SCHOOL_LOCATION']
RANGE = xrange(64, 115) # meetings since 1915

edu_pattern = r'; (?P<degree>(?!D\.C\.)([A-Za-z]{1,2}\.)*), (?P<school>[\w+\s*\w+]*),(?P<location>[\w+\s*\w+\.,\s]*), (?P<grad_year>\d{4})'
edu_regex = re.compile(edu_pattern)

sem = threading.Semaphore(4)
printlock = threading.Lock()

def get_bio(bio_link):
    """ Pull full text of congressperson's biography. """
    soup = BeautifulSoup(requests.get(bio_link).text)
    ps = [p.text for p in soup.find_all('p')]
    return ps[0]

def get_edu(bio):
    """ Extract degree data from biography. """
    strip = lambda s : s.replace('\n', '').replace('\r', '')
    bio = strip(bio)
    matches = edu_regex.finditer(bio)
    edus = []
    try: 
        while 1:
            match = matches.next()
            gd = match.groupdict()
            edus.append(gd)
    except StopIteration:
        pass

    # uncomment this block to fact-check education parser
    """ 
    print bio
    for e in edus:
        print e['degree']
        print e['school']
        print e['grad_year']
        print '--'

    inp = raw_input()
    while not inp == "":
        if inp[0] == "d":
            n = int(inp[1:])
            edus.pop(n)
        elif inp[0] == "e":
            edu = []
            print "degree"
            edu.append(raw_input())
            print "school"
            edu.append(raw_input())
            print "grad_year"
            edu.append(raw_input())
            edus.append(edu)
        inp = raw_input()
    """
    return edus

def get_people(congress_num):
    """ Get biography link for all congress people in a session. """
    sem.acquire()
    printlock.acquire()
    print "starting thread", congress_num
    printlock.release()
    url = BASE_URL
    payload = {"congress" : str(congress_num)}
    req = requests.post(url, payload)
    soup = BeautifulSoup(req.text)
    trs = soup.find_all('table')[1].find_all('tr')
    people = []
    for i, tr in enumerate(trs):
        if i:
            tds = tr.find_all('td')
            link = tds[0].a
            if link:
                href, name = link.get('href'), link.text
                printlock.acquire()
                print "thread {} {}".format(congress_num, name.encode('ascii', 'ignore'))
                printlock.release()
                bio = get_bio(href)
                edu = get_edu(bio)
                for e in edu:
                    person = [name, \
                            href, \
                            tds[1].text,
                            tds[2].text,
                            tds[3].text,
                            tds[4].text,
                            tds[5].text,
                            e["degree"],
                            e["school"],
                            e["grad_year"],
                            e["location"]
                    ]
                    people.append(person)
    write(HEADER, people, OUTPUT(congress_num))
    sem.release()

def get_people_all():
    """ Get bio links for members of every congress. """
    all_people = []
    all_people.append(HEADER)
    # use four threads to scrape information for all congresspeople
    for n in RANGE:
        thread = threading.Thread(target=get_people, args=(n,))
        thread.start()

def write(header, data, file):
    """ Write data to CSV. """
    with open(file, "wb") as f:
        writer = csv.writer(f, delimiter=',')
        for line in data:
            writer.writerow([unicode(s).encode("utf-8") for s in line])

def main():
    get_people_all()

if __name__ == '__main__':
    main()
