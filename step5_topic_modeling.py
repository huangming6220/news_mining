# -*- coding: utf-8 -*-

###############################################################################
# Run topic modeling with TKM
# Change the file path in line 40
# the codes from line 74 for visualizing the topics with PyLDA

# TKM Paper: Topic modeling based on Keywords and Context
# Please cite: https://arxiv.org/abs/1710.02650 (accepted at SDM 2018)
###############################################################################

import TKMCore
import algTools
import os

def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # os.rename(fullPath, fullPath.replace(' ', '_'))
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles

def readBrownDataset():
    # mypath = '/home/sgnbx/Downloads/poverty/allfiles'
    # for f in os.listdir(mypath):
    #     os.rename(os.path.join(mypath, f),os.path.join(mypath, f.replace(' ','_')))
    #
    # onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if isfile(os.path.join(mypath, f))]
    documents = getListOfFiles('output/news')
    # print (documents)
    docs=[]
    import re
    for d in documents:

        with open(d, 'r') as fi:
                d= fi.read().replace("\n"," ")
                d=re.sub(r"/[A-Za-z0-9_-]+ "," ",d)#   The/at Fulton/np-tl County/nn-tl Grand/jj-tl Jury/nn-tl said/vbd Friday/nr an/at investigation/nn") #.replace("/at","").replace("/nn-tl","").replace("/nn-hp","").replace("/np-hl","").replace("/nn","").replace("/vbd","").replace("/in","").replace("/jj","").replace("/hvz","").replace("/cs","").replace("/nps","").replace("/nr","").replace("/np-tl","").replace("/md","").replace("/np","").replace("/cd-hl","").replace("/vbn","").replace("/np-tl","").replace("/dti","").replace("--/--","")
                docs.append(d)
    return docs

print("\nDownloading test data set using Python's NLTK library...")
docs = readBrownDataset()
print("\nPreprocessing data set...")
# Transform data set with words into sequence of numbers
m_docs, id2word,word2id,wordfreq = algTools.process_corpus(docs)
# print(m_docs)
# print(id2word)
# print(word2id)
list_vocab = []
list_freq = []
for i,j in wordfreq:
    list_vocab.append(i)
    list_freq.append(j)

# print([id2word[_id] for _id in m_docs[0][:50]])
# print(["{}: {}".format(_id, word) for _id, word in id2word.items()][:10])
print("\nRunning TKM... - Takes 1 - 2 minutes")
tkmc = TKMCore.TKMCore(
    m_docs=m_docs,
    n_words=len(id2word),
    n_topics=30,
    winwid=7,
    alpha=7,
    beta=0.08
)

import numpy as np
p_d_t,dl = tkmc.run(convergence_constant=0.08, mseed=4848)
print("\nPrinting Topics with Human Weights...")
algTools.print_topics(p_w_t=tkmc.get_f_w_t_hu(), id2word=id2word)

## visualization
#theta = p_d_t
#phi = tkmc.get_f_w_t_hu()
#phi = phi.transpose()
#
#import pyLDAvis
#
#data = {'topic_term_dists': phi,
#        'doc_topic_dists': theta,
#        'doc_lengths': dl,
#        'vocab': list_vocab,
#        'term_frequency': list_freq
#       }
#vis_data = pyLDAvis.prepare(**data)
#pyLDAvis.show(vis_data)