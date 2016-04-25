#This code combines the output of the tokeniser and the input tweet set and returns the final input file in the following format :- tweet Id, Tweet tokens, POS tokens,label
import sys
from itertools import izip
def main():
    #check for the validity of arguments
    if len(sys.argv)!= 4:
        print "Usage :: python combine.py ../documents-export-2014-03-19/trainingDatasetProcessed.txt ../documents-export-2014-03-19/trainingTokenised.txt ../documents-export-2014-03-19/finalTrainingInput.txt"
        sys.exit(0)
    #Parallely combine both the files
    arr=[]
    #read from the files
    file1=open(sys.argv[1],'r')
    file2=open(sys.argv[2],'r')
    for l1, l2 in izip(file1, file2):
        w1 = l1.strip().split('\t') #tab separated
        w2 = l2.strip().split('\t')
        st = w1[0]+'\t'+w2[0]+'\t'+w2[1]+'\t'+w1[2]+'\n'
        arr.append(st)
    file1.close()
    file2.close()
    #write this to file
    f=open(sys.argv[3],'w')
    f.write("".join(arr))
    f.close()
if __name__ == "__main__":
    main()