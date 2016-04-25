import re
pos=0
neg=1
neu=2
total=3
special_char='1234567890#@%^&()_=`{}:"|[]\;\',./\n\t\r '
list_special_tag = ['#','U','@',',','E','~','$','G']
def replaceHashtag(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after replacement 
    #*** - > # """
    for i in range(len(tweet)):
        if token[i]=='#' or tweet[i].startswith('#'):
            token[i]='#'
            tweet[i]=tweet[i][1:].strip(special_char)
    return tweet,token
def removeNonEnglishWords(tweet,token):
    #remove the non-english or better non-ascii characters
    #takes as input a list of words in tweet and a list of corresponding tokens, 
    #not using tokens now but may use in future
    #and return the modified list of token and words
    new_tweet=[]
    new_token=[]
    for i in range(len(tweet)):
        if tweet[i]!='':
            chk=re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,.#@!~`%&-_=])+$',tweet[i])
            if chk:
                new_tweet.append(tweet[i])
                new_token.append(token[i])
    return new_tweet, new_token
def removeStopWords(tweet, token, stop_words_dict):
    #remove the stop words ,
    #takes as input a list of words in tweet ,a list of corresponding tokens and a stopWords Dictonary, 
    #and return the modified list of token and words
    new_tweet=[]
    new_token=[]
    for i in range(len(tweet)):
        if stop_words_dict[tweet[i].lower().strip(special_char)] == 0:
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token
def replaceEmoticons(emoticons_dict,tweet,token):
    #replaces the emoticons present in tweet with its polarity
    #takes as input a emoticons dict which has emoticons as key and polarity as value
    #and a list which contains words in tweet and return list of words in tweet after replacement
    for i in range(len(tweet)):
        if tweet[i] in emoticons_dict:
            tweet[i]=emoticons_dict[tweet[i]]
            token[i]='E'
    return tweet,token


def expandAcronym(acronym_dict,tweet,token):
    #expand the Acronym present in tweet 
    #takes as input a acronym dict which has acronym as key and abbreviation as value,
    #a list which contains words in tweet and a list of token and return list of words in tweet after expansion and tokens
    new_tweet=[]
    new_token=[]
    count=0
    for i in range(len(tweet)):
        word=tweet[i].lower().strip(special_char)
        if word:
            if word in acronym_dict:
                count+=1
                new_tweet+=acronym_dict[word][0]
                new_token+=acronym_dict[word][1]
            else:
                new_tweet+=[tweet[i]]
                new_token+=[token[i]]
    return new_tweet, new_token,count
def replaceRepetition(tweet):
    #takes as input a list which contains words in tweet and return list of words in tweet after replacement and numner of repetion
    #   eg coooooooool -> coool 
    count=0
    for i in range(len(tweet)):
        x=list(tweet[i])
        if len(x)>3:
            flag=0
            for j in range(3,len(x)):
                if(x[j-3].lower()==x[j-2].lower()==x[j-1].lower()==x[j].lower()):
                    x[j-3]=''

                    if flag==0:
                        count+=1
                        flag=1
            tweet[i]=''.join(x).strip(special_char)

    return tweet,count


def replaceNegation(tweet):
    #takes as input a list which contains words in tweet and return list of words in tweet after replacement of "not","no","n't","~"
    #   eg isn't -> negation 
    #   not -> negation
    for i in range(len(tweet)):
        word=tweet[i].lower().strip(special_char)
        if(word=="no" or word=="not" or word.count("n't")>0):
            tweet[i]='negation'

    return tweet


def expandNegation(tweet,token):
    #takes as input a list which contains words in tweet and return list of words in tweet after expanding of "n't" to "not"
    #eg isn't -> is not
    
    new_tweet=[]
    new_token=[]
    for i in range(len(tweet)):
        word=tweet[i].lower().strip(special_char)
        if(word[-3:]=="n't"):
            if word[-5:]=="can't" :
                new_tweet.append('can')
            else:
                new_tweet.append(word[:-3])
            new_tweet.append('not')
            new_token.append('V')
            new_token.append('R')
        else:
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet,new_token


def removeTarget(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after replacement 
    #@**** -> @ 
    new_token=[]
    new_tweet=[]
    for i in range(len(tweet)):
        if token[i]=='@' or tweet[i].startswith('@'):
            continue
        else:
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token


def removeUrl(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after replacement 
    #www.*.* ->'URL'
    new_token=[]
    new_tweet=[]
    for i in range(len(tweet)):
        if token[i]!='U':
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token

def removeNumbers(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after removing 
    #numbers
    new_token=[]
    new_tweet=[]
    for i in range(len(tweet)):
        if token[i]!='$':
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token

def removeProperCommonNoun(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after removing 
    #numbers 
    new_token=[]
    new_tweet=[]
    for i in range(len(tweet)):
        if token[i]!='^' and token[i]!='Z' and token[i]!='O':
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token

def removePreposition(tweet, token):
    #takes as input a list which contains words in tweet and return list of words in tweet after removing 
    #numbers
    new_token=[]
    new_tweet=[]
    for i in range(len(tweet)):
        if token[i]!='P':
            new_tweet.append(tweet[i])
            new_token.append(token[i])
    return new_tweet, new_token
def preprocesingTweet1(tweet, token, emoticons_dict, acronym_dict):
    #preprocess the tweet
    tweet,token = replaceEmoticons(emoticons_dict,tweet,token)
    tweet, token = removeNonEnglishWords(tweet, token)
    tweet, token = removeNumbers(tweet, token)
    tweet, token = removeProperCommonNoun(tweet, token)
    tweet, token = removePreposition(tweet, token)
    tweet, token, count1 = expandAcronym(acronym_dict,tweet,token)
    tweet, count2 = replaceRepetition(tweet)
    tweet,token = replaceHashtag (tweet, token)
    tweet,token = removeUrl(tweet, token)
    tweet, token = removeTarget(tweet, token)
    tweet,token = expandNegation (tweet, token)
    return tweet, token, count1, count2


def preprocesingTweet2(tweet, token, stopWords):
    #preprocess the tweet
    tweet = replaceNegation(tweet)
    tweet, token = removeStopWords(tweet, token, stopWords)
    return tweet, token
