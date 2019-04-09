import nltk
import corenlp

from spacy.lang.en import English
from spacy.pipeline import DependencyParser

import spacy
import os
from nltk.corpus import wordnet as wn

def main():
    # read directory and list all files
    directory = "WikipediaArticles"
    directoryFiles = os.listdir(directory)

    # read each file and split into sentences
    for file in directoryFiles:
        fileRead = open(directory + "/" + file, "r")
        text = fileRead.read()
        text = text.split("\n")
        # dummy = open("src/dummy1.txt", "w")
        for sentence in text:
            if sentence != '' and sentence != [] and len(sentence) != 0:
                # words in each sentence
                tokenized_text = sentence.split(" ")
                # pos tags for words in sentences
                pos_tags = nltk.pos_tag(tokenized_text)
                #dependecy parser

                nlp = English()
                parser = nlp.create_pipe("parser")
                parser = DependencyParser(nlp.vocab)
                doc = nlp("This is a sentence.")
                # This usually happens under the hood
                processed = parser(doc)
                nlp.begin_training()
                print(processed)

                #wordnet functions
                synonyms = []
                antonyms = []

                for syn in wn.synsets("good"):
                    for l in syn.lemmas():
                        synonyms.append(l.name())
                        if l.antonyms():
                            antonyms.append(l.antonyms()[0].name())

                # print(set(synonyms))
                # print(set(antonyms))

                break

       # dummy.write(str(pos_tags) + "\n\n")


# NEXT TO DO:
# 1. Dependency Parser
# 2. Features using WordNet

if __name__ == '__main__':
    main()
