import pickle

with open( 'C:\Retrieval_folder\index\\abc', 'rb') as file:
    __current_posting = pickle.load(file)
    print('x')
    file.close()


