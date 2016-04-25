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

    ####    Bigram Dictionary     ####
    dict_bi={}
    
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
                tweet,token=preprocesingTweet2(tweet, token, stopWords)
                tweet=[i.strip(specialChar).lower() for i in tweet]
                tweet=[i for i in tweet if i]
                for i in range(len(tweet)-1):
                    phrase=tweet[i]+' '+tweet[i+1]
                    if phrase not in dict_bi:
                        dict_bi[phrase]=[0,0,0]
                    dict_bi[phrase][eval(label)]+=1
    f.close()

    model_bi=[]

    for i in dict_bi.keys():
        count=reduce(lambda x,y:x+y,dict_bi[i])
        if count>=10:
            count=count*1.0
            pos=dict_bi[i][positive]/count
            neg=dict_bi[i][negative]/count
            neu=dict_bi[i][neutral]/count
            if pos>0.9 or neg>0.9 or neu > 0.9:
                l=[i,pos,neg,neu,count]
                model_bi.append(l)

    model_bi=sorted(model_bi,key=lambda x:x[4],reverse=True)      #### Sorting uniModel with COUNT
    
    ####    Print model_bi List    ####
    for i in model_bi:
        print i[0]