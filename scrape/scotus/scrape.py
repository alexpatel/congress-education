#!/usr/bin/python2
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://supremecourthistory.org/history_timeline.html"
OUTPUT = "scotus.csv"
HEADER = ['NAME', 'BIO_LINK', 'TENURE', 'TITLE' , 'BIO', 'BIRTH-DEATH', 'DEGREE', 'SCHOOL', 'GRAD_YEAR', 'SCHOOL_LOCATION']

def get_bio(bio_link):
    """ Pull full text of congressperson's biography. """
    soup = BeautifulSoup(requests.get(bio_link).text)
    ps = [p.text for p in soup.find_all('p')]
    return " ".join(ps[0].split())

def get_people():
    """ Get biography link for all supreme court justices. """
    req = requests.get(BASE_URL)
    soup = BeautifulSoup(req.text)
    headers = soup.find_all('ul')
    groups = headers[2:4]
    info = []
    get_level = lambda gno : 'Chief Justice' if gno == 0 else 'Associate Justice'
    for (i, g) in enumerate(groups):
        level = get_level(i)
        links = g.findAll('a')
        for l in links:
            txt = l.text.split(',')
            href = l.get('href')
            info.append([txt[0], href, txt[1], level, get_bio(href)])

if __name__ == '__main__':
    get_people()
