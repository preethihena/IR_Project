#!/usr/bin/env python
import functools
import unicodedata,pickle
import os
import phonetics
# from nltk.stem import PorterStemmer
# from nltk.stem import LancasterStemmer
from tokenization import *


#Directory of this file
BASE_DIR  = os.path.dirname(os.path.realpath(__file__))
# Location of the files to be indexed
FILE_ROOT = os.path.join(BASE_DIR, 'inputFiles')


def soundex(query: str):

    # Step 0: Clean up the query string
    query = query.lower()
    letters = [char for char in query if char.isalpha()]

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If query contains only 1 letter, return query+"000" (Refer step 5)
    if len(query) == 1:
        return query + "000"

    to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    first_letter = letters[0]
    letters = letters[1:]
    letters = [char for char in letters if char not in to_remove]

    if len(letters) == 0:
        return first_letter + "000"

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    first_letter = [value if first_letter else first_letter for group, value in to_replace.items()
                    if first_letter in group]
    letters = [value if char else char
               for char in letters
               for group, value in to_replace.items()
               if char in group]

    # Step 3: Replace all adjacent same digits with one digit.
    letters = [char for ind, char in enumerate(letters)
               if (ind == len(letters) - 1 or (ind+1 < len(letters) and char != letters[ind+1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if first_letter == letters[0]:
        letters[0] = query[0]
    else:
        letters.insert(0, query[0])

    # Step 5: Append 3 zeros if result contains less than 3 digits.
    # Remove all except first letter and 3 digits after it.

    first_letter = letters[0]
    letters = letters[1:]

    letters = [char for char in letters if isinstance(char, int)][0:3]

    while len(letters) < 3:
        letters.append(0)

    letters.insert(0, first_letter)

    string = "".join([str(l) for l in letters])

    return string



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

    print("Type 'soundex' to create soundex_inverted_index:")

    print("Type 'dmetaphone' to create double_metaphone_inverted_index:")

    phonetic_type=input()

    if phonetic_type== 'soundex' or phonetic_type == 'dmetaphone':
        pass
    else:
        print("You entered wrong input")

    inverted = {}
    doc_ids_names={}
    
    doc_id = 1
    # Build Inverted-Index for documents
    for filename in os.listdir(FILE_ROOT):
        if filename.endswith(".txt") and doc_id <=2:
            doc_ids_names[doc_id]=filename
            file_location = os.path.join(FILE_ROOT, filename)
            doc_file = open(file_location,"r")
            print(filename)
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


    # for word, doc_locations in inverted.items():
    #     print (word, doc_locations)
