import spacy
import os, re
from nltk.corpus import wordnet as wn


def sentences_from_corpus(directory, file):
    sentences_in_file = []
    fileRead = open(directory + "/" + file, "r", encoding="utf8")
    fileText = fileRead.read()
    sentences = fileText.split("\n")
    for each_sentence in sentences:
        if len(each_sentence) > 0:
            sentences_in_file.append(each_sentence)
    return sentences_in_file


def tokenize(sentence):
    nlp = spacy.load('en_core_web_lg')
    doc = nlp(sentence)
    return doc


def tags(token):
    each_token = list()
    each_token.append(token.pos_)
    each_token.append(token.dep_)
    each_token.append(token.lemma_)
    each_token.append(token.tag_)
    # print(token.text, token.pos_, token.dep_, token.lemma_, token.tag_)
    return each_token


def entity(doc):
    entity_tags = []
    for ent in doc.ents:
        each_token = list()
        each_token.append(ent.text)
        each_token.append(ent.label_)
        entity_tags.append(each_token)
        # print(ent.text, ent.label_)
    return entity_tags


def get_entity(doc):
    entity_tags = []
    for ent in doc.ents:
        entity_tags.append(ent.label_)
    return entity_tags


def hypernyms(token):
    hypernym_tags = []
    try:
        for each_sense in wn.synsets(token.text):
            ss = wn.synset(each_sense.name())
            if len(ss.hypernyms()) > 0:
                hypernym_tags.append(ss.hypernyms())
    finally:
        return hypernym_tags


def hyponyms(token):
    hyponym_tags = []
    try:
        for each_sense in wn.synsets(token.text):
            ss = wn.synset(each_sense.name())
            if len(ss.hyponyms()) > 0:
                hyponym_tags.append(ss.hyponyms())
    finally:
        return hyponym_tags


def synonyms_antonyms(token):
    synonyms = []
    antonyms = []
    try:
        for ss in wn.synsets(token.text):
            for l in ss.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
    finally:
        return (set(synonyms), set(antonyms))


def meronyms(token):
    meronym_tags = []
    try:
        for ss in wn.synsets(token.text):
            if len(ss.part_meronyms()) > 0:
                meronym_tags.append(ss.part_meronyms())
    finally:
        return (meronym_tags)


def holonyms(token):
    holonym_tags = []
    try:
        for ss in wn.synsets(token.text):
            if len(ss.part_holonyms()) > 0:
                holonym_tags.append(ss.part_holonyms())
    finally:
        return (holonym_tags)


def corpusFeatures():
    directory = "WikipediaArticles"
    directoryFiles = os.listdir(directory)
    corpus_features = dict()
    for file in directoryFiles:
        fileOpen = open("Task1/" + file, "w+", encoding="utf8")
        sentences_in_file = sentences_from_corpus(directory, file)
        fileOpen.write("Document is :   " + file +"\n\n\n")
        for each_sentence in sentences_in_file:
            doc = tokenize(each_sentence)
            fileOpen.write("Sentence is :  \n")
            fileOpen.write(str(doc))
            fileOpen.write("\n\n\n")

            entity_tags = entity(doc)
            fileOpen.write("Entities are :  FORMAT: ent.text, ent.label_ \n")
            fileOpen.write(str(entity_tags))
            fileOpen.write("\n\n\n")

            corpus_features[file].append(each_sentence, get_entity(doc))

            for token in doc:
                fileOpen.write("\nToken is : "+str(token.text)+"\n")
                doc_tags = tags(token)
                fileOpen.write("Tags are : ")
                fileOpen.write(str(doc_tags)+"\n")

                hypernym_tags = hypernyms(token)
                fileOpen.write("Hypernym Tags are :")
                fileOpen.write(str(hypernym_tags)+"\n")

                hyponym_tags = hyponyms(token)
                fileOpen.write("Hyponym Tags are :")
                fileOpen.write(str(hyponym_tags)+"\n")

                synonyms_antonyms_tags = synonyms_antonyms(token)
                fileOpen.write("Synonym and Antonym Tags are :")
                fileOpen.write(str(synonyms_antonyms_tags)+"\n")

                meronym_tags = meronyms(token)
                fileOpen.write("Meronyms Tags are :")
                fileOpen.write(str(meronym_tags)+"\n")

                holonym_tags = holonyms(token)
                fileOpen.write("Holonym Tags are :")
                fileOpen.write(str(holonym_tags)+"\n")
            fileOpen.write("\n\n\n")
        break
    return corpus_features
