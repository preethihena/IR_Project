import phonetics
import operator
import pickle
from collections import OrderedDict

# open a file, where you stored the pickled data
file = open('indexed', 'rb')

# dump information to that file
inverted_index = pickle.load(file)

# close the file
file.close()
retrieved_docs_list=[]
def get_levenshtein_distance(word1, word2):

    print type(word1)
    print type(word2)
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

def check_phonetic(word):
    phonetic_dict={}
    one=phonetics.dmetaphone(word)
    for each in inverted_index:
        two = inverted_index[each][0]
        if (one[0] in two and len(one[0])>0) or (one[1] in two and len(one[1])>0):
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



final=OrderedDict()
query=raw_input('Enter query:').split(' ')
positions=[]
flag=0
for word in query:
    position=query.index(word)
    positions.append(position)
    name="list_"+str(position)
    if word in inverted_index:  #need to find inverted index list here
        final[name]=[(word,-1)]
        retrieve_docs(word)
        continue
    else:
        flag=1
        phonetic_dict=check_phonetic(word)
        print phonetic_dict
        if(len(phonetic_dict)==0):
            #write some function afterwards
            continue
        else:
            edit_dict = dict(map(lambda x: (x[0], get_levenshtein_distance(query[position],x[0])), phonetic_dict.iteritems()))
            edit_list = sorted(edit_dict.items(), key=operator.itemgetter(1))  #returns list of tuples
            final[name]=edit_list
            retrieve_docs(str(final[name][0][0]))

            
print final
if flag==1:
    print  "Your suggested query is:" 
    print form_final_query(final)

print retrieved_docs_list

final_doc_set = set.union(*retrieved_docs_list)
print final_doc_set

# for word, doc_locations in inverted.items():
#     print (word, doc_locations)




    