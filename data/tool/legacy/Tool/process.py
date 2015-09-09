import demjson
from string import punctuation
import string
'''
twitterList = []
f = open('result.txt','r')
for line in f.readlines():
    JSONObject = demjson.decode(line)
    twitterList.append(JSONObject)
'''

text = '12345,!?67890'
text = "".join([c for c in text if c not in punctuation])
print text    