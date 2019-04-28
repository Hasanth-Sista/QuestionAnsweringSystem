import sys, os
import features, mlearning
import pysolr
import urllib
import json

def main():
    #read input file from command line
    if len(sys.argv) != 2:
        print("Please give input text file with questions as input in command line")
    elif len(sys.argv) == 2:
        inputFilePath = sys.argv[1]
        questions = []
        fileRead = open(inputFilePath, "r", encoding="latin-1")
        fileText = fileRead.read()
        sentences = fileText.split("\n")
        for each_sentence in sentences:
            questions.append(each_sentence.strip())


        # TASK 1 commented as it takes lot of time
        features.corpusFeatures()


        # TASK 2
        solr = pysolr.Solr('http://localhost:8983/solr/project')
        directory = "WikipediaArticles"
        directoryFiles = os.listdir(directory)
        for file in directoryFiles:
            fileRead = open(directory + "/" + file, "r", encoding="ISO-8859-1")
            fileText = fileRead.read()
            sentences = fileText.split("\n")
            for each_sentence in sentences:
                doc = features.tokenize(each_sentence)
                entity_tags = features.entity(doc)
                if len(each_sentence) > 0:
                    solr.add([{"id" : file, "sentence" : each_sentence, "entity" : entity_tags}])
            break


    else:
        print("Command incorrect. Please give correct input the program")


if __name__ == '__main__':
    main()
