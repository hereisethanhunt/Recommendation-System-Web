h=open("user_clus.txt","r")
g=open("user_c.txt","w")
c=1
for i in h:
	word=i.split(";")
	g.write(str(c)+";"+str(word[1])+";"+"\n")
	c+=1