"""jobNlp.py

Uses natural language processing (NLP) to identify key information in job
postings and provide a summary of the data.
"""

"""
goals:
    * take data from job description, probably given in an HTML format.
    * identify key aspects of the job description
        - key technical skills
        - key experience lengths (e.g. "2+ years of professiona ___ experience")
        - preferences
            - grad school/advanced degree preferred?
                - how much does experience req. change based on degree? e.g.
                  do they require only 1 year of experience rather than 5 if you
                  have a masters?
                - what advanced degree(s) do they prefer?
            - nice-to-have skills
        - who I'm working for
            - where they're located
            - where the job is located (is it remote?)
        - benefits
            - healthcare coverage, vacation hours & holidays

    * possible things to watch out for
        * having my inputs be detected on LinkedIn as crawling behavior.
            * maybe I'd access webpages too fast if I use a browser driver or
              if I automate mouse clicks and stuff.
              --> maybe have the time it takes to analyze one description vary
                  slightly? maybe apply brownian noise to the mouse movements? 

"""

from inspect import stack
import json     # FIXME I don't think I'll need this later. 
import pprint   # FIXME I don't think I'll need this later, either

import re
import spacy
from bs4 import BeautifulSoup

# ------------------------------------------------------------------------------
# 
# 
def correctStr(str):
    """Adds escape characters to problematic characters in input string and
    returns the corrected string.
    """
    res = ""
    prob = set('"')  # problematic characters
    for c in str:
        if c in prob:
            res += "\\"
        res += c
    return res

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)

print()

with open("jobDesc2.txt") as file:
    soup = BeautifulSoup(file, 'html.parser')
    print(soup.prettify(),"\n--- just text ---", soup.get_text())
    # for line in file:
        # doc = nlp(line)
        # for token in doc:
        #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #             token.shape_, token.is_alpha, token.is_stop)
        # print(line)
        # pass
    # tempStr = "".join(soup.get_text().split())
    tmpStr = soup.get_text()   # create single unified string of job descr.
    tmpList = tmpStr.split("About the job") # job description always starts with "Abou the job" header
    
    # FIXME
    print("tmpList:\n", tmpList)
    # print("\n-----   repr: tmpList[-1]\n", repr(tmpList[-1]))
    print("\n-----    tmpList[-1]\n", (tmpList[-1]))
    # print("type of tmpList[-1]", type(tmpList[-1]))

    descrLines = tmpList[-1].split("\n")

    # FIXME
    print("\npretty print of list:")
    pprint.pprint(descrLines)

    print("trying to get char at end of line:", descrLines[5][-1])

    # go through lines and split by section
    secs = []   # [ [section title, section content], [], ... ]
    # stk = []    # temp list for constructing sections
    secTitle = ""
    # for line in descrLines:
    #     if re.search("[a-zA-Z]", line):
    #         if line[-1] == ":":
    #             print("\nsecTitle:", secTitle)
    #             print("\nstck:", stk)
    #             tmp = [secTitle, stk.copy()]
    #             print("\ntmp:", tmp)

    #             secs.append(tmp)
    #             secTitle = line
    #             stk.clear()
    #             # print("stk after adding:", stk)

    #             # print("\nstck AFTER:", stk)
    #             # print("\nsecs:", secs)

    #         else:
    #             stk.append(line)
    #         # print(line)
    
    resStr = ""
    for line in descrLines:
        if re.search("[a-zA-Z]", line):
            if line[-1] == ":":
                tmp = [secTitle, resStr]
                print("\ntmp:", tmp)

                secs.append(tmp)
                secTitle = line
                resStr = ""
                # print("stk after adding:", stk)

                # print("\nstck AFTER:", stk)
                # print("\nsecs:", secs)

            else:
                resStr += line
            # print(line)

    print("pretty print of processing:")
    pprint.pprint(secs)
    print("test1:\n", correctStr(secs[-1][1]))
    print("test2:\n", secs[-2][1])
    print("test2:\n", repr(secs[-2][1]))