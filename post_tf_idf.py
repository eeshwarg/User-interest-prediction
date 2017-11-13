import cPickle
from sys import argv
import operator
import numpy as np
from sklearn.cluster import KMeans
import psutil
from sklearn.decomposition import PCA
import os
import shutil
from tf_idf import TF_IDF_FILE, VOCABULARY_FILE

# source_directory = argv[1]

MAX_NO_OF_DOCUMENTS = 1000      # Restrict the number of documents to be clustered to this value
MAX_CPU_USAGE_PERCENTAGE = 80
NO_OF_TERMS = 10    # Number of heaviest terms to be printed after clustering
# NO_OF_CLUSTERS = int(argv[2])

# Return a data structure after unpickling
def unpickle(file):
    return cPickle.load(open(file,'rb'))

# Construct a list corresponding to the terms' tf-idf values from the document's dictionary
def construct_doc_vector(doc_dict,vocabulary):
    v = []
    for word in vocabulary:
        if word in doc_dict:
            v.append(doc_dict[word])
        else:
            v.append(0)

    return v

# Get the tf-idf matrix
def construct_matrix(tf_idf,vocabulary):
    m = []
    docs = []
    count = 1
    for doc in tf_idf:
        docs.append(doc)
        m.append(construct_doc_vector(tf_idf[doc],vocabulary))
        # print "Appended",count,"documents' dictionaries"
        # usage = psutil.virtual_memory().percent
        # if usage > MAX_CPU_USAGE_PERCENTAGE or count >= MAX_NO_OF_DOCUMENTS:
        #     break
        count += 1

    return docs,np.array(m)

# Cluster documents into different folders based on similarity of tf-idf vectors
def cluster_docs_into_folders(tf_idf_matrix,docs_list,source_directory,NO_OF_CLUSTERS):
    pca = PCA()
    reduced = pca.fit_transform(tf_idf_matrix)
    # print tf_idf_matrix.shape
    # print reduced.shape

    kmeans = KMeans(n_clusters=NO_OF_CLUSTERS,random_state=0).fit(tf_idf_matrix)
    labels = kmeans.labels_

    # Create a differnt directory for each cluster
    for i in range(NO_OF_CLUSTERS):
        new_dir = 'cluster-'+str(i)
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        os.makedirs(new_dir)

    # Copy the documents from the original directory to the appropriate cluster directory
    for i in range(len(labels)):
        shutil.copyfile(source_directory+docs_list[i],'cluster-'+str(labels[i])+'/'+docs_list[i])

    labels, docs_list = zip(*sorted(zip(labels,docs_list)))

# Obtain the centroid of a collection(directory) of vectors(documents)
def average_tf_idf_over_docs(tf_idf,dir):
    average_tf_idf = {}
    no_of_docs = 0
    for doc in os.listdir(dir):
        no_of_docs += 1
        for word in tf_idf[doc]:
            if word not in average_tf_idf:
                average_tf_idf[word] = 0
            average_tf_idf[word] += tf_idf[doc][word]

    for word in average_tf_idf:
        average_tf_idf[word] /= no_of_docs

    return average_tf_idf

# Prints the top weighted terms of each cluster
def get_most_weighted_terms(tf_idf,no_of_terms,NO_OF_CLUSTERS):
    avg_tf_idf = []
    for i in range(NO_OF_CLUSTERS):
        avg_tf_idf.append(average_tf_idf_over_docs(tf_idf,'cluster-'+str(i)))

    # For each cluster, store the terms and their average tf-idf values in decreasing order of the tf-idf values as a list of 2-tuples
    sorted_tuples = []
    for i in range(len(avg_tf_idf)):
        sorted_tuples.append(sorted(avg_tf_idf[i].items(), key=operator.itemgetter(1),reverse=True))

    for i in range(len(sorted_tuples)):
        print "\nCluster",str(i+1)
        print "========="
        for j in range(NO_OF_TERMS):
            print str(sorted_tuples[i][j][0])
        print

def cluster(source_directory,NO_OF_CLUSTERS):
    vocabulary = unpickle(VOCABULARY_FILE)
    tf_idf = unpickle(TF_IDF_FILE)

    # print len(vocabulary)
    # print len(tf_idf)

    docs_list, tf_idf_matrix = construct_matrix(tf_idf,vocabulary)
    # print docs_list

    # print tf_idf_matrix.shape

    cluster_docs_into_folders(tf_idf_matrix,docs_list,source_directory,NO_OF_CLUSTERS)

    get_most_weighted_terms(tf_idf,NO_OF_TERMS,NO_OF_CLUSTERS)

if __name__ == '__main__':
    main()
