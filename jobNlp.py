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

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)


with open("jobDesc1.txt") as file:
    for line in file:
        # doc = nlp(line)
        # for token in doc:
        #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #             token.shape_, token.is_alpha, token.is_stop)
        print(line)