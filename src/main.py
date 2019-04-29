import sys, os
import features, mlearning
import pysolr
import urllib
import json
import spacy

def main():
    #read input file from command line
    if len(sys.argv) != 2:
        print("Please give input text file with questions as input in command line")
    elif len(sys.argv) == 2:
        inputFilePath = sys.argv[1]
        questions = []
        fileRead = open(inputFilePath, "r", encoding="latin-1")
        # fileText = fileRead.read()
        nlp1 = spacy.load('en_core_web_lg')
        doc1 = nlp1(fileRead.read())
        sentences = list(doc1.sents)
        # sentences = fileText.split("\n")
        for each_sentence in sentences:
            questions.append(each_sentence.strip())


        # TASK 1 commented as it takes lot of time
        #features.corpusFeatures()


        # TASK 2
        solr = pysolr.Solr('http://localhost:8983/solr/projectNLP')
        directory = "..\\WikipediaArticles"
        directoryFiles = os.listdir(directory)
        for file in directoryFiles:
            fileRead = open(directory + "/" + file, "r", encoding="ISO-8859-1")
            # fileText = fileRead.read()
            # sentences = fileText.split("\n")
            doc1 = nlp1(fileRead.read())
            sentences = list(doc1.sents)
            # print(sentences)
            for each_sentence in sentences:
                print(each_sentence)
                doc = features.tokenize(str(each_sentence))
                entity_tags = features.entity(doc)
                if len(each_sentence) > 0:
                    #solr.add([{"id" : file, "sentence" : each_sentence, "entity" : entity_tags}])
                    # jsonFile.append([{"id" : file, "sentence" : each_sentence, "entity" : entity_tags}])
                    with open('jsonFile.json', 'a') as outfile:  
                        json.dump({"id" : file, "sentence" : str(each_sentence), "entity" : entity_tags}, outfile)
                        outfile.write(",")
                    

            break


    else:
        print("Command incorrect. Please give correct input the program")


if __name__ == '__main__':
    main()
