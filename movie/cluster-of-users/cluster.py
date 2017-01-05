arr_clus=[]
movieid=[]
rating=[]
target=open("user_c.txt","r")
for i in target:
	x=i.split(';')
	user=x[0]
	cluster=x[1]
	#print x[0]
	if (int(x[1]) == 2):
		arr_clus.append(int(x[0]))
#print arr_clus

	
for f in arr_clus:
	#print f
	max1=0
	max2=0
	target1=open("u.data","r")
	for i in target1:
		x=i.split('\t')
		#print x[0]
		if (f == int(x[0])):
			if(int(x[2])>max1):
				max1=int(x[2])
				max2=int(x[1])
	movieid.append(max2)
	rating.append(max1)
print movieid
print rating

