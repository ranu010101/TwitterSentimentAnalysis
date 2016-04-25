import sys
pos,neg,neu=0,1,2

if __name__ == '__main__':
	if len(sys.argv)!= 3:    
		print "Usage :: python .py real_labels predicted_labels"
		sys.exit(0)
	real_file=open(sys.argv[1],'r')
	predicted_file=open(sys.argv[2],'r')
	real_labels=[]
	predicted_labels=[]
	confMat=[[0,0,0],[0,0,0],[0,0,0]]
	for i in real_file:
		i=i.strip('\t\n\r ')
		real_labels+=[i]
	for i in predicted_file:
		i=i.strip('\t\n\r ')
		predicted_labels+=[i]
	len_labels=len(real_labels)
	for i in range(len_labels):
		confMat[eval(real_labels[i])][eval(predicted_labels[i])]+=1
	print "actual/predicted\tpositive\tnegative\tneutral"
	print "positive\t\t",
	for i in confMat[pos]:
			print str(i)+'\t\t',
	print "\nnegative\t\t",
	for i in confMat[neg]:
			print str(i)+'\t\t',
	print "\nneutral\t\t\t",
	for i in confMat[neu]:
			print str(i)+'\t\t',
	print		