import sys
from replaceExpand import *
from collections import defaultdict

if __name__ == '__main__':

    ####    Emoticon Directory Creation    ####
    f=open("emoticonsWithPolarity.txt",'r')
    data=f.read().split('\n')
    dict_emoticon={}                       #### emoticon dictionary
    for i in data:
        if i:
            i=i.split()
            value=i[-1]
            key=i[:-1]
            for j in key:
                dict_emoticon[j]=value
    f.close()

    ####    Acronym Dictionary Creation    ####
    f=open("acronym_tokenised.txt",'r')
    data=f.read().split('\n')
    dict_acronym={}                        #### acronym dictionary
    for i in data:
        if i:
            i=i.split('\t')
            word=i[0].split()
            token=i[1].split()[1:]
            key=word[0].lower().strip(specialChar)
            value=[j.lower().strip(specialChar) for j in word[1:]]
            dict_acronym[key]=[value,token]
    f.close()

    ####    StopWord Directory Creation    ####
    stopWords=defaultdict(int)
    f=open("stopWords.txt", "r")           
    for line in f:
        if line:
            line=line.strip(specialChar).lower()
            stopWords[line]=1
    f.close()

    ####    Unigram Dictionary     ####
    dict_uni={}                             
    
    ####    Preprocessing Tweet    ####
    f=open(sys.argv[1],'r')
    for i in f:
        if i:
            i=i.split('\t')
            tweet=i[1].split()
            token=i[2].split()
            label=i[3].strip()
            if tweet:
                tweet, token, count1, count2 = preprocesingTweet1(tweet, token, dict_emoticon, dict_acronym)
                tweet,token = preprocesingTweet2(tweet, token, stopWords)
                for i in tweet:
                    word = i.strip(specialChar).lower()
                    if word:
                        if word not in dict_uni:
                            dict_uni[word] = [0,0,0]
                        dict_uni[word][eval(label)]+=1
    f.close()

    model_uni=[]

    for i in dict_uni.keys():
        count=reduce(lambda x,y:x+y,dict_uni[i])
        if count>=20:
            count=count*1.0
            pos=dict_uni[i][positive]/count
            neg=dict_uni[i][negative]/count
            neu=dict_uni[i][neutral]/count
            if pos>0.7 or neg>0.7 or neu > 0.7:
                l=[i,pos,neg,neu,count]
                model_uni.append(l)

    model_uni=sorted(model_uni,key=lambda x:x[4],reverse=True)    #### Sorting model_uni with COUNT

    ####    Print model_uni List    ####
    for i in model_uni:
        print i[0]