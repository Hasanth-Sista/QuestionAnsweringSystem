import sys, os
from features import * #, mlearning
import pysolr
import urllib
import json
import spacy

def main():
    nlp = spacy.load('en_core_web_lg')
    #read input file from command line
    if len(sys.argv) != 2:
        print("Please give input text file with questions as input in command line")
    elif len(sys.argv) == 2:
        inputFilePath = sys.argv[1]
        questions = []
        fileRead = open(inputFilePath, "r", encoding="latin-1")
        # fileText = fileRead.read()
        # nlp1 = spacy.load('en_core_web_lg')
        doc = nlp(fileRead.read())
        sentences = list(doc.sents)
        # sentences = fileText.split("\n")
        for each_sentence in sentences:
            questions.append(str(each_sentence).strip())

        cp = corpus()
        # TASK 1 commented as it takes lot of time
        # cp.corpusFeatures()

        # TASK 2
        solr = pysolr.Solr('http://localhost:8983/solr/projectNLP')
        directory = "WikipediaArticles"
        directoryFiles = os.listdir(directory)
        counter = 1
        for file in directoryFiles:
            fileRead = open(directory + "/" + file, "r", encoding="ISO-8859-1")
            # fileText = fileRead.read()
            # sentences = fileText.split("\n")
            doc = nlp(fileRead.read())
            sentences = list(doc.sents)
            # print(sentences)
            for each_sentence in sentences:
                # print(each_sentence)
                doc = cp.tokenize(str(each_sentence))
                entity_tags = cp.entity(doc)
                # print(len(each_sentence))
                if len(each_sentence) > 0:
                    solr.add([{"id" : counter, "title" : file, "sentence" : each_sentence, "entity" : entity_tags}],commit=True)
                    counter = counter + 1
                    # jsonFile.append([{"id" : file, "sentence" : each_sentence, "entity" : entity_tags}])
                    # with open('jsonFile.json', 'a') as outfile:  
                    #     json.dump({"id" : file, "sentence" : str(each_sentence), "entity" : entity_tags}, outfile)
                    #     outfile.write(",")

            # break
    else:
        print("Command incorrect. Please give correct input the program")


if __name__ == '__main__':
    main()
