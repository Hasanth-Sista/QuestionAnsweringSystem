import sys, os
from features import * #, mlearning
import pysolr
import urllib
import json
import spacy
from nltk.corpus import wordnet as wn
# from nltk import sent_tokenize

def main():
    # f = open("dictionary.txt", encoding="utf8")
    # diction = f.read()
    # words_syns = diction.split()
    if len(sys.argv) != 1:
        print("Please give input text file with questions as input in command line")
    elif len(sys.argv) == 1:
        words_syns_dict = dict()
        # sentences = sent_tokenize(f.read())
        f = open("dictionary.txt", "r")
        for each_syn in f:
            word_sen, word_data = each_syn.split("__")
            if words_syns_dict.get(word_sen.lower()) is None:
                words_syns_dict[word_sen.lower()] = []
            words_syns_dict[word_sen.lower()].append(word_data.lower())

        nlp = spacy.load('en_core_web_lg')
        solr = pysolr.Solr('http://localhost:8983/solr/project_NLP')
        # print(words_syns_dict)
        # f = open(sys.argv[1], "r")
        super_list=[]
        # for q in f:
            
        # tokens = question.split(" ")
        question = "Where was Melinda born?"
        orig_question = question
        # question = q
        question=question[:-1]
        print(question)
        tokens = question.lower().split()
        entity_token=""
        to_find=""
        if "who" in tokens:
            entity_token = "PERSON:* or "
            to_find="who"
            # entity_search+=" AND ORG:*"
            # return ("PERSON", "NORP")
        elif "when" in tokens:
            to_find="when"
            # return ("DATE", "TIME", "CARDINAL")
        elif "where" in tokens:
            to_find="where"

        doc = nlp(question)

        entity_sent="("
        entity_sent+=entity_token
        # print(entity_sent)
        ent_len = len(doc.ents)
        local_len = 1
        for ent in doc.ents:
            # print(ent.text)
            ent_text_split = ent.text.split(" ")
            # entity_sent+= ent.label_+":"+ent_text_split[0]
            entity_sent+= ent.label_+":"+ent.text
            if words_syns_dict.get(ent.text.lower()) is not None:
                entity_sent+=" or "
                for x in words_syns_dict[ent.text.lower()]:
                    entity_sent+=ent.label_+":"+x+" or "
            if((words_syns_dict.get(ent.text) is None) and local_len!=ent_len):
                entity_sent+=" or "
            else:
                entity_sent+=")"
            local_len += 1
        # entity_sent+=")"
        local_len =1
        ent_len = len(doc)
        # print(ent_len)
        lemma_sent=" AND ("
        for token in doc:
            # print(str(token.pos_), str(token.lemma_),str(token.text))
            # if(token.lemma_!="who"and token.lemma_!="the" and token.lemma_!="is" and token.lemma_!="did" and token.lemma_!="do" and token.lemma_!="go" and token.lemma_!="what" and token.lemma_!="be" and token.lemma_!="in" and token.lemma_!="a" and token.lemma_!="and" and token.lemma_!="from" and token.lemma_!="when" and token.lemma_!="where"):
            if((token.pos_=="NOUN" or token.pos_=="NNS" or token.pos_=="VERB" or token.pos_=="PROPN") and token.text!="was" and token.text!="is" and token.text!="did"):
                lemma_sent+="( lemma"+":"+token.lemma_+" or "
                for ss in wn.synsets(token.text):
                    for l in ss.lemmas():
                        # synonyms.append(l.name())
                        lemma_sent+="lemma"+":"+l.name()+" or "
                if words_syns_dict.get(str(token.lemma_).lower()) is not None:
                    for x in words_syns_dict[str(token.lemma_).lower()]:
                        # for syns in x:
                        lemma_sent+="lemma"+":"+x+" or "
                lemma_sent = lemma_sent[:-3]
                lemma_sent+=")"
                if(local_len!=ent_len):
                    lemma_sent+=" AND "
                else:
                    lemma_sent+=")"
                
            local_len += 1
            
        
        # lemma_sent+=")"
        search_string = entity_sent+lemma_sent

        query_split = search_string.split()
        if(query_split[-1]=="AND"):
            query_split[-1]=""
            search_string=""
            for each in query_split:
                search_string+=each+" "
            search_string+=")"

        
        #PERSON:* AND ORG:Apple Inc. AND lemma:who AND lemma:found AND lemma:Apple AND lemma:Inc. AND lemma:? AND 
        # search_string = "PERSON:* AND ORG:Apple Inc. AND lemma:found AND lemma:Apple"
        print("here1", search_string)
        query_result = solr.search(search_string)

        # print(len(query_result))
        # print(type(query_result))
        
        answers_list=[]
        sentences_list=[]
        file_list=[]
        for result in query_result:
            if(to_find=="where"):
                if ('GPE' in result):
                    # print("The GPE '{0}'.".format(result['GPE']))
                    answers_list.append(result['GPE'])
                if ('ORDINAL' in result):
                    # print("The ORDINAL '{0}'.".format(result['ORDINAL']))
                    answers_list.append(result['ORDINAL'])
            elif(to_find=="who"):
                if ('ORG' in result):
                    # print("The ORG '{0}'.".format(result['ORG']))
                    answers_list.append(result['ORG'])
                if ('PERSON' in result):
                    # print("The PERSON '{0}'.".format(result['PERSON']))
                    answers_list.append(result['PERSON'])
            elif(to_find=="when"):
                if ('DATE' in result):
                    # print("The DATE '{0}'.".format(result['DATE']))
                    answers_list.append(result['DATE'])
                if ('TIME' in result):
                    # print("The TIME '{0}'.".format(result['TIME']))
                    answers_list.append(result['TIME'])
                if ('ORDINAL' in result):
                    # print("The ORDINAL '{0}'.".format(result['ORDINAL']))
                    answers_list.append(result['ORDINAL'])
            # print("The related sentences are '{0}'.".format(result['sentence']))
            sentences_list.append(result['sentence'])
            if(result['title'] not in file_list):
                file_list.append(result['title'])
            # print("The related sentences are '{0}'.".format(result['id']))

        super_list.append({"Question" : orig_question, "answers" : answers_list, "sentences" : sentences_list, "documents" : file_list})
        print(super_list)
        # with open('jsonFile.json', 'a') as outfile:  
        #     json.dump(super_list, outfile)
        #     outfile.write(",")

if __name__ == '__main__':
    main()