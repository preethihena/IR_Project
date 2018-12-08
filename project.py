import phonetics
import operator
import pickle

# open a file, where you stored the pickled data
file = open('indexed', 'rb')

# dump information to that file
inverted_index = pickle.load(file)

# close the file
file.close()
def get_levenshtein_distance(word1, word2):

def check_phonetic(word):
    phonetic_dict={}
    one=phonetics.dmetaphone(word)
    for each in inverted_index:
        two = inverted_index[each][0]
        if (one[0] in two and len(one[0])>0) or (one[1] in two and len(one[1])>0):
            phonetic_dict[each]=-1
    return phonetic_dict


# final=OrderedDict()
# query=input().split()
# positions=[]
# for word in query:
#     position=query.index(word)
#     positions.append(position)
#     name="list_"+str(position)
#     if word in inverted:  #need to find inverted index list here
#         final[name]=word
#         continue
#     else:
#         phonetic_dict=check_phonetic(word)
#         if(len(phonetic_dict)==0):
#             #write some function afterwards
#         else:
#             edit_dict = dict(map(lambda x: (x[0], get_levenshtein_distance(query[position],x[1])), phonetic_dict.iteritems()))
#             edit_list = sorted(dict_name.items(), key=operator.itemgetter(1))  #returns list of tuples
#             final[name]=edit_list
            

for word, doc_locations in inverted.items():
    print (word, doc_locations)


    