import nltk
import os

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
                tokenized_text = sentence.split(" ")
                # pos tags for words in sentences
                pos_tags = nltk.pos_tag(tokenized_text)
       # dummy.write(str(pos_tags) + "\n\n")


# NEXT TO DO:
# 1. Dependency Parser
# 2. Features using WordNet

if __name__ == '__main__':
    main()
