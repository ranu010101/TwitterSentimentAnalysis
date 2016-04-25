from featureExtractor import *
from probablityModel import *
import sys
from classifier import *
from prepare import *
from collections import defaultdict
from svmutil import *

if __name__ == '__main__':
    if len(sys.argv)!= 3:                                                   
        print "Usage :: python main.py ../dataset/finalTrainingInput.txt ../dataset/finalTestingInput"
        sys.exit(0)
    acronym_dict,stop_words,emoticons_dict = loadDictionary()

    prior_score=dict(map(lambda (k,v): (frozenset(reduce( lambda x,y:x+y,[[i] if i not in acronym_dict else acronym_dict[i][0] for i in k.split()])),int(v)),[ line.split('\t') for line in open(".//code//AFINN-111.txt") ]))
    
    #First, unigram model is created
    print "Unigram Model is being created"
    uni_model=[]
    file=open('.//code//unigram.txt','r')
    for line in file:
        if line:
            line=line.strip('\r\t\n ')
            uni_model.append(line)
    uni_model.sort()

    print "Unigram Model has been created"

    print "Bigram Model is being created"
    bi_model=[]
    file=open('.//code//bigram.txt','r')
    for line in file:
        if line:
            line=line.strip('\r\t\n ')
            bi_model.append(line)
    bi_model.sort()
    print "Bigram Model has been created"

    print "Trigram Model is being created"
    tri_model=[]
    file=open('.//code//trigram.txt','r')
    for line in file:
        if line:
            line=line.strip('\r\t\n ')
            tri_model.append(line)
    tri_model.sort()
    print "Trigram Model has been created"
    #polarity dictionary combines prior score
    polarity_dictionary = probTraining(prior_score)
    #Create a feature vector of training set
    print "Feature Vectors are being created"
    encode={'positive': 1.0,'negative': 2.0,'neutral':3.0}
    training_label=[]
    f=open(sys.argv[1],'r')
    feature_vector_train=[]
    for i in f:
        if i:
            i=i.split('\t')
            _tweet=i[1].split()
            _token=i[2].split()
            label=i[3].strip()
            if _tweet:
                vector=[]
                training_label.append(encode[label])
                vector,polarity_dictionary=findFeatures(_tweet, _token, polarity_dictionary, stop_words, emoticons_dict, acronym_dict)
                uni_vector=[0]*len(uni_model)
                for i in _tweet:
                    word=i.strip(specialChar).lower()
                    if word:
                        if word in uni_model:
                            ind=uni_model.index(word)
                            uni_vector[ind]=1
                vector=vector+uni_vector

                bi_vector=[0]*len(bi_model)
                _tweet=[i.strip(specialChar).lower() for i in _tweet]
                _tweet=[i for i in _tweet if i]
                for i in range(len(_tweet)-1):
                    phrase=_tweet[i]+' '+_tweet[i+1]
                    if word in bi_model:
                        ind=bi_model.index(phrase)
                        bi_vector[ind]=1
                vector=vector+bi_vector

                tri_vector=[0]*len(tri_model)
                _tweet=[i.strip(specialChar).lower() for i in _tweet]
                _tweet=[i for i in _tweet if i]
                for i in range(len(_tweet)-2):
                    phrase=_tweet[i]+' '+_tweet[i+1]+' '+_tweet[i+2]
                    if word in tri_model:
                        ind=tri_model.index(phrase)
                        tri_vector[ind]=1
                vector=vector+tri_vector
                feature_vector_train.append(vector)
    f.close()
    print "Feature Vectors Train Created"
    
    #for each new _tweet create a feature vector and feed it to above model to get label
    
    testing_label=[]
    data=[]
    data1=[]
    f=open(sys.argv[2],'r')
    feature_vectots_test=[]
    for i in f:
        if i:
            i=i.split('\t')
            _tweet=i[1].split()
            _token=i[2].split()
            label=i[3].strip()
            if _tweet:
                data.append(label)
                testing_label.append(encode[label])
                vector=[]
                vector,polarity_dictionary=findFeatures(_tweet, _token, polarity_dictionary, stop_words, emoticons_dict, acronym_dict)

                uni_vector=[0]*len(uni_model)
                for i in _tweet:
                    word=i.strip(specialChar).lower()
                    if word:
                        if word in uni_model:
                            ind=uni_model.index(word)
                            uni_vector[ind]=1
                vector=vector+uni_vector

                bi_vector=[0]*len(bi_model)
                _tweet=[i.strip(specialChar).lower() for i in _tweet]
                _tweet=[i for i in _tweet if i]
                for i in range(len(_tweet)-1):
                    phrase=_tweet[i]+' '+_tweet[i+1]
                    if word in bi_model:
                        ind=bi_model.index(phrase)
                        bi_vector[ind]=1
                vector=vector+bi_vector

                tri_vector=[0]*len(tri_model)
                _tweet=[i.strip(specialChar).lower() for i in _tweet]
                _tweet=[i for i in _tweet if i]

                for i in range(len(_tweet)-2):
                    phrase=_tweet[i]+' '+_tweet[i+1]+' '+_tweet[i+2]
                    if word in tri_model:
                        ind=tri_model.index(phrase)
                        tri_vector[ind]=1
                vector=vector+tri_vector
                feature_vectots_test.append(vector)
    f.close()
    print "Feature Vectors of test input created. Accuracy is being calculated..."
    predicted_label = svmClassifier(training_label,testing_label,feature_vector_train,feature_vectots_test)
    for i in range(len(predicted_label)):
        given_label = predicted_label[i]
        label = encode.keys()[encode.values().index(given_label)]
        data1.append(label)

    f=open('./code/taskB.gs','w')
    f.write('\n'.join(data))
    f.close()

    f=open('./code/taskB.pred','w')
    f.write('\n'.join(data1))
    f.close()