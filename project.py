import phonetics
import operator
def get_levenshtein_distance(word1, word2):
    """
    https://en.wikipedia.org/wiki/Levenshtein_distance
    :param word1:
    :param word2:
    :return:
    """
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

def check_phonetic(word):
	phonetic_dict={}
	one=phonetics.dmetaphone()
	for each in inverted_index:
		two=phonetics.dmetaphone()
		if one==two:
			phonetic_dict['each']=0
	return phonetic_dict
final=OrderedDict()
query=input().split()
positions=[]
for word in query:
	position=query.index(word)
	positions.append(position)
	a="list_"+str(position)
	if word in inverted_index:  #need to find inverted index list here
		final[a]=word
		continue
	else:
		phonetic_dict=check_phonetic(word)
		if(len(phonetic_dict)==0):
			#write some function afterwards
		else:
			edit_dict = dict(map(lambda x: (x[0], get_levenshtein_distance(query[position],x[1])), phonetic_dict.iteritems()))
			edit_list = sorted(dict_name.items(), key=operator.itemgetter(1))  #returns list of tuples
			final[a]=edit_list
			


	