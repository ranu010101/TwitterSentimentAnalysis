from senti_classifier import senti_classifier
from replaceExpand import *
from nltk.corpus import wordnet

#calculateScore obtains score for a given tweet using dictionary for polarity

def calculateScore(tweet, pDict): #pDict represents polarity dictionary
    score = {}
    tweet = [_.lower().strip(specialChar) for _ in tweet]
    tweet = [_ for _ in tweet if _]
    tweetLength = len(tweet)
    init = 0
    neutralScore = 0
    while init<tweetLength:
        for _ in range(init,tweetLength):
            flag = 0
            for __ in range(tweetLength,_,-1):
                phrase = frozenset(tweet[_:__])
                if phrase in pDict:
                    init = __
                    flag = 1
                    positiveScore = pDict[phrase][positive]
                    negativeScore = pDict[phrase][negative]
                    neutralScore = pDict[phrase][neutral]
                    score[phrase]=[positiveScore, negativeScore, neutralScore]
                    break
            if flag==1:
                break
            else:
                positiveScore, negativeScore = senti_classifier.polarity_scores([tweet[_]])
                score[frozenset([tweet[_]])]=[positiveScore, negativeScore, neutralScore]
                pDict[frozenset([tweet[_]])]=[positiveScore, negativeScore, neutralScore]
    return score,pDict

#findCapitalised finds capitals in a tweet

def findCapitalised(tweet, token, score):
    count = 0
    countCapitals = 0
    countCapitalPositives = 0
    countCapitalNegatives = 0
    isCapitalised = 0
    for _ in range(len(tweet)):
        if token[_]!='$':
            word = tweet[_].strip(specialChar)
            if word:
                count = count + 1
                if word.isupper():
                    countCapitals = countCapitals + 1
                    word=frozenset([word.lower()])
                    for phrase in score.keys():
                        if word.issubset(phrase):
                                if score[phrase][positive]!=0.0:
                                    countCapitalPositives +=1
                                if score[phrase][negative]!=0.0:
                                    countCapitalNegatives +=1
    percentageCapitalised = 0.0
    if count>0:
        percentageCapitalised = float(countCapitals)/count
    if percentageCapitalised!=0.0:
	    isCapitalised=1
    return [ percentageCapitalised, countCapitalPositives, countCapitalNegatives ,isCapitalised ]

#findNegation finds negations in a tweet

def findNegation(tweet):
	negCount = 0
	for _ in range(len(tweet)):
		if tweet[_] == 'negation': #compares against negations
			negCount+=1
	return [negCount]

#findTotalScore computes total score

def findTotalScore(score):
    totalScore = 0
    for _ in score.values():
        totalScore += (_[positive] - _[negative])
    return [ totalScore ]

#findPositiveNegativeWords finds total number of positive and negative words

def findPositiveNegativeWords(tweet, token, score):
    countPositive=0
    countNegative=0
    count=0
    totalScore = 0
    if tweet:
        for _ in range(len(tweet)):
            if token[_] not in listSpecialTag:
                word=frozenset([tweet[_].lower().strip(specialChar)])
                if word:
                    count+=1
                    for phrase in score.keys():
                        if word.issubset(phrase):
                            if score[phrase][positive]!=0.0:
	                            countPositive+=1
                            if score[phrase][negative]!=0.0:
                                countNegative+=1
                            totalScore += (score[phrase][positive] - score[phrase][negative])
    return [ countPositive, countNegative, totalScore ]

#findEmoticons filters emoticons from tweet

def findEmoticons(tweet, token):
	countEmoPostive = 0
	countEmoNegative =0
	countEmoExtremePostive = 0
	countEmoExtremeNegative = 0

	for _ in range(len(tweet)):
	    if token[_] ==  'E':
			if tweet[_] == 'Extremely-Postive':
				countEmoExtremePostive+=1
			if tweet[_] == 'Extremely-Negative':
				countEmoExtremeNegative+=1
			if tweet[_] == 'Postive':
				countEmoPostive+=1
			if tweet[_] == 'Negative':
				countEmoNegative+=1

	return [ countEmoPostive, countEmoNegative, countEmoExtremePostive, countEmoExtremeNegative ]

#findHashtag finds hashtags in a tweet

def findHashtag( tweet, token, score):
	
    countHashPostive=0
    countHashNegative=0
    count=0
    for _ in range(len(tweet)):
        if token[_]=='#' :
            count+=1
            word=frozenset([tweet[_].lower().strip(specialChar)])
            if word:
                for phrase in score.keys():
                    if word.issubset(phrase):
                        if score[phrase][positive]!=0.0:
                            countHashPostive+=1
                        if score[phrase][negative]!=0.0:
                            countHashNegative+=1
                        break
    return [ countHashPostive, countHashNegative ]

#countSpecialChar finds special chars in a tweet

def countSpecialChar(tweet,score):
    listSpecialChars={'?':0,'!':0,'*':0}
    for _ in range(len(tweet)):
        word=tweet[_].lower().strip(specialChar)
        if word:
            listSpecialChars['?']+=word.listSpecialChars('?')
            listSpecialChars['!']+=word.listSpecialChars('!')
            listSpecialChars['*']+=word.listSpecialChars('*')
    return [ listSpecialChars['?'], listSpecialChars['!'], listSpecialChars['*'] ]

#countPosTag counts POS tags in a tweet

def countPosTag(tweet,token,score):
    POStagList = {'N':0,'V':0,'R':0,'P':0,'O':0,'A':0}
    for _ in range(len(tweet)):
        word=tweet[_].lower().strip(specialChar)
        if word:
            if token[_] in POStagList:
                POStagList[token[_]]+=1

    return [ POStagList['N'], POStagList['V'], POStagList['R'], POStagList['P'], POStagList['O'], POStagList['A'] ]

#findUrl counts URLs in a tweet

def findUrl(tweet,token):
    count = 0
    for _ in range(len(tweet)):
        if token[_] ==  'U':
            count+=1
    return [count]

#findFeatures takes tweet as input and token, then returns the feature vector

def findFeatures(tweet, token, pDict, stopWords, emoticonsDict, acronymDict):

    tweet,token,i,j = preprocesingTweet1(tweet, token, emoticonsDict, acronymDict) 
    score,pDict = calculateScore(tweet, pDict)

    #Initializing feature vector
    fVector=[] 
    fVector.extend(findTotalScore(score))
    tweet,token=preprocesingTweet2(tweet, token, stopWords)
    
    #Adding respective features
    fVector.extend(findCapitalised( tweet, token, score))
    fVector.extend(findHashtag( tweet, token, score))
    fVector.extend(findEmoticons(tweet, token))
    fVector.extend(findNegation(tweet))
    fVector.extend(findPositiveNegativeWords(tweet,token, score))
    fVector.extend(countSpecialChar(tweet,score))  
    fVector.extend(countPosTag(tweet,token,score))

    return fVector, pDict
