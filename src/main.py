import sys, os
from features import * #, mlearning
import pysolr
import urllib
import json
import spacy
from nltk import sent_tokenize

def main():
    nlp = spacy.load('en_core_web_lg')
    #read input file from command line
    if len(sys.argv) != 1:
        print("Please give input text file with questions as input in command line")
    elif len(sys.argv) == 1:
        # inputFilePath = sys.argv[1]
        # questions = []
        # fileRead = open(inputFilePath, "r", encoding="latin-1")
        # # fileText = fileRead.read()
        # # nlp = spacy.load('en_core_web_lg')
        # doc = nlp(fileRead.read())
        # # sentences = list(doc.sents)
        # # sentences = fileText.split("\n")
        # # nlt = sent_tokenize(fileRead.read())
        # # for each_sentence in sentences:
        # #     questions.append(str(each_sentence).strip())

        cp = corpus()
        # TASK 1 commented as it takes lot of time
        cp.corpusFeatures()


        # TASK 2
        solr = pysolr.Solr('http://localhost:8983/solr/project_NLP')
        directory = "..\\WikipediaArticles"
        directoryFiles = os.listdir(directory)
        counter = 1
        for file in directoryFiles:
            # fileRead = open(directory + "/" + file, "r", encoding="ISO-8859-1")
            # print(file)
            if(file=="MelindaGates.txt"):
                fileRead = open(directory + "/" + file, "r", encoding="latin-1")
            else:
                fileRead = open(directory + "/" + file, "r", encoding="utf8")
            # fileText = fileRead.read()
            # sentences = fileText.split("\n")
            # doc = nlp(fileRead.read())
            # sentences = list(doc.sents)
            # sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
            # print(sentences)
            # nlt = sent_tokenize(fileRead.read())
            
            sentences = sent_tokenize(fileRead.read())
            solr_json_doc = []
            for each_sentence in sentences:
                counter=counter+1
                each = nlp(each_sentence)
                # each = each_sentence
                sentence_json_doc = {}
                sentence_json_doc['id'] = counter
                sentence_json_doc['title'] = file
                sentence_json_doc['sentence'] = each_sentence

                for entity in each.ents:
                    if entity.label_ not in sentence_json_doc:
                        sentence_json_doc[entity.label_] = []
                    # print(entity.label_," ",entity.text)
                    sentence_json_doc[entity.label_].append(entity.text)

                sentence_json_doc['lemma'] = []
                for token in each:
                    sentence_json_doc['lemma'].append(token.lemma_)
                
                sentence_json_doc['pos'] = []
                for token in each:
                    sentence_json_doc['pos'].append(token.pos_)
                
                sentence_json_doc['dependecy_parse'] = []
                for token in each:
                    sentence_json_doc['dependecy_parse'].append(token.dep_)
                
                solr_json_doc.append(sentence_json_doc)
                # doc = cp.tokenize(str(each))
                # entity_tags = cp.entity(doc)
                # print(len(each_sentence))
                # if len(each_sentence) > 0:
                #     solr.add([{"id" : counter, "title" : file, "sentence" : each_sentence, "entity" : entity_tags}],commit=True)
                    # jsonFile.append([{"id" : file, "sentence" : each_sentence, "entity" : entity_tags}])
                    # with open('jsonFile.json', 'a') as outfile:  
                    #     json.dump({"id" : file, "sentence" : str(each_sentence), "entity" : entity_tags}, outfile)
                    #     outfile.write(",")
            solr.add(solr_json_doc)       

            # break


    else:
        print("Command incorrect. Please give correct input the program")

if __name__ == '__main__':
    main()
