import nltk
import corenlp
import spacy
import os
from spacy.lang.en import English
from spacy.pipeline import DependencyParser
from spacy.tokenizer import Tokenizer
from nltk.corpus import wordnet as wn


def sentences_from_corpus(directory):
    sentences_in_corpus = []
    directoryFiles = os.listdir(directory)
    for file in directoryFiles:
        fileRead = open(directory + "/" + file, "r", encoding="utf8")
        fileText = fileRead.read()
        sentences = fileText.split("\n")
        for each_sentence in sentences:
            if len(each_sentence) > 0:
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
    for each_sentence in sentences_in_corpus:
        doc = each_sentence.split(" ")
        for token in doc:
            for ss in wn.synsets(token):
                print(ss)
                print(ss, ss.hypernyms())
                print(ss, ss.hyponyms())
                synonyms = []
                antonyms = []
                for l in ss.lemmas():
                    synonyms.append(l.name())
                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name())
                print(synonyms)
                print(antonyms)
                print(ss, ss.part_meronyms())
                print(ss, ss.part_holonyms())


def main():
    directory = "WikipediaArticles"
    # get all sentences from corpus
    sentences_in_corpus = sentences_from_corpus(directory)
    # tokenize, lemmatize and dependency parsing
    tokenize(sentences_in_corpus)
    # get all features using wordnet
    features_from_wordnet(sentences_in_corpus)


if __name__ == '__main__':
    main()
