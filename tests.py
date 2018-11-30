import pickle
import urllib
import json

__dictionary_of_postings = {1:{1:1,1:2}, 2:{2:1,2:2}}

url = 'http://getcitydetails.geobytes.com/GetCityDetails?fqcn=Paris'
# response = urllib.urlopen(url)
# json = json.loads(response.url)

with urllib.request.urlopen(url) as url:
    s = url.read()
    json = json.loads(s)
#I'm guessing this would output the html source code?
print(s)
x=2
for key in __dictionary_of_postings:
    with open('C:\Retrieval_folder\index' + '\\' + str(key), 'wb') as file:
        pickle.dump(__dictionary_of_postings[key], file)
        file.close()
        x=2


with open( 'C:\Retrieval_folder\index\\abc', 'rb') as file:
    __current_posting = pickle.load(file)
    print('x')
    file.close()


