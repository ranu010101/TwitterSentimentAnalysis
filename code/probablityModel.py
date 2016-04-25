from replaceExpand import *
from senti_classifier import senti_classifier


def probTraining(prevScore):

    #Training file contains trained data in X, in format tweet\t pos \t label \n.
    #It returns the dictonary comtaining the probability of word being positive, negative or neutral.

    wordProbabilityability = {}
    tweetCount = [0,0,0,0]
    for i in prevScore.keys():
        if i:
            wordProbability[i] = [0.0,0.0,0.0]
            positiveScore, negativeScore = senti_classifier.polarity_scores(list(i))
            if prevScore[i]>0.0:
                wordProbability[i][positive]=prevScore[i]/5.0
                wordProbability[i][negative]=negativeScore
            elif prevScore[i]<0.0:
                wordProbability[i][negative]=-(prevScore[i]/5.0)
                wordProbability[i][positive]=positiveScore
            else:
                wordProbability[i][positive]=positiveScore
                wordProbability[i][negative]=negativeScore
                
    return wordProbability
