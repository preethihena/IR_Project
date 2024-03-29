#!/usr/bin/env python
import functools
import unicodedata,pickle
import os
import phonetics
# from nltk.stem import PorterStemmer
# from nltk.stem import LancasterStemmer
from tokenization import *
from soundex import soundex

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
        if phonetic_type =='dmetaphone':
            phonetic_hash = phonetics.dmetaphone(word)
        elif phonetic_type == 'soundex':
            phonetic_hash = soundex(word)
        indices = inverted.setdefault(word, (phonetic_hash,{}))
        indices[1][doc_id] = locations
    return inverted


if __name__ == '__main__':
    phonetic_dict = {'1':'soundex','2':'dmetaphone'}

    print("Type '1' to create soundex_inverted_index:")

    print("Type '2' to create double_metaphone_inverted_index:")

    phonetic_type=phonetic_dict.get(input(),None)

    if phonetic_type== 'soundex' or phonetic_type == 'dmetaphone':
        inverted = {}
        doc_ids_names={}
        
        doc_id = 1
        # Build Inverted-Index for documents
        for filename in os.listdir(FILE_ROOT):
            if filename.endswith(".txt"):
                doc_ids_names[doc_id]=filename
                file_location = os.path.join(FILE_ROOT, filename)
                doc_file = open(file_location,"r")
                # print(filename)
                text = doc_file.read()
                doc_index = inverted_index(text)
                inverted_index_add(inverted, doc_id, doc_index)
                doc_id += 1

        #open file to store the index
        if phonetic_type == 'soundex':
            file = open('soundex_index', 'wb')
        else:
            file = open('dmetaphone_index', 'wb')

        # dump information to that file
        pickle.dump(inverted, file)

        # close the file
        file.close()

        file1 = open('Documents_info','wb')
        pickle.dump(doc_ids_names, file1)
        file1.close()
        print("{} files Indexed by {} algorithm.".format(doc_id,phonetic_type))
    else:
        print("You entered wrong input")


    


    # for word, doc_locations in inverted.items():
    #     print (word, doc_locations)
