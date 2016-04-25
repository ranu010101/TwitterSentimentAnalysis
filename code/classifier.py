from svmutil import *

# trLab:training label, teLab:testing label, feVeTr: feature vectors for training, feVeTe: feature vectors for testing

def svmClassifier(trLab,teLab,feVeTr,feVeTe):
    
    #Feed the feature vector to svm to create model
    print "Creating SVM Model"
    model= svm_train(trLab,feVeTr)
    print "Model is created. Saving the model."

    #Save model
    svm_save_model('.//code//sentimentAnalysisSVM.model', model)
    print "Model is saved. Proceed to test."

    #prLab:predicted label, predAcc: predicted accuracy/predAcc, predVal:predicted value for accuracy 	

    prLab, predAcc, predVal = svm_predict(teLab, feVeTe, model)
    print "Finished. The accuracy is:"
    print predAcc[0]
    return prLab
