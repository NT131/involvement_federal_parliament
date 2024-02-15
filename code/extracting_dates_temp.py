#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 11:00:14 2024

@author: niels_tack
"""
import requests
from bs4 import BeautifulSoup
import re

# URL of the webpage containing the HTML content
url = "https://www.dekamer.be/kvvcr/showpage.cfm?&language=nl&cfm=/site/wwwcfm/qrva/qrvatoc.cfm?legislat=55&bulletin=B125"

# Send an HTTP GET request to the URL
response = requests.get(url)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
# Get the HTML content from the response
html_content = response.content


# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

str(soup)[200:500]

divs_temp = re.split(r'<div class=\"linklist_[01]\">', str(soup))
len(divs_temp)
divs_temp[20]

# Find all div elements
divs = soup.find_all('div')

# Initialize a list to store the extracted content segments
extracted_content = []

# Initialize a variable to store the current segment
current_segment = ''

# Iterate through each div
for div in divs:
    # Extract the content of the div
    div_content = div.decode_contents()
    
    # Add the content to the current segment
    current_segment += div_content
    
    # Check if a new div section has started
    if div.find_next_sibling('div'):
        # If a new div section has started, append the current segment to the list
        extracted_content.append(current_segment)
        
        # Reset the current segment for the new segment
        current_segment = ''

len(extracted_content)

extracted_content[54]
extracted_content[55]
extracted_content[56]

# Print or process the extracted content segments
for segment in extracted_content:
    print(segment)