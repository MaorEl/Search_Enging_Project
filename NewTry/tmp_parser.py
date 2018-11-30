# import ast
# import pickle
#
# dic = {1:2}
# dic2 = {3:4}
#
# term_path =  'C:\Retrieval_folder\corpus\index\dic_test'
#
# with open(term_path, 'wb') as file:
#     pickle.dump(dic,file)
#     file.close()
#
# with open(term_path, 'rb') as file:
#     o = pickle.load(file)
#     print(o)
#     file.close()
#
# with open(term_path, 'wb') as file:
#     o.update(dic2)
#     print(o)
#     pickle.dump(o, file)
#     file.close()
#

# string = 'African National 1)african dddd[ANC] Dogs do(g st}ayaway'
# x = ' '.join(' '.join(' '.join(' '.join(' '.join(' '.join(string.split('(')).split(')')).split(']')).split('[')).split('{')).split('}')).split()
# #x.split()
# print(x)
