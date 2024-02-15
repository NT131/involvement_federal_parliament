#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 11:59:10 2024

@author: niels_tack
"""
import pandas as pd

import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage containing the HTML content
url = "https://www.dekamer.be/kvvcr/showpage.cfm?&language=nl&cfm=/site/wwwcfm/qrva/qrvatoc.cfm?legislat=55&bulletin=B125"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Get the HTML content from the response
html_content = response.content

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Split soup string at every staring point of a relevant htlml block, 
# i.e. indicated by "<div class="linklist_0">" or "<div class="linklist_1">"
# There are separate div elements for the enumerateion (e.g. 11., 25.).
# we can avoid selecting thise too by adding the start of the html code in the relevant section,
# i.e. "\n<table width="100%">\n"

# divs = re.split(r'<div class=\"linklist_[01]\">', str(soup))
divs = re.split(r'<div class=\"linklist_[01]\">\n<table width="100%">\n', str(soup))

# Inspect results
len(divs)
divs[0]
divs[1]
divs[10]
divs[20]
divs[-1]

# Drop first element, since this is the html code up to the first relevant section
del divs[0]

# Oba

# A function to extract the text between two strings
# This is less robust than using BeautifulSoup, but the latter rendered errors, 
# possibly due to set up of html page
def extract_text(s, start, end):
    start_index = s.find(start)
    if start_index != -1:
        start_index += len(start)
        end_index = s.find(end, start_index)
        if end_index != -1:
            return s[start_index:end_index].strip()


def split_author(input_string):
    """
    Function to split strings as obtained from html page into name of member, his/her party and id of question

    e.g. 
    'Anneleen\n      Van Bossuyt,\n      N-VA (07354)'
    ('Anneleen Van Bossuyt', ' N-VA ', '07354')
    """
    # Remove unnecessary characters (newlines and bracket at end (of id number))
    cleaned_string = input_string.replace("\n", "").rstrip(")")
    
    # Replace any sequence of spaces with a single space
    cleaned_string = re.sub(r'\s+', ' ', cleaned_string)

    # split on comma (between name and party) and left bracket (between party and id number)
    name, party, id_number = re.split(r',|\(', cleaned_string)

    return name, party, id_number

# Create empty lis to store details
details_question_list =[]

for div in divs: 
    # Extracting values for the specified tags
    author_full = extract_text(div, '<i>Auteur</i></td><td class="txt">', '</td>')
    department = extract_text(div, '<i>Departement</i></td><td class="txt">', '</td>')
    title = extract_text(div, '<i>Titel</i></td><td class="txt">', '</td>')
    date_submission_full= extract_text(div, '<i>Datum indiening</i></td>\n<td class="txt">', '</td>')
    date_submission = date_submission_full.split()[0] if date_submission_full else None
    answer_published = extract_text(div, '<a href="', '" target="_blank">')

    # Split string on about using dedicatd function
    author, party_author, id_question = split_author(author_full)

    #Store elements in overall list
    details_question_list.append([id_question, author, party_author, department, 
                                  title, date_submission, answer_published])

# Inspect data
len(details_question_list)
details_question_list[0]
details_question_list[10]
details_question_list[20]
details_question_list[-20]
details_question_list[-1]
    

# Turn list into dataframe
questions_df = pd.DataFrame(details_question_list,
                            columns = ["ID vraag", "Parlementslid", "Partij parlementslid", 
                                       "Minister (bevoegdheden)", "Onderwerp",
                                       "Datum ingediend", "Url publicatie"]
                           )

# Inspect results
questions_df.head()
questions_df.shape
questions_df.columns
