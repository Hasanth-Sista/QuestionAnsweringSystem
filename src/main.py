import nltk
import corenlp
from spacy.lang.en import English
from spacy.pipeline import DependencyParser
from spacy.tokenizer import Tokenizer
import spacy
import os
from nltk.corpus import wordnet as wn


def tokenizer(directory):
    tokens = dict()
    directoryFiles = os.listdir(directory)
    for file in directoryFiles:
        fileRead = open(directory + "/" + file, "r")
        fileText = fileRead.read()
        sentences = fileText.split("\n")
        for each_sentence in sentences:
            if len(each_sentence) != 0:
                # words in each sentence
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(each_sentence)
                for parsed_token in doc:
                    if parsed_token.text in tokens:
                        x = tokens.get(parsed_token)
                        x.append(parsed_token.pos_)
                    else:
                        tokens[parsed_token.text] = parsed_token.pos_
                        # print(token.text, token.pos_, token.dep_)


def main():
    directory = "WikipediaArticles"

    # tokenize, lemmatize and dependency parsing
    tokenizer(directory)

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
