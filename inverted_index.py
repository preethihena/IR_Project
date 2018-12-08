#!/usr/bin/env python
import functools
import unicodedata,pickle
import os
import phonetics
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from tokenization import *


#Directory of this file
BASE_DIR  = os.path.dirname(os.path.realpath(__file__))
# Location of the files to be indexed
FILE_ROOT = os.path.join(BASE_DIR, 'inputFiles')

def inverted_index(text):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """
    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted



def inverted_index_add(inverted, doc_id, doc_index):
    """
    Add Invertd-Index doc_index of the document doc_id to the 
    Multi-Document Inverted-Index (inverted), 
    using doc_id as document identifier.
        {word:(hash,{doc_id:[locations]})}
    """

    # porter = PorterStemmer()
    # lancaster=LancasterStemmer()
    for word, locations in doc_index.items():
    	# word = porter.stem(word)
    	# word = lancaster.stem(word)
        phonetic_hash = phonetics.dmetaphone(word)
        indices = inverted.setdefault(word, (phonetic_hash,{}))
        indices[1][doc_id] = locations
    return inverted


if __name__ == '__main__':

    inverted = {}
    
    doc_id = 1
    # Build Inverted-Index for documents
    for filename in os.listdir(FILE_ROOT):
        if filename.endswith(".txt") and doc_id <=2:
            file_location = os.path.join(FILE_ROOT, filename)
            file = open(file_location,"r")
            text = file.read()
            doc_index = inverted_index(text)
            inverted_index_add(inverted, doc_id, doc_index)
            doc_id += 1

    #open file to store the index
    file = open('indexed', 'wb')
    # dump information to that file
    pickle.dump(inverted, file)

    # close the file
    file.close()

    # for word, doc_locations in inverted.items():
    #     print (word, doc_locations)
