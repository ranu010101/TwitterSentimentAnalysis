from replaceExpand import *
from collections import defaultdict

#loadDictionary loads various dictionaries involving, emoticons, acronyms, stop-words

def loadDictionary():
    #Creates emoticons dictionary

    text = open(".//code//emoticonsWithPolarity.txt",'r')
    textNSeparated = text.read().split('\n')
    emoticonsDictionary = {}

    for _ in textNSeparated:
        if _:
            _ = _.split()
            value = _[-1]
            key = _[:-1]
            for __ in key:
                emoticonsDictionary[__] = value
    text.close()

    #Creates acronym dictionary

    text = open(".//code//acronym_tokenised.txt",'r')
    textNSeparated = text.read().split('\n')
    acronymDictionary = {}

    for _ in data:
        if _:
            _ = _.split('\t')
            word = _[0].split()
            token = _[1].split()[1:]
            key = word[0].lower().strip(specialChar)
            value = [__.lower().strip(specialChar) for __ in word[1:]]
            acronymDictionary[key] = [value,token]
    text.close()

    #Loads stopwords 

    text = open(".//code//stopWords.txt", "r")
    stopWords = defaultdict(int)
    
    for _ in text:
        if _:
            _ = _.strip(specialChar).lower()
            stopWords[_]=1
    text.close()

    return acronymDictonary, stopWords, emoticonsDictionary
