# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
# from collections import Counter
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import nltk
import features


def findTfid(totalCount, contextCount):
    return (contextCount/totalCount)


def countOfContext(file, question):
    doc = features.tokenize(question)
    entity_tags = features.entity(doc)
    count = 0
    for tag in entity_tags:
        count += file.count(tag[0])
    return count


def tokensInFile(file):
    return len(nltk.Text(file))

