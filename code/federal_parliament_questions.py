#!/usr/bin/env python
# coding: utf-8

# The Belgian Federal Parliament (De Kamer) provides an overview of all written questions of members of parliament to the ministers. There is no API. The questions and answers are available through pdfs or html pages. 

# # Setting up

# In[1]:


# show all outputs of cell, not merely of last line (i.e. default of Jupyter Notebook)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"


# In[74]:


import os
import requests
from bs4 import BeautifulSoup
# import fitz  # PyMuPDF
import pandas as pd

import re

from collections import Counter

import pickle


# # Extract various Bulletins

# First we create a function to obtain the urls of all so-called Bulletins in which the Federal Parliament provides the individual questions. 

# In[4]:


def scrape_list_bulletins(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        bulletin_urls = []
    
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('showpage.cfm?&language=nl&cfm=/site/wwwcfm/qrva/qrvatoc.cfm?legislat'):
                bulletin_url = f"https://www.dekamer.be/kvvcr/{link['href']}"

                # print(bulletin_url)

                bulletin_urls.append(bulletin_url)
            
                # question_response = requests.get(question_url)
                # question_soup = BeautifulSoup(question_response.text, 'html.parser')
                
                # question_info = extract_question_info(question_soup)
                # bulletin_urls.append(question_info)

        # Remove duplicates, since urls are 2 times shown
        bulletin_urls = sorted(set(bulletin_urls))
        
        return bulletin_urls



    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


# In[5]:


# Define url of page with overview of urls of bulletins
url_main_page = "https://www.dekamer.be/kvvcr/showpage.cfm?section=/qrva&language=nl&cfm=qrvaList.cfm"

# Obtain urls
bulletin_urls_main_page = scrape_list_bulletins(url_main_page)

# Inspect results
bulletin_urls_main_page


# # Extract relevant information for each question

# Each Bulletin contains various questions. The html page of the Bulletin provides for each question some information, which can extract:
# * Auteur (i.e. author, the member of parliament posing the question)
# * Departement (i.e. the minister to whom the question is directed)
# * Titel (i.e. subject of the question)
# * Datum ingediend (i.e. the date when the question was asked)
# * Antwoord gepubliceerd (i.e. the hyperlink to the answer to the question)
# 
# * To obtain these elements, we create various functions. 

# Then we obtain for each of those bulletins all questions and the relevant information for these questions. For this we use a helper function to extract the author, relevant minister and subject of the question. The html structure is not so clear (i.e. not all relevant elements are contained within a single container, so using specific anchors does not suffice). Later on the date the question was asked, as well as wether an answer was provided before publishing the question or not can be obtained. 

# In[6]:


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


# In[7]:


# WORKABLE CODE ##

def scrape_bulletin(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        question_containers_0 = soup.find_all('div', class_='linklist_0')
        question_containers_1 = soup.find_all('div', class_='linklist_1')

        entries = []
        
        for question_container in question_containers_0 + question_containers_1:


            tr_elements = question_container.find_all('tr')
            # print("----", tr_elements)

            # Initialize variables for additional information
            author, party_author, id_question, department, title = "N/A", "N/A", "N/A", "N/A", "N/A"

            for tr_element in tr_elements:

                # print(tr_element)
                # print("**********")
                
                td_elements = tr_element.find_all('td', class_='txt')

                
                
                if len(td_elements) == 2:
                    label, value = td_elements[0].text.strip(), td_elements[1].text.strip()

                    # print(label)
                    # print("****")
                    # print(value)
                    # print("***************")

                    if "Auteur" in label:
                        # Split string on about using dedicatd function
                        author, party_author, id_question = split_author(value)
                    elif "Departement" in label:
                        department = value
                    elif "Titel" in label:
                        title = value
                    # elif "Datum indiening" in label:
                    #     date_questions = value
                    # elif "Antwoord gepubliceerd" in label:
                    #     # Extract the URL if available
                    #     answer_published = td_elements[1].find('a')['href'] if td_elements[1].find('a') else "N/A"




            # # Print or store the extracted information
            # print(f"Auteur: {author}")
            # print(f"Departement: {department}")
            # print(f"Titel: {title}")
            # print(f"Datum vraag: {date_questions}")
            # print("----")

            if not author == party_author == id_question == department == title == 'N/A':
                entries.append([id_question, author, party_author, department, title])

        return entries
                

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")



# In[8]:


# # limit amounf of pages for testing
# bulletin_urls_main_page = bulletin_urls_main_page[:3]


# In[9]:


# Initialize list with details on all questions
questions_all = []
# iterate over all urls of bulletin
for index, url in enumerate(bulletin_urls_main_page):
    # Obtain information of all questions in relevant bulletin
    questions_per_bulletin = scrape_bulletin(url)
    questions_all.extend(questions_per_bulletin) # extend to overall list (no appending to avoid nesting)
    print(f"Aantal pagina's aan vragen verwerkt: {index + 1}.") # Show progress


# In[100]:


# Turn list into dataframe
questions_df = pd.DataFrame(questions_all,
                            columns = ["ID vraag", "Parlementslid", "Partij parlementslid", "Minister (bevoegdheden)", "Onderwerp"]
                           )


# In[101]:


# # Inspect results
# questions_all
questions_df

questions_df["Partij parlementslid"].value_counts()


# Upon inspection of the results, it seems some party names are incorrect. Sometimes abbreviations are use ('VB' instead of 'Vlaams Belang') or a party changed names during the legislative periode (e.g. 'sp.a' v. 'Vooruit').

# In[102]:


# Strip leading and trailing whitespace from column names
questions_df.columns = questions_df.columns.str.strip()

# Replace party names, accounting for trailing spaces
questions_df["Partij parlementslid"] = questions_df["Partij parlementslid"].str.strip().replace(['sp.a', 'Voorui'], 'Vooruit')
questions_df["Partij parlementslid"] = questions_df["Partij parlementslid"].str.strip().replace('cdH', 'LENGAG')

# Additional replacements, accounting for trailing spaces
questions_df["Partij parlementslid"] = questions_df["Partij parlementslid"].str.strip().replace({
    'LENGAG': 'Les Engagés', 'CD&V': 'cd&v', 'DéFI': 'Défi', 'VB': 'Vlaams Belang', 'INDEP': 'Onafhankelijk'})


questions_df["Partij parlementslid"].value_counts()


# Also, the responsible minister is merely name by the competences he/she manages. It seems more user-friendly to replace this by the actual name of the minister.
# 
# **Once dates of question can be taken into account, the change in ministers can be taken into account. Currently we simply refer to the name of the current minister holding the post**

# In[103]:


minister_competences_2_names_dict = {
    # Function allocated to multiple persons, unclear to distinguish based on allocated competences
    'Eerste Minister': 'Alexander De Croo',
    'Eerste Minister': 'Sophie Wilmès', # 27 oktober 2019 - 30 november 2019 (before exit Reynders) 
    'Eerste Minister': 'Charles Michel',

    # Michel II (9 december 2018 - 27 oktober 2019) (and not continued as such in Wilmès-I and / Wilmès-II)
        # See https://nl.wikipedia.org/wiki/Regering-Michel_II
    'Minister van Begroting en van Ambtenarenzaken, belast met de Nationale Loterij en Wetenschapsbeleid': 'Sophie Wilmès',
    'Minister van Werk, Economie en Consumenten, belast met Buitenlandse Handel, Armoedebestrijding, Gelijke Kansen en Personen met een beperking': 'Wouter Beke', # 2 juli 2019 - 2 oktober 2019 
    
    
    # Wilmès-I (27 oktober 2019 - 17 maart 2020)
        # See https://nl.wikipedia.org/wiki/Regering-Wilm%C3%A8s_I

        # Before exit Didier Reynders (27 oktober 2019 - 30 november 2019)
    'Vice-eersteminister en Minister van Buitenlandse en Europese Zaken, en van Defensie, belast met Beliris en de Federale Culturele Instellingen': 'Didier Reynders', 
    'Minister van Begroting en van Ambtenarenzaken, belast met de Nationale Loterij en Wetenschapsbeleid': 'David Clarinval', 
    'Vice-eersteminister en Minister van Justitie, belast met de Regie der Gebouwen': 'Koen Geens', 

        # After exit Didier Reynders: 
        # competences shifted to Wilmès, Clarinval and Geens (but remained same during Wilmès I and Wilmès II)
    
    # Wilmès-II (17 maart 2020 - 1 oktober 2020)
        # Zie https://nl.wikipedia.org/wiki/Regering-Wilm%C3%A8s_II


    # Wilmès I en Wilmès II (so no changes at 17 maart 2020 - so from 27 oktober 2019 or 30 november 2019 until 1 oktober 2020)
        # After exit Reynders (as of 30 november 2019 until 1 oktober 2020)
    'Eerste Minister, belast met Beliris en de Federale Culturele Instellingen': 'Sophie Wilmès', 
    'Vice-eersteminister en Minister van Begroting en van Ambtenarenzaken, belast met de Nationale Loterij en Wetenschapsbeleid': 'David Clarinval', 
    'Vice-eersteminister en Minister van Justitie, belast met de Regie der Gebouwen, en Minister van Europese Zaken': 'Koen Geens',

        # General (as of 27 oktober 2019 until 1 oktober 2020)
    'Vice-eersteminister en Minister van Financiën, belast met Bestrijding van de fiscale fraude, en Minister van Ontwikkelingszaken': 'Alexander De Croo',

    'Minister van Buitenlandse Zaken, en van Defensie': 'Philippe Goffin',
    'Minister van Digitale Agenda, Telecommunicatie en Post, belast met Administratieve Vereenvoudiging, Bestrijding van de sociale fraude, Privacy en Noordzee': 'Philippe De Backer',
    'Minister van Energie, Leefmilieu en Duurzame Ontwikkeling': 'Marie-Christine Marghem',
    "Minister van Middenstand, Zelfstandigen, Kmo's, Landbouw, en Maatschappelijke Integratie, belast met Grote Steden": 'Denis Ducarme',
    'Minister van Mobiliteit, belast met Belgocontrol en de Nationale Maatschappij der Belgische spoorwegen': 'François Bellot',
    'Minister van Pensioenen': 'Daniel Bacquelaine',
    'Minister van Sociale Zaken en Volksgezondheid, en van Asiel en Migratie': 'Maggie De Block',
    'Minister van Veiligheid en Binnenlandse Zaken': 'Pieter De Crem',
    'Minister van Werk, Economie en Consumenten, belast met Armoedebestrijding, Gelijke Kansen en Personen met een beperking': 'Nathalie Muylle', # 2 oktober 2019 - 27 oktober 2019 
     
    # Regering De Croo

    'Vice-eersteminister en Minister van Economie en Werk': 'Pierre-Yves Dermagne',
    'Vice-eersteminister en Minister van Buitenlandse Zaken, Europese Zaken en Buitenlandse Handel, en de Federale Culturele Instellingen': 'Sophie Wilmès', # 1 oktober - 14 juli 2022
    'Vice-eersteminister en Minister van Mobiliteit': 'Georges Gilkinet',
    'Vice-eersteminister en Minister van Financiën, belast met de Coördinatie van de fraudebestrijding': 'Vincent Van Peteghem',
    'Vice-eersteminister en Minister van Sociale Zaken en Volksgezondheid': 'Frank Vandenbroucke',
    'Vice-eersteminister en Minister van Ambtenarenzaken, Overheidsbedrijven, Telecommunicatie en Post': 'Petra De Sutter',
    'Vice-eersteminister en Minister van Justitie, belast met de Noordzee': 'Vincent Van Quickenborne', # 1 oktober 2020 - 22 oktober 2023
    'Vice-eersteminister en Minister van Justitie, belast met de Noordzee': 'Paul Van Tigchelt', # 22 oktober 2023 - now
    
    

    "Minister van Middenstand, Zelfstandigen, Kmo's en Landbouw, Institutionele Hervormingen en Democratische Vernieuwing": 'David Clarinval',
    "Minister van Middenstand, Zelfstandigen, Kmo's en Landbouw, Institutionele Hervormingen en Democratische Vernieuwing, belast met Buitenlandse Handel" :'David Clarinval', 
    'Minister van Pensioenen en Maatschappelijke Integratie, belast met Personen met een beperking, Armoedebestrijding en Beliris': 'Karine Lalieux',
    'Minister van Defensie': 'Ludivine Dedonder',
    'Minister van Klimaat, Leefmilieu, Duurzame Ontwikkeling en Green Deal': 'Zakia Khattabi',
    'Minister van Binnenlandse Zaken, Institutionele Hervormingen en Democratische Vernieuwing': 'Annelies Verlinden',
    'Minister van Ontwikkelingssamenwerking en Grootstedenbeleid': 'Meryame Kitir', # 1 oktober 2020 - 17 december 2022 
    'Minister van Ontwikkelingssamenwerking en Grootstedenbeleid': 'Caroline Gennez', # 17 december 2022 - now
    # 'Minister van Ontwikkelingssamenwerking, belast met Grote Steden' seems to be same as 'Minister van Ontwikkelingssamenwerking en Grootstedenbeleid'
    'Minister van Ontwikkelingssamenwerking, belast met Grote Steden': 'Meryame Kitir', # 1 oktober 2020 - 17 december 2022 
    'Minister van Ontwikkelingssamenwerking, belast met Grote Steden': 'Caroline Gennez', # 17 december 2022 - now
    'Minister van Energie': 'Tinne Van der Straeten',
    'Minister van Buitenlandse Zaken, Europese Zaken en Buitenlandse Handel, en de Federale Culturele Instellingen.': 'Hadja Lahbib', # 15 juli 2022 - now
    

    'Staatssecretaris voor Relance en Strategische Investeringen, belast met Wetenschapsbeleid, toegevoegd aan de Minister van Economie en Werk': 'Thomas Dermine',
    'Staatssecretaris voor Digitalisering, belast met Administratieve Vereenvoudiging, Privacy en de Regie der Gebouwen, toegevoegd aan de Eerste Minister': 'Mathieu Michel',
    'Staatssecretaris voor Digitalisering, belast met Administratieve Vereenvoudiging, Privacy en de Regie der Gebouwen, de Federale Culturele Instellingen, toegevoegd aan de Eerste Minister': 'Mathieu Michel',
    'Staatssecretaris voor Gendergelijkheid, Gelijke Kansen en Diversiteit, toegevoegd aan de Minister van Mobiliteit': 'Sarah Schlitz', # 1 oktober 2020 - 26 april 2023
    'Staatssecretaris voor Gendergelijkheid, Gelijke Kansen en Diversiteit, toegevoegd aan de Minister van Mobiliteit': 'Marie-Colline Leroy', # 2 mei 2023 - now
    'Staatssecretaris voor Asiel en Migratie, belast met de Nationale Loterij, toegevoegd aan de Minister van Binnenlandse Zaken, Institutionele Hervormingen en Democratische Vernieuwing': 'Sammy Mahdi', # 1 oktober 2020 - 28 juni 2022
    'Staatssecretaris voor Asiel en Migratie, toegevoegd aan de Minister van Binnenlandse Zaken, Institutionele Hervormingen en Democratische Vernieuwing': 'Nicole de Moor', # 28 juni 2022 - now # 'Nationale Loterij' now at Van Peteghem
    'Staatssecretaris voor Begroting en Consumentenbescherming, toegevoegd aan de Minister van Justitie, belast met de Noordzee': 'Eva De Bleeker', # 1 oktober 2020 - 18 november 2022 
    'Staatssecretaris voor Begroting en Consumentenbescherming, toegevoegd aan de Minister van Justitie, belast met de Noordzee': 'Alexia Bertrand', # 18 november 2022 - now
}


# In[104]:


# Temporary modification of dict, until splitting by time is possible
minister_competences_2_names_dict["Eerste minister"] = 'Alexander De Croo / Sophie Wilmès / Charles Michel'
minister_competences_2_names_dict['Minister van Begroting en van Ambtenarenzaken, belast met de Nationale Loterij en Wetenschapsbeleid'] = 'Sophie Wilmès / David Clarinval'
minister_competences_2_names_dict['Vice-eersteminister en Minister van Justitie, belast met de Noordzee'] = 'Vincent Van Quickenborne / Paul Van Tigchelt'
minister_competences_2_names_dict['Minister van Ontwikkelingssamenwerking en Grootstedenbeleid'] = 'Meryame Kitir / Caroline Gennez'
minister_competences_2_names_dict['Minister van Ontwikkelingssamenwerking, belast met Grote Steden'] = 'Meryame Kitir / Caroline Gennez'
minister_competences_2_names_dict['Staatssecretaris voor Gendergelijkheid, Gelijke Kansen en Diversiteit, toegevoegd aan de Minister van Mobiliteit'] = 'Sarah Schlitz / Marie-Colline Leroy'
minister_competences_2_names_dict['Staatssecretaris voor Begroting en Consumentenbescherming, toegevoegd aan de Minister van Justitie, belast met de Noordzee'] = 'Eva De Bleeker / Alexia Bertrand'



# In[105]:


# Assess results
minister_competences_2_names_dict.keys()

minister_competences_2_names_dict["Eerste minister"]
minister_competences_2_names_dict['Minister van Begroting en van Ambtenarenzaken, belast met de Nationale Loterij en Wetenschapsbeleid']
minister_competences_2_names_dict['Vice-eersteminister en Minister van Justitie, belast met de Noordzee'] 
minister_competences_2_names_dict['Minister van Ontwikkelingssamenwerking en Grootstedenbeleid']
minister_competences_2_names_dict['Minister van Ontwikkelingssamenwerking, belast met Grote Steden']
minister_competences_2_names_dict['Staatssecretaris voor Gendergelijkheid, Gelijke Kansen en Diversiteit, toegevoegd aan de Minister van Mobiliteit'] 
minister_competences_2_names_dict['Staatssecretaris voor Begroting en Consumentenbescherming, toegevoegd aan de Minister van Justitie, belast met de Noordzee']


# In[106]:


# map names to positions using dict
questions_df["Minister"] = questions_df["Minister (bevoegdheden)"].map(minister_competences_2_names_dict)


# In[107]:


# Inspect results (include check to ensure that names assigned for all posts / competences
questions_df.head()
questions_df[questions_df["Minister"].isna()]
questions_df["Minister"].unique()


# In[108]:


## Save details_questions_term_df for later use
# 1. Save as pkl
with open('../data/federal_details_questions_df.pkl', 'wb') as file:
    pickle.dump(questions_df, file)

# 2. Save as csv
questions_df.to_csv(path_or_buf = '../data/federal_details_questions_df.csv',
                               sep = ";",
                               encoding = "utf-16", # to ensure trema's are well handled (e.g. Koen Daniëls)
                               index = False)

