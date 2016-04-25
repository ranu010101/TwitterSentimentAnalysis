import sys
if __name__ == '__main__':
    
    ####    Check Arguments    ####
    if len(sys.argv)!= 3:                                                   
        print "Usage :: python findF1.py actual_Label predicted_Label"
        sys.exit(0)

    predicted_Label=[]
    actual_Label=[]

    ####   
    f=open(sys.argv[1],'r')
    for line in f:
        actual_Label.append(line.strip())
    f.close()

    f=open(sys.argv[2],'r')
    for line in f:
        predicted_Label.append(line.strip())
    f.close()

    #### Initialising variables to zero
    count_Positive_A=0
    count_Negative_A=0
    count_Neutral_A=0

    ####    Counting positiveA, negativeA, neutralA    ####
    for i in xrange(len(actual_Label)):
        if actual_Label[i]=='positive':
            count_Positive_A+=1
        elif actual_Label[i]=='negative':
            count_Negative_A+=1
        else:
            count_Neutral_A+=1

    count_Positive_P=0
    count_Negative_P=0
    count_Neutral_P=0

    for i in xrange(len(predicted_Label)):
        if predicted_Label[i]=='positive':
            count_Positive_P+=1
        elif predicted_Label[i]=='negative':
            count_Negative_P+=1
        else:
            count_Neutral_P+=1

    true_P_Positive=0
    true_P_Negative=0
    true_P_Neutral=0
    for i in xrange(len(predicted_Label)):
        if predicted_Label[i]=='positive':
            if actual_Label[i]=='positive':
                true_P_Positive+=1
        elif predicted_Label[i]=='negative':
            if actual_Label[i]=='negative':
                true_P_Negative+=1
        else:
            if actual_Label[i]=='neutral':
                true_P_Neutral+=1

    precision_Positive = true_P_Positive/float(count_Positive_P)
    precision_Negative = true_P_Negative/float(count_Negative_P)
    precision_Neutral = true_P_Neutral/float(count_Neutral_P)

    recall_Positive = true_P_Positive/float(count_Positive_A)
    recall_Negative = true_P_Negative/float(count_Negative_A)
    recall_Neutral = true_P_Neutral/float(count_Neutral_A)

    f1_Positive = (2*precision_Positive*recall_Positive)/(precision_Positive+recall_Positive)
    f1_Negative = (2*precision_Negative*recall_Negative)/(precision_Negative+recall_Negative)
    f1_Neutral = (2*precision_Neutral*recall_Neutral)/(precision_Neutral+recall_Neutral)

    ####    Print Precision    ####
    print "Precision: Positive, Negative, Neutral"
    print f1_Positive
    print f1_Negative
    print f1_Neutral

    ####    Print Recall    ####
    print "Recall: Positive, Negative, Neutral"

    print recall_Positive
    print recall_Negative
    print recall_Neutral

    print "Average F1 for Positive and Neutral"

    #Print average
    average = (f1_Neutral+f1_Positive)/2
    print average