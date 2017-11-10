from __future__ import division
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sys import argv
import cPickle
from collections import defaultdict
import os
import math

stop_words = set(stopwords.words('english'))

def pickleDictionary(dict,file):
    with open(file,'wb') as f:
        cPickle.dump(dict,f)
    f.close()

# Get the term frequency of terms in a document
def index_doc(input_dir,file,df):
    doc_terms = {}
    tokenizer = RegexpTokenizer(r'\w+')
    with open(input_dir+file,'r') as f:
        for line in f:
            for word in tokenizer.tokenize(line.decode('utf8')):
                word = word.lower()
                if word not in stop_words:
                    if word not in doc_terms:
                        doc_terms[word] = 1
                        df[word] += 1
                    else:
                        doc_terms[word] += 1
    f.close()
    return doc_terms

# Compute the tf_idf value of terms given the term frequencies and inverse docuement frequencies
def compute_tf_idf(tf_in_docs,idf):
    tf_idf = {}         # A dictionary of dictionaries that stores the tf-idf values of all terms in documents
    for doc in tf_in_docs:
        t = tf_in_docs[doc]
        tf_idf[doc] = {}
        norm = 0
        for word in t:
            tf_idf[doc][word] = t[word] * idf[word]
            norm += tf_idf[doc][word]**2
        norm = norm**0.5
        for word in t:
            tf_idf[doc][word] /= norm

    return tf_idf

def main():
    input_dir = argv[1]

    tf_in_docs = {}     # A dictionary of dictionaries that stores the term frequencies for all the documents in the collection
    df = defaultdict(int)       # A dictionary that stores the number of documents each term in the vocabulary appears in

    for file in os.listdir(input_dir):
        if file.endswith(".txt"):
            tf_in_docs[file] = index_doc(input_dir,file,df)

    no_of_docs = len(tf_in_docs)
    idf = {}
    for term in df:
        idf[term] = math.log(no_of_docs/df[term])

    tf_idf = compute_tf_idf(tf_in_docs,idf)

    pickleDictionary(tf_idf,'tf_idf.txt')
    pickleDictionary(idf,'idf.txt')

if __name__ == '__main__':
    main()
