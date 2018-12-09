import phonetics
import operator
import pickle
from collections import OrderedDict
from tokenization import * 
from difflib import SequenceMatcher


retrieved_docs_list=[]

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





def get_levenshtein_distance(word1, word2):
    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    for x in range(1, len(word1) + 1):
        for y in range(1, len(word2) + 1):
            if word1[x - 1] == word2[y - 1]:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else:
                matrix[x][y] = min(
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1,
                    matrix[x][y - 1] + 1
                )

    return matrix[len(word1)][len(word2)]


# def check_phonetic(word):
#     phonetic_dict={}
#     one=set(phonetics.dmetaphone(word))
#     for each in inverted_index:
#         two = set(inverted_index[each][0])
#         common_hash = one.intersection(two)
#         if ((len(common_hash)==1 and common_hash.pop()!=' ') or bool(common_hash)!=False): 
#             phonetic_dict[each]=-1
#     return phonetic_dict

def check_phonetic(word,phonetic_type):
    phonetic_dict={}
    if phonetic_type=="dmetaphone":
        one=phonetics.dmetaphone(word)
        for each in inverted_index:
            two = inverted_index[each][0]
            if (one[0] in two and len(one[0])>0) or (one[1] in two and len(one[1])>0):
                phonetic_dict[each]=-1
    else:
        one=soundex(word)
        for each in inverted_index:
            two = inverted_index[each][0]
            if one==two:
                phonetic_dict[each]=-1
    return phonetic_dict


def form_final_query(final):
    final_query=[]
    for word in final:
        final_query.append(str(final[word][0][0]))
    final_query=' '.join(final_query)
    return final_query


def retrieve_docs(word):
    set_of_docs=set()
    if word.isdigit():
        pass
    else:
        for doc in inverted_index[word][1]:
            set_of_docs.add(doc)
        retrieved_docs_list.append(set_of_docs)

def check_similarity(word):
    similarity_dict={}
    for each in inverted_index:
        ans=SequenceMatcher(a=word,b=each).ratio()
        similarity_dict[each]=ans
    return similarity_dict



print("Type 'soundex' to use soundex_inverted_index:")

print("Type 'dmetaphone' to use double_metaphone_inverted_index:")

phonetic_type=input()
# open a file, where inverted index is stored
if phonetic_type =="soundex":
    file = open('soundex_index', 'rb')
elif phonetic_type =="dmetaphone":
    file = open('dmetaphone_index', 'rb')
else:
    print("You entered wrong input")

# get the informationh from file
inverted_index = pickle.load(file)

# close the file
file.close()

final=OrderedDict()
query=input('Enter query:\n')
changed_query = [word for _, word in word_index(query)]
#print(changed_query)
query=query.split()
positions=[]
flag=0
for word in query:
    position=query.index(word)
    positions.append(position)
    name="list_"+str(position)
    if word not in changed_query:
        final[name]=[(word,-1)]
    else:
        if word in inverted_index:  
            final[name]=[(word,-1)]
            retrieve_docs(word)
        else:
            flag=1
            phonetic_dict=check_phonetic(word,phonetic_type)
            #print(phonetic_dict)
            if(len(phonetic_dict)==0):
                similarity_dict=check_similarity(word)
                similarity_list=sorted(similarity_dict.items(), key=operator.itemgetter(1) , reverse=True)
                #print(similarity_list)
                #edit_list=list(map(lambda x:(x[0],x[1],get_levenshtein_distance(word,x[0])),similarity_list[:5]))
                #print(edit_list)
                final[name]=similarity_list
                retrieve_docs(str(final[name][0][0]))
            else:
                edit_dict = dict(map(lambda x: (x[0], get_levenshtein_distance(word,x[0])), phonetic_dict.items()))
                edit_list = sorted(edit_dict.items(), key=operator.itemgetter(1))  #returns list of tuples
                final[name]=edit_list
                retrieve_docs(str(final[name][0][0]))

            
#print (final)
if flag==1:
    print ("Your suggested query from our limited vocabulary is:") 
    print (form_final_query(final))

#print (retrieved_docs_list)

final_doc_set = set.union(*retrieved_docs_list)
print(final_doc_set)

# for word, doc_locations in inverted.items():
#     print (word, doc_locations)

file1 =open('Documents_info', 'rb')
doc_ids_names=pickle.load(file1)
file1.close()

for doc_id in final_doc_set:
    doc_name=doc_ids_names[doc_id]
    print(doc_id,'.',doc_name)





    