import numpy as np
import matplotlib.pyplot as plt
xx=956
f=open("u.user","r")
h=open("u.user1","w")
for line in f:
	lines=line.replace("\n","|")
	words=lines.split("|")
	if words[2]=='M':
		x=100
	else:
		x=200
	y=words[3]
	g=open("u.occupation","r")
	for lines in g:
		line=lines.replace("\n","|")
		word=line.split("|")
		print word[0]+ y+word[1]
		if word[0]==y:
			y=word[1]
	g.close()
	h.write(str(int(words[0]))+"|"+str(int(words[1])*2)+"|"+str(x)+"|"+str(y)+"|"+"\n")
h.close()


plt.style.use("ggplot")
from sklearn.cluster import KMeans
f=open("w.txt","w")
y=[]
file = open("u.user1" , "r")
for line in file:
	data = line.split('|')
	# print data
	N = []
	for numbers in data:
		try:
			n = float(numbers)
			# f.write(str(n)+" ")
			N.append(n)
		except ValueError:
			pass
	N.pop(0)
    	print N
    	# f.write('\n')
    	y.append(N)
    	X=np.array(y)
# X=np.array([[1,2,4],[1,2,5],[1,2,9],[1,2,10],[1,2,14],[1,2,15],[1,2,16]])


Kmeans=KMeans(n_clusters=20)
Kmeans.fit(X)
centroids= Kmeans.cluster_centers_
labels=Kmeans.labels_
print(centroids)
for i in centroids:
	f.write(str(1)+";")
	c=1
	for j in i:
		c+=1
		f.write(str(j)+";")
		if(c%4==0):
			f.write("\n")

print(labels)
p=open("user_clus.txt","w")
c=1
for i in labels:
	p.write(str(c)+";"+str(i)+";"+"\n")
	c+=1
p.close()
d1=open("user_clus.txt","r")
for lines in d1:
	words=lines.split(";")
	xx=int(words[0])
d1.close()
yy=1
d=open("user_clus.txt","r")
for lines in d:
	words=lines.split(";")
	if(int(words[0])==xx):
		print "hello"
		yy=words[1]
print "you are assigned cluster number : "+ yy
colors= 7*["g.","r.","y.","b.","c.","y."]
for i in range(len(X)):
	# print("coordiante",X[i],"label:",labels[i])
	plt.plot(X[i][0],X[i][1],colors[labels[i]],markersize=10)
plt.scatter(centroids[:,1],centroids[:,2],marker="x",s=150,linewidths=5,zorder=10)
plt.show()
a=[0]*1683
g=open("user_clus.txt","r")
for line in g:
	word=line.split(";")
	a[int(word[0])]=int(word[1])
for i in range(100):
	plt.bar(i,a[i])
plt.xlabel("user id")
plt.ylabel("cluster id")
plt.title("movie clustering")
plt.show()
