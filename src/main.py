import nltk
import corenlp
import spacy
import os
from spacy.lang.en import English
from spacy.pipeline import DependencyParser
from spacy.tokenizer import Tokenizer
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.corpus import wordnet as wn



def sentences_from_corpus(directory):
    sentences_in_corpus = []
    directoryFiles = os.listdir(directory)
    for file in directoryFiles:
        fileRead = open(directory + "/" + file, "r")
        fileText = fileRead.read()
        sentences = fileText.split("\n")
        for each_sentence in sentences:
            if len(each_sentence) != 0:
                sentences_in_corpus.append(each_sentence)
    return sentences_in_corpus


def tokenize(sentences_in_corpus):
    nlp = spacy.load('en_core_web_sm')
    for each_sentence in sentences_in_corpus:
        doc = nlp(each_sentence)
        for token in doc:
            print(token.text, token.pos_, token.dep_, token.lemma_, token.tag_)
        for ent in doc.ents:
            print(ent.text, ent.label_)


def features_from_wordnet(sentences_in_corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
    for each_sentence in sentences_in_corpus:
        doc = nlp(each_sentence)
        for token in doc:
            print(token._.wordnet.synsets())

    # wordnet object link spacy token with nltk wordnet interface by giving acces to
    # synsets and lemmas
    token._.wordnet.synsets()
    token._.wordnet.lemmas()

    # And automatically tags with wordnet domains
    token._.wordnet.wordnet_domains()


def main():
    directory = "..\\WikipediaArticles"
    # get all sentences from corpus
    sentences_in_corpus = sentences_from_corpus(directory)
    # tokenize, lemmatize and dependency parsing
    tokenize(sentences_in_corpus)
    # get all features using wordnet
    # features_from_wordnet(sentences_in_corpus)
    # read each file
    # parser = nlp.create_pipe("parser")
    # nlp.add_pipe(parser)
    #
    # print(tokens)

    # tokenized_text = sentence.split(" ")
    # pos tags for words in sentences
    # pos_tags = nltk.pos_tag(tokens)
    # dependecy parser

    # parser = DependencyParser(nlp.vocab)
    # doc = nlp("This is a sentence.")
    # This usually happens under the hood
    # processed = parser(doc)
    # nlp.begin_training()
    # print(processed)

    #
    # #wordnet functions
    # synonyms = []
    # antonyms = []
    #
    # for syn in wn.synsets("good"):
    #     for l in syn.lemmas():
    #         synonyms.append(l.name())
    #         if l.antonyms():
    #             antonyms.append(l.antonyms()[0].name())
    #
    # # print(set(synonyms))
    # # print(set(antonyms))
    #
    # break


# NEXT TO DO:
# 1. Dependency Parser
# 2. Features using WordNet

if __name__ == '__main__':
    main()
