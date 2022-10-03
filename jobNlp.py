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
import string

import re
import spacy
from spacy import displacy  # FIXME I don't think I'll need this later either
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
    print(soup.prettify(),"\n--- just text ---", soup.get_text())     # FIXME
    tmpStr = soup.get_text()                # create single unified string of job descr.
    tmpList = tmpStr.split("About the job") # descript. always starts with "About the job" header
    
    # FIXME
    # print("tmpList:\n", tmpList)
    # print("\n-----    tmpList[-1]\n", (tmpList[-1]))
    # /FIXME

    descrLines = tmpList[-1].split("\n")

    # FIXME
    # print("\npretty print of list:")
    # pprint.pprint(descrLines)
    # print("trying to get char at end of line:", descrLines[5][-1])
    # /FIXME

    # go through lines and split by section
    secs = []       # [ [section title, section content], [], ... ]
    secTitle = ""
    resStr = ""
    for line in descrLines:
        if re.search("[a-zA-Z]", line):     # check that line has letters in it
            if line[-1] == ":":
                tmp = [secTitle, resStr]
                # print("\ntmp:", tmp)      # FIXME

                secs.append(tmp)
                secTitle = line
                resStr = ""
                # print("stk after adding:", stk)

                # print("\nstck AFTER:", stk)
                # print("\nsecs:", secs)

            else:
                resStr += line
            # print(line)

    # print("pretty print of processing:")
    # pprint.pprint(secs)
    # print("test1:\n", correctStr(secs[-1][1]))
    # print("test2:\n", secs[-2][1])
    # print("test2:\n", repr(secs[-2][1]))

    # try named entity recognition on the job description
    # FIXME ?
    print("{: >50} {: >12} {: >12} {: >12}".format("token text",
                                                        "start char",
                                                        "end char",
                                                        "token label"))
    print("-" * 150)
    # /FIXME

    for sec in secs:
        # t = sec[1]
        # doc = nlp(t)
        doc = nlp(sec[1])
        for ent in doc.ents:
            # print up to `n` characters into separate columns i.e. `{: >n}`
            print("{: >50} {: >12} {: >12} {: >12}".format(ent.text,
                                                        ent.start_char,
                                                        ent.end_char,
                                                        ent.label_))
            # displacy.serve(doc)
    
    # a different approach: split by sentence
    # might want to go back and change how we store secs if this works better.
    for sec in secs:
        sents = sec[1].split(".")
        for s in sents:
            doc = nlp(s)
            for ent in doc.ents:
                # print up to `n` characters into separate columns i.e. `{: >n}`
                print("{: >50} {: >12} {: >12} {: >12}".format(ent.text,
                                                        ent.start_char,
                                                        ent.end_char,
                                                        ent.label_))
    
    # try a different pipeline I got from github haha
    diffNlp = spacy.load("en_core_web_md")
    # add pipeline
    diffNlp.add_pipe("entityLinker", last=True)

    for sec in secs:
        # doc = diffNlp(sec[1])
        # for sent in doc.sents:
        #     # sent._.linkedEntities.pretty_print()
        #     pass
        # # doc._.linkedEntities.print_super_entities()

        # for ent in doc._.linkedEntities:
        #     print("ent:", ent)
        #     superEnt = ent.get_super_entities()
        #     for sEnt in superEnt:
        #         d = str(sEnt.get_description())
        #         print("{: >50}\t{: <150}".format(sEnt.get_label(), d))

        seen = set()

        sents = sec[1].split(".")
        for s in sents:
            if re.search("[a-zA-Z]", s) == None:    # how effecient is this? should we just do the string processing and then test if the string is valid/long enough?
                continue
            
            tmp = ''.join(filter(lambda x: x in string.printable, s))
            tmp = tmp.strip()
            doc = diffNlp(tmp)

            for ent in doc._.linkedEntities:
                e_name = str(ent)
                if not (e_name in seen):
                    seen.add(e_name)
                    print(e_name)
                    superEnt = ent.get_super_entities()
                    for sEnt in superEnt:
                        lab = str(sEnt.get_label())
                        d = str(sEnt.get_description())
                        print("\t\t{: >30}\t{: <150}".format(lab, d))
