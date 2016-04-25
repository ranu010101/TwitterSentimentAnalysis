#This code takes as input the path of the filename of the original dataset and the output filename
#It returns the processed dataset with the relevant fields
#It helps in generating Training Data with Labels and Testing Data with Labels or without labels
import sys
def main():
    if len(sys.argv)!= 4:                                                                               
        print "Usage :: python extractData pathOfInputFileName outputFileName tempFileToHoldTweetForNlpTagger"
        sys.exit(0)
    arr=[]
    arr1=[]
    file=open(sys.argv[1],'r')
    for line in file:
    	word_list = line.split('\t')
        if word_list[3]!="Not Available\n":
    	   arr.append(line)
           arr1.append(word_list[3])
    file.close()
    file=open(sys.argv[2],'w')
    file.write("".join(arr))
    file.close()
    file=open(sys.argv[3],'w')
    file.write("".join(arr1))
    file.close()
if __name__ == "__main__":                                                                              
    main()
