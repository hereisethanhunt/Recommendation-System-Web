target=open("u.user","r")
idd=1
flag=0
gender="M"
for i in target:
	x=i.split("|")
	if(int(x[0]) == idd and str(x[2]) == gender):
		print "login succeded"
		flag=1
if(flag==0):
	print "hatt"