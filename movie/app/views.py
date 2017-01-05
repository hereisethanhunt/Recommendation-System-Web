from flask import render_template,jsonify,json,session,url_for,redirect
from app import app
from flask import flash,redirect
from .forms import LoginForm
from flask import request
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from subprocess import call
import time
import pdb
import MySQLdb
import requests
import random
import math
import time
import numpy
import threading
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call
background_scripts = {}
#voted contains list of all items that a user has rated
voted = {}
cluster=[0]*1701
user_cluster=[0]*1000
#list of ID's of all users
matrix1 = [[0 for _ in range(2019)] for _ in range(960)]
matrix = [[0 for _ in range(1683)] for _ in range(1000)]
avg_item_rating = []
avg_user_rating = []
avg_user_rating1=[]
avg_item_rating1=[]

def read1():
	starting_time = time.time()
	data = []
	with open("mappingstep2.txt" , "r") as file:
		for line in file :
			n = line.split(';')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[3])
			d['rating'] = int(n[2])

			assert(d['uid'] <= 960)
			assert(d['iid'] <= 2019)

			matrix1[d['uid']][d['iid']] = d['rating']
			# matrix[944][6]=4

			# if d['uid'] not in voted:
			# 	voted[d['uid']] = []
			# voted[d['uid']].append(d['iid'])
			# data.append(d)
	#print matrix
	# with open("data.txt" , "r") as file:
	# 	for line in file :
	# 		n = line.split(';')
	# 		# print n
	# 		d = {}
	# 		d['uid'] = int(n[0])
	# 		d['iid'] = int(n[1])
	# 		cluster[d['uid']] = d['iid']
	# 		print cluster[d['uid']]


	with open("user_clus.txt" , "r") as file:
		for line in file :
			n = line.split(';')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[1])
			user_cluster[d['uid']] = d['iid']


	# ff=open("qwer.txt","w")
	# for i in range(len(cluster)):
	# 	print cluster[i]
	# 	print "hatt"
	# 	ff.write(str(cluster[i]))

	# for i in range(len(data)):
	# 	print data[i]
	# print "max uid %d max iid %d" %(max_uid , max_iid)
	ending_time = time.time()

	print ("time taken is %f"  %(ending_time - starting_time))








def read():
	starting_time = time.time()
	data = []
	with open("u.data" , "r") as file:
		for line in file :
			n = line.split('\t')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[1])
			d['rating'] = int(n[2])

			assert(d['uid'] <= 1000)
			assert(d['iid'] <= 1683)

			matrix[d['uid']][d['iid']] = d['rating']
			# matrix[944][6]=4

			# if d['uid'] not in voted:
			# 	voted[d['uid']] = []
			# voted[d['uid']].append(d['iid'])
			# data.append(d)
	#print matrix
	with open("data.txt" , "r") as file:
		for line in file :
			n = line.split(';')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[1])
			cluster[d['uid']] = d['iid']
			print cluster[d['uid']]


	with open("user_clus.txt" , "r") as file:
		for line in file :
			n = line.split(';')
			# print n
			d = {}
			d['uid'] = int(n[0])
			d['iid'] = int(n[1])
			user_cluster[d['uid']] = d['iid']


	ff=open("qwer.txt","w")
	for i in range(len(cluster)):
		print cluster[i]
		print "hatt"
		ff.write(str(cluster[i]))

	# for i in range(len(data)):
	# 	print data[i]
	# print "max uid %d max iid %d" %(max_uid , max_iid)
	ending_time = time.time()

	print ("time taken is %f"  %(ending_time - starting_time))

def metrics1():
	for i in range(len(matrix1)):
		sum = 0
		n = 0
		for j in range(len(matrix1[i])):
			if matrix1[i][j] > 0:
				sum += matrix1[i][j];
				n += 1
		if n > 0:
			avg_user_rating1.append(float(sum) / float(n))
		else:
			avg_user_rating1.append(0)
	print avg_user_rating1[944]



	# for i in range(len(avg_user_rating)):
	# 	if avg_user_rating[i] > 0:
	# 		print "user %d rating %f" %(i , avg_user_rating[i])
	
	
	for j in range(len(matrix1[i])):
		sum = 0
		n = 0
		for i in range(len(matrix1)):
			if matrix1[i][j] > 0:
				sum += matrix1[i][j]
				n += 1
		if n > 0:
			sum = sum / float(n)
		avg_item_rating1.append(sum)













def metrics():
	for i in range(len(matrix)):
		sum = 0
		n = 0
		for j in range(len(matrix[i])):
			if matrix[i][j] > 0:
				sum += matrix[i][j];
				n += 1
		if n > 0:
			avg_user_rating.append(float(sum) / float(n))
		else:
			avg_user_rating.append(0)
	print avg_user_rating[944]



	# for i in range(len(avg_user_rating)):
	# 	if avg_user_rating[i] > 0:
	# 		print "user %d rating %f" %(i , avg_user_rating[i])
	
	
	for j in range(len(matrix[i])):
		sum = 0
		n = 0
		for i in range(len(matrix)):
			if matrix[i][j] > 0:
				sum += matrix[i][j]
				n += 1
		if n > 0:
			sum = sum / float(n)
		avg_item_rating.append(sum)

def ItemPearsonCorrelation(xitem , yitem):
	numerator = 0
	fden = 0
	sden = 0
	for i in range(len(matrix)):
		if matrix[i][xitem] > 0 and matrix[i][yitem] > 0:
			a  = (matrix[i][xitem] - avg_item_rating[xitem])
			fden += a * a
			b = (matrix[i][yitem] - avg_item_rating[yitem])
			sden += b * b
			numerator += a * b

	fden = math.sqrt(fden)
	sden = math.sqrt(sden)
	denominator = fden * sden
	if denominator == 0:
		return 0
	return (numerator / denominator)

#Returns similarity between two users 
def UserPearsonCorrelation(xuser , yuser):
	numerator = 0
	fden = 0
	sden = 0
	for i in range(len(matrix[0])):
		if matrix[xuser][i] > 0 and matrix[yuser][i] > 0:
			a  = (matrix[xuser][i] - avg_user_rating[xuser])
			fden += a * a
			b = (matrix[yuser][i] - avg_user_rating[yuser])
			sden += b * b
			numerator += a * b

	fden = math.sqrt(fden)
	sden = math.sqrt(sden)
	denominator = fden * sden
	if denominator == 0:
		return 0
	return (numerator / denominator)

def UserPearsonCorrelation1(xuser , yuser):
	numerator = 0
	fden = 0
	sden = 0
	for i in range(len(matrix1[0])):
		if matrix1[xuser][i] > 0 and matrix1[yuser][i] > 0:
			a  = (matrix1[xuser][i] - avg_user_rating1[xuser])
			fden += a * a
			b = (matrix1[yuser][i] - avg_user_rating1[yuser])
			sden += b * b
			numerator += a * b

	fden = math.sqrt(fden)
	sden = math.sqrt(sden)
	denominator = fden * sden
	if denominator == 0:
		return 0
	return (numerator / denominator)




def ItemWeightedSum(points , user , neighborCount):
	numerator = 0
	denominator = 0
	for i in range(min(neighborCount , len(points))):
		# print "%f %d " %(points[i][0] , points[i][1])
		numerator += points[i][0] * matrix[user][points[i][1]] 
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



def UserWeightedSum(points , item , neighborCount):
	numerator = 0
	denominator = 0
	neighborCount = int(neighborCount)
	#print "neighborCount %d " %(neighborCount)
	for i in range(min(neighborCount , len(points))):
		numerator += points[i][0] * matrix[points[i][1]][item]
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator


def UserWeightedSum1(points , item , neighborCount):
	numerator = 0
	denominator = 0
	neighborCount = int(neighborCount)
	#print "neighborCount %d " %(neighborCount)
	for i in range(min(neighborCount , len(points))):
		numerator += points[i][0] * matrix1[points[i][1]][item]
		denominator += abs(points[i][0])
	if denominator == 0:
		return 0
	return numerator / denominator



def IICF(user , item , neighborCount):
	
	d = []
	for j in range(len(matrix[user])):
		if j != item and cluster[j]==cluster[item] and matrix[user][j] > 0:
		
			d.append( (ItemPearsonCorrelation(j , item) , j) )
	
	d.sort(reverse = True)
	return ItemWeightedSum(d , user , neighborCount)


def UUCF1(user , item , neighborCount):
	rated_users = []	#list of all users that have rated "item"
	for i in range(len(matrix1)):
		if matrix1[i][item] > 0 and i != user and user_cluster[i]==user_cluster[user]:
			rated_users.append( ( UserPearsonCorrelation1(user , i) , i ) )
	rated_users.sort(reverse = True)
	print rated_users
	return UserWeightedSum1(rated_users , item , neighborCount)




def UUCF(user , item , neighborCount):
	rated_users = []	#list of all users that have rated "item"
	for i in range(len(matrix)):
		if matrix[i][item] > 0 and i != user and user_cluster[i]==user_cluster[user]:
			rated_users.append( ( UserPearsonCorrelation(user , i) , i ) )
	rated_users.sort(reverse = True)
	print rated_users
	return UserWeightedSum(rated_users , item , neighborCount)			


def RandomGenerate1(olduserid):
	counter = 0
	file = open("testpoints1" , "w")
	file1=open("tester1.txt","w")
	#while counter < 500:
	for i in range(len(matrix1[0])):
		#print "counter %d" %(counter)
		#x = int(random.random() * 500)
		#y = int(random.random() * 500)
		if matrix1[int(olduserid)][i] == 0:
		#	continue

		#rating =  UUCF(int(olduserid) , i , 7)
		#if rating >= 0.5:
			file.write(str(olduserid) + " " + str(i) + "\n")
		#file1.write(str(rating))
			file1.write("\n")
			counter += 1
	file1.close()





#The RandomGenerate function produces random points in the data matrix
def RandomGenerate(olduserid):
	counter = 0
	file = open("testpoints" , "w")
	file1=open("tester.txt","w")
	#while counter < 500:
	for i in range(len(matrix[0])):
		#print "counter %d" %(counter)
		#x = int(random.random() * 500)
		#y = int(random.random() * 500)
		if matrix[int(olduserid)][i] == 0:
		#	continue

		#rating =  UUCF(int(olduserid) , i , 7)
		#if rating >= 0.5:
			file.write(str(olduserid) + " " + str(i) + "\n")
		#file1.write(str(rating))
			file1.write("\n")
			counter += 1
	file1.close()

def linetest1(neighborCount):
	x11=[]
	correct = float(0)
	incorrect = float(0)
	counter = 0
	invalid = 0
	input_file = open("testpoints1" , "r")
	file2=open("tester4.txt","w")
	for line in input_file:
		points = map(int , line.split(' '))
		x = points[0]
		y = points[1]
		#if (x <= 943):
		rating =  UUCF1(x , y , neighborCount)
		# else:
		# 	rating =  UUCF(x , y , neighborCount)
		if (rating >=3.0 and avg_item_rating1[y] > 3.0):
			file2.write(str(y))
			file2.write("\t")
			file2.write(str(rating))
			file2.write("\n")
			#print "adding"
	file2=open("tester4.txt","r")
	for i in file2:
		points = i.split('\t')
		x=points[0]
		x11.append(x)
	print "where is the control"
	return x11















def linetest(neighborCount):
	x11=[]
	correct = float(0)
	incorrect = float(0)
	counter = 0
	invalid = 0
	input_file = open("testpoints" , "r")
	file2=open("tester3.txt","w")
	for line in input_file:
		points = map(int , line.split(' '))
		x = points[0]
		y = points[1]
		#if (x <= 943):
		rating =  IICF(x , y , neighborCount)
		# else:
		# 	rating =  UUCF(x , y , neighborCount)
		if (rating >=3.5 and avg_item_rating[y] > 3.5):
			file2.write(str(y))
			file2.write("\t")
			file2.write(str(rating))
			file2.write("\n")
			#print "adding"
	file2=open("tester3.txt","r")
	for i in file2:
		points = i.split('\t')
		x=points[0]
		x11.append(x)
	print "where is the control"
	return x11


def algo(olduserid):
	read()
	metrics()
	RandomGenerate(olduserid)
	x22=linetest(17)
	return x22
	print "am i here"

def algo1(olduserid):
	read1()
	metrics1()
	RandomGenerate1(olduserid)
	x32=linetest1(17)
	return x32
	print "am i here"


@app.route('/index')
# @app.route('/index')
def index():
    return render_template("loginsign.html")

@app.route('/musicquery2')
def musicquery2():
    db = MySQLdb.connect("localhost","root","root","music");
    cursor = db.cursor()
    c=cursor.execute("SELECT `User-ID`, CAST(SUM(`Play Count`) as char) FROM `KAGGLE-TRIPLETS` GROUP BY `User-ID` ORDER BY SUM(`Play Count`) DESC limit 10");
    x=list(cursor.fetchall());
    #print x;
    ret_data = {"value": x}
    return jsonify(ret_data)


@app.route('/musicquery1')
def musicquery1():
    db = MySQLdb.connect("localhost","root","root","music");
    cursor = db.cursor()
    c=cursor.execute("SELECT `Song-ID`, CAST(SUM(`Play Count`) as char) FROM `KAGGLE-TRIPLETS` GROUP BY `Song-ID` ORDER BY SUM(`Play Count`) DESC limit 10");
    x=list(cursor.fetchall());
    #print x;
    ret_data = {"value": x}
    return jsonify(ret_data)


@app.route('/')
def loginsign():
	print "qwer"
	return render_template("loginsign.html")

@app.route('/form1', methods=['POST'])
def form1():

	hello1=request.form['userid']
	hello2=request.form['location']
	hello3=request.form['age']
	hello4=request.form['occupation']
	hello5=request.form['gender']

	if (hello1=='' or hello2 == '' or hello3 == '' or hello4 == '' or hello5 == ''):
		return render_template("loginsign.html")
	else:
		target=open("u.user","a")
		print "abeeeeee"
		target.write(str(hello1))
		target.write('|')
		target.write(str(hello3))
		target.write('|')
		target.write(str(hello5))
		target.write('|')
		target.write(str(hello4))
		target.write('|')
		target.write("32114")
		target.write("\n")
		target.close()
		call('timeout 70s python signup.py',shell=True)
		# xx=int(hello1)
		# f=open("u.user","r")
		# h=open("u.user1","w")
		# for line in f:
		# 	lines=line.replace("\n","|")
		# 	words=lines.split("|")
		# 	if words[2]=='M':
		# 		x=100
		# 	else:
		# 		x=200
		# 	y=words[3]
		# 	g=open("u.occupation","r")
		# 	for lines in g:
		# 		line=lines.replace("\n","|")
		# 		word=line.split("|")
		# 		print word[0]+ y+word[1]
		# 		if word[0]==y:
		# 			y=word[1]
		# 	g.close()
		# 	#h.write(str(int(words[0])*5)+"|"+str(words[1])+"|"+str(x)+"|"+str(y)+"|"+"\n")
		# 	h.write(str(int(words[0]))+"|"+str(int(words[1])*2)+"|"+str(x)+"|"+str(y)+"|"+"\n")

		# h.close()


		# plt.style.use("ggplot")
		# from sklearn.cluster import KMeans
		# f=open("w.txt","w")
		# y=[]
		# file = open("u.user1" , "r")
		# for line in file:
		# 	data = line.split('|')
		# 	# print data
		# 	N = []
		# 	for numbers in data:
		# 		try:
		# 			n = float(numbers)
		# 			# f.write(str(n)+" ")
		# 			N.append(n)
		# 		except ValueError:
		# 			pass
		# 	N.pop(0)
		#     	print N
		#     	# f.write('\n')
		#     	y.append(N)
		#     	X=np.array(y)
		# # X=np.array([[1,2,4],[1,2,5],[1,2,9],[1,2,10],[1,2,14],[1,2,15],[1,2,16]])


		# Kmeans=KMeans(n_clusters=20)
		# Kmeans.fit(X)
		# centroids= Kmeans.cluster_centers_
		# labels=Kmeans.labels_
		# print(centroids)
		# for i in centroids:
		# 	f.write(str(1)+";")
		# 	c=1
		# 	for j in i:
		# 		c+=1
		# 		f.write(str(j)+";")
		# 		if(c%4==0):
		# 			f.write("\n")

		# print(labels)
		# p=open("user_c.txt","w")
		# c=1
		# for i in labels:
		# 	p.write(str(c)+";"+str(i)+";"+"\n")
		# 	c+=1
		# p.close()
		# yy=1
		# d=open("user_c.txt","r")
		# for lines in d:
		# 	words=lines.split(";")
		# 	if(int(words[0])==xx):
		# 		print "hello"
		# 		yy=words[1]
		# print "you are assigned cluster number : "+ yy
		# colors= 7*["g.","r.","y.","b.","c.","y."]
		# for i in range(len(X)):
		# 	# print("coordiante",X[i],"label:",labels[i])
		# 	plt.plot(X[i][0],X[i][1],colors[labels[i]],markersize=10)
		# plt.scatter(centroids[:,1],centroids[:,2],marker="x",s=150,linewidths=5,zorder=10)
		# plt.show()



		return render_template("loginsign.html")


@app.route('/form' ,methods=['POST'])#, methods=['GET'])
def form():
	hello1= request.form['userid']
	hello2= request.form['gender']
	print hello1
	print hello2
	if (hello1=='' or hello2 == ''):
		return render_template("loginsign.html")
	target=open("u.user","r")
	flag=0
	for i in target:
		x=i.split("|")
		if(int(x[0]) == int(hello1) and str(x[2]) == hello2):
			print "login succeded"
			session['id']=hello1;
			flag=1
	target.close()
	if(flag==0):
		print "couldnt log"
		return render_template("loginsign.html")
	else:
		return render_template("index.html")


@app.route('/crossdomain')
def crossdomain():
    return render_template("crossdomain.html")

@app.route('/recommend_cross')
def recommend_cross():
	print session['id']
	olduserid=session['id']
	print olduserid
	x31=algo1(olduserid)
	print "qwerttyyyyyt"
	print x31
	x41=[]
	for j in x31:
		target=open("mappingstep2.txt","r")
		for i in target:
			x=i.split(";")
			if(int(j) == int(x[3])):
				x41.append(str(x[1]))
				break
	x51=[]
	pii=[[]]


	#print x41
	for j in x41:
		target=open("kaggle_songs.txt","r")
		for i in target:
			x=i.split(" ")
			if(int(j)==int(x[1])):
				x51.append(x[0])
	#print x51
	db=MySQLdb.connect("localhost","root","root","music")
	cursor=db.cursor()
	for i in x51:
		c=cursor.execute("SELECT * FROM UT where `SONG-ID` like %s",(i))
		x=list(cursor.fetchall())
		pii.append(x)

	#print pii



	lenmusic=len(pii)
	# background_scripts[olduserid] = False
	x21=[]
	read()
	c=0
	for i in range(len(matrix[int(olduserid)])):
		if(matrix[int(olduserid)][i]>0):
	 		c+=1;

	if(c>5):
		x11=algo(int(olduserid))
		print "once or twice"
	else:
		x11=user_clusteri(user_cluster[int(olduserid)])
		print "are u new"
		x21=algo(int(olduserid))
		print "really?"
		print c

	#print x11
	#print x21
 #  x11=[1,2,4,5]
	#pii=[[]]
 #  print x11
	names=[[]]
	db = MySQLdb.connect("localhost","root","root","movielens" );
	cursor = db.cursor()
	for i in x21:
 	  	c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where movie_id like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 1;",[i]);
		x=list(cursor.fetchall())
   		pii.append(x)
	for i in x11:
		c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where movie_id like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 1;",[i]);
		x=list(cursor.fetchall())
		pii.append(x)
    

	print pii
	lenmovies=len(pii)

	pii.append(lenmovies) 
	pii.append(lenmusic)
	print pii

	ret_data = {"value": pii}
	#return json.loads(unicode(opener.open(ret_data), "ISO-8859-1"))
	return jsonify(ret_data)
	#return "hyy"

@app.route('/music')
def music():
    return render_template("music.html")

@app.route('/autocomplete1', methods=['GET'])
def autocomplete1():
    #print "hello"
    hello= str(request.args.get('echoValue'))
    #print hello
    db = MySQLdb.connect("localhost","root","root","music" );
    cursor = db.cursor()
    c=cursor.execute("select `Song-Name` from TPY where `Song-Name` like (%s) limit 10",(hello+"%"));
    x=cursor.fetchall();
    names = []
    for i in x:
        names.append(str(i).strip("(),'"))

    #print names    
    ret_data = {"value": names}
    return jsonify(ret_data)

@app.route('/musicupdate', methods=['GET'])
def musicupdate():
    print "abcdef"
    hello1= str(request.args.get('echoValue'))
    print hello1
    db = MySQLdb.connect("localhost","root","root","music" );
    cursor = db.cursor()
    c=cursor.execute("select `Song-Name`,year,Artist,`Track-ID` from TPY where `Song-Name` like %s limit 10",[hello1+"%"]);
    x=list(cursor.fetchall());
    # t=str(x);
    # t.encode("UTF-8");
    # x = t.split(",")
    # print x;
    
    ret_data = {"value": x}
    
    # #print ret_data
    return jsonify(ret_data)
    #return "ok"



@app.route('/query4')
def query4():
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select `Year-Of-Publication`,count(`Year-Of-Publication`) from Books group by `Year-Of-Publication` order by count(`Year-Of-Publication`) desc limit 5");
    x=list(cursor.fetchall());
    #print x;
    ret_data = {"value": x}
    return jsonify(ret_data)

@app.route('/query3')
def query3():
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select `Publisher`,CAST(avg(`Book-Rating`) as char),count(Books.ISBN) from Books,`BX-Book-Ratings` where Books.ISBN=`BX-Book-Ratings`.ISBN group by `Publisher` having count(Books.ISBN) > 5 order by avg(`Book-Rating`) desc limit 10");
    x=list(cursor.fetchall());
    print x;
    ret_data = {"value": x}
    
#     #print ret_data
    return jsonify(ret_data)

@app.route('/query5')
def query5():
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select `Book-Author`,CAST(avg(`Book-Rating`) as char),count(Books.ISBN) from Books,`BX-Book-Ratings` where Books.ISBN=`BX-Book-Ratings`.ISBN group by `Book-Author` having count(Books.ISBN) > 5 order by avg(`Book-Rating`) desc limit 10");
    x=list(cursor.fetchall());
    print x;
    ret_data = {"value": x}
    
#     #print ret_data
    return jsonify(ret_data)


@app.route('/query2')
def query2():
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute(" select Location,COUNT(Location),CAST(AVG(`Book-Rating`) AS char),`Book-Title`,`Image-URL-M` from `BX-Users`,`BX-Book-Ratings`,Books where `BX-Book-Ratings`.ISBN=Books.ISBN and `BX-Book-Ratings`.`User-ID`=`BX-Users`.`User-ID` group by Location having count(Location) > 50 order by AVG(`Book-Rating`) DESC limit 10");
    x=list(cursor.fetchall());
    print x;
    ret_data = {"value": x}
    
#     #print ret_data
    return jsonify(ret_data)


@app.route('/query1')
def query1():
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select count(`User-ID`),CAST(avg(`Book-Rating`) as char),`Book-Title`,`Image-URL-M` from `BX-Book-Ratings`,Books where `BX-Book-Ratings`.ISBN=Books.ISBN  group by `Book-Title` order by count(`User-ID`) DESC limit 10");
    x=list(cursor.fetchall());
    print x;
    ret_data = {"value": x}
    
    #print ret_data
    return jsonify(ret_data)

   
    #return "ok"




@app.route('/querymaster')
def querymaster():
    
    hello1=str(request.args.get('echo1'))
    hello2=str(request.args.get('echo2'))
    hello3=str(request.args.get('echo3'))
    hello4=str(request.args.get('echo4'))
    hello5=str(request.args.get('echo5'))
    hello6=str(request.args.get('decho1'))
    hello7=str(request.args.get('decho2'))
    hello8=str(request.args.get('decho3'))
    hello9=str(request.args.get('decho4'))
    hello10=str(request.args.get('decho5'))
    hello11=str(request.args.get('decho6'))
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    
    a=hello6;
    b=hello7;
    c=hello8;
    print a;
    print b;
    print c;
    print hello9;
    print hello10;
    if(hello4=='false' and hello5 == 'false'):
        print "hello1"
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and occupations.name like %s and genres.name like %s  and gender like %s  group by ratings.movie_id having cnt>10 order by rate desc limit 10 ",(a+"%",b+"%",c+"%"));
        x= list(cursor.fetchall());
    if(hello4=='false' and hello5 == 'true'):
        print "hello2"
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and occupations.name like %s and genres.name like %s  and gender like %s  group by ratings.movie_id having cnt > %s order by rate desc limit 10 ",(a+"%",b+"%",c+"%",hello11));
        x= list(cursor.fetchall());
    if(hello4=='true' and hello5 == 'false'):
        print "hello3"
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and occupations.name like %s and genres.name like %s  and gender like %s and age > %s and age < %s group by ratings.movie_id having cnt>10 order by rate desc limit 10 ",(a+"%",b+"%",c+"%",hello9,hello10));
        x= list(cursor.fetchall());
    if(hello4=='true' and hello5 == 'true'):
        print "hello4"
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and occupations.name like %s and genres.name like %s  and gender like %s and age > %s and age < %s group by ratings.movie_id having cnt>%s order by rate desc limit 10 ",(a+"%",b+"%",c+"%",hello9,hello10,hello11));
        x= list(cursor.fetchall());
    print x;
    ret_data = {"value": x}
    return jsonify(ret_data)
    
@app.route('/updaterating')
def updaterating():
    print "vishal is legend"
    read()

    hello=str(request.args.get('echoValue'))
    hello1=int(request.args.get('echoValue1'))
    if (matrix[int(session['id'])][hello1] > 0):
    	return "you have already rated with a rating "+ str(matrix[int(session['id'])][hello1])
    else:
    	target=open("u.data","a")
    	target.write(str(session['id']))
    	target.write("\t")
    	target.write(str(hello1)+"\t"+str(hello)+"\t"+"787659878"+ "\n")
        return "thanks for rating"

@app.route('/recommend_olduser')
def recommend_olduser():
    olduserid=session['id']
    print olduserid
    background_scripts[olduserid] = False
    x21=[]
    #threading.Thread(target=lambda: algo(olduserid)).start()
    read()
    c=0
    for i in range(len(matrix[int(olduserid)])):
    	if(matrix[int(olduserid)][i]>0):
    		c+=1;
    if(c>5):
    	x11=algo(int(olduserid))
    else:
    	x11=user_clusteri(user_cluster[int(olduserid)])
    	x21=algo(int(olduserid))

    print x11
    print x21
    #x11=[1,2,4,5]
    pii=[[]]
    # print x11
    names=[[]]
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    for i in x21:
    	c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where movie_id like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 1;",[i]);
       	x=list(cursor.fetchall())
    	pii.append(x)
    for i in x11:
    	c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where movie_id like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 1;",[i]);
       	x=list(cursor.fetchall())
    	pii.append(x)
    

    print pii
    ret_data = {"value": pii}
    return jsonify(ret_data)
   


# @app.route('/recommend_newuser')
# def recommend_newuser():
# 	print "halooqqqqqqqqqqqqqqqqqqqqqqqqqq"
	
	
# 	newuserid=944
# 	moviesid=algo(newuserid)
# 	print moviesid
# 	print len(moviesid)
# 	pii=[[]]
# 	db = MySQLdb.connect("localhost","root","root","movielens")
# 	cursor = db.cursor()
# 	for i in moviesid:
# 		c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where movie_id like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 1;",[i]);
# 		x=list(cursor.fetchall())
# 		pii.append(x)

# 	print pii

# 	ret_data = {"value": pii}
# 	return jsonify(ret_data)
	#return "ok"
    

def user_clusteri(cluster_number):
	metrics()
	arr_clus=[]
	movieid=[]
	rating=[]
	target=open("user_c.txt","r")
	for i in target:
		x=i.split(';')
		user=x[0]
		cluster=x[1]
		#print x[0]
		if (int(x[1]) == cluster_number):
			arr_clus.append(int(x[0]))
	print arr_clus
	print len(arr_clus)
	print "no. of users in cluster"
	
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
		if(avg_item_rating[max2]>4):
			movieid.append(max2)
			rating.append(max1)
	print "cluster moviessss"
	print len(movieid)
	return movieid
	



@app.route('/recommend')
def recommend():
    a="";
    b="";
    c="";
    d="";
    e="";
    f="";
    g="";
    names=[]
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    c=cursor.execute("select genre from dummyvector where score >= 3 limit 10");
    x=list(cursor.fetchall());
    for p in x:
        a= p[0];
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and genres.name like %s  group by ratings.movie_id  having cnt >10 order by rate desc limit 3 ",(a+"%"));
        x=list(cursor.fetchall());
        names=names+x
        print names;

    
    c=cursor.execute("select genre from dummyvector where score <3 or score > 0 limit 2");
    x=list(cursor.fetchall());
    if(x):
        for p in x:
            e= p[0];
            print e;
            p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and genres.name not like %s group by ratings.movie_id  having cnt >50 order by rate desc limit 2 ",(e+"%"));
            x=list(cursor.fetchall());
            names=names+x
            print names

    else:
        p=cursor.execute("select CAST(avg(rating) as char) as rate,ratings.movie_id,count(ratings.movie_id) as cnt ,title,movies.release_date,genres.name from movies,ratings,genres_movies,genres,occupations,users where genres.id=genres_movies.genre_id and genres_movies.movie_id=movies.id and users.id=ratings.user_id and users.occupation_id=occupations.id and movies.id=ratings.movie_id and occupations.name like 'Engineer' and gender like 'M%' and age>0 and age<40 group by ratings.movie_id having cnt > 10 order by rate desc limit 10 ");
        x=list(cursor.fetchall());
        names=names+x
        print names;
        
    ret_data = {"value": names}
    return jsonify(ret_data)
    

@app.route('/rate')
def rate():
    # print "yogesh is awesome"
    hello= str(request.args.get('echoValue'))
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    c=cursor.execute("select title,movie_id,CAST(AVG(rating) AS CHAR) AS `Average`,count(*) from ratings,movies where movies.id=%s and movie_id=%s group by movie_id",(hello,hello));
    x=list(cursor.fetchall());
    #print x;
    ret_data = {"value": x}
    return jsonify(ret_data)
    #return "ok"

@app.route('/movies')
def movies():
    return render_template("movies.html")

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    #print "hello"
    hello= str(request.args.get('echoValue'))
    #print hello
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    c=cursor.execute("select `title` from movies where `title` like (%s) limit 10",(hello+"%"));
    x=cursor.fetchall();
    names = []
    for i in x:
        names.append(str(i).strip("(),'"))

    #print names    
    ret_data = {"value": names}
    return jsonify(ret_data)

@app.route('/moviesupdate', methods=['GET'])
def moviesupdate():
    print "hellodudesss"
    hello1= str(request.args.get('echoValue'))
    print hello1
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    c=cursor.execute("select title,name,release_date,movies.id from genres,genres_movies,movies where title like %s and movies.id=genres_movies.movie_id and genres_movies.genre_id=genres.id limit 10;",[hello1+"%"]);
    x=list(cursor.fetchall());
    print "hellllloooo"
    print x;
    
    ret_data = {"value": x}
    
    #print ret_data
    return jsonify(ret_data)

@app.route('/books')
def books():
    
    print "hello";
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()

    c=cursor.execute("select * from Books limit 20");
    x=cursor.fetchone()[0];
    #print x;
    return render_template("books.html");

@app.route('/echo/', methods=['GET'])
def echo():
    ret_data = {"value": request.args.get('echoValue')}
    return jsonify(ret_data)


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/signUpUser', methods=['GET'])
def signUpUser():
    # print "hello"
    hello= str(request.args.get('echoValue'))
    #print hello
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select distinct`Book-Author` from Books where `Book-Author` like (%s) limit 5",(hello+"%"));
    x=cursor.fetchall();
    names = []
    for i in x:
        names.append(str(i).strip("(),'"))
    c=cursor.execute("select `Book-Title` from Books where `Book-Title` like (%s) limit 5",(hello+"%"));
    x=cursor.fetchall();
    for i in x:
        names.append(str(i).strip("(),'"))

    # print names;
    
    # print "hiyyyy"
    names.reverse();
    user =  "hi"
    ret_data = {"value": names}
    
    # print ret_data
    return jsonify(ret_data)

@app.route('/tabledatafunction', methods=['GET'])
def tabledatafunction():
    # print "hello"
    hello1= str(request.args.get('echoValue'))
    print hello1
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    c=cursor.execute("select `Book-Title`,`Book-Author`,`Year-Of-Publication`,`Publisher`,`Image-URL-M` from Books where `Book-Title` like %s limit 10;",[hello1+"%"]);
    x=list(cursor.fetchall());
    #print x;
    # names = []
    # for i in x:
    #     names.append(str(i).strip("(),'"))
    #names = [w.replace(' " ', ' \' ') for w in names]

    # c=cursor.execute("select `Book-Author` from Books where `Book-Title` like %s limit 1;",[hello1+"%"]);
    # x=cursor.fetchall();
    # for i in x:
    #     names.append(str(i).strip("(),'"))
    # c=cursor.execute("select `Year-Of-Publication` from Books where `Book-Title` like %s limit 1;",[hello1+"%"]);
    # x=cursor.fetchall();
    # for i in x:
    #     names.append(str(i).strip("(),'"))
    # c=cursor.execute("select `Publisher` from Books where `Book-Title` like %s limit 1;",[hello1+"%"]);
    # x=cursor.fetchall();
    # for i in x:
    #     names.append(str(i).strip("(),'"))
    # c=cursor.execute("select `Image-URL-M` from Books where `Book-Title` like %s limit 1;",[hello1+"%"]);
    # x=cursor.fetchall();
    # for i in x:
    #     names.append(str(i).strip("(),'"))

    #print names;
    
    # # print "hiyyyy"
    # user =  "hi"
    ret_data = {"value": x}
    
    #print ret_data
    return jsonify(ret_data)
    #return "ok"
@app.route('/visualisation')
def chart():
    
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    y=[]
    for x in xrange(1,11):
    
        c=cursor.execute("select count(*) from `BX-Book-Ratings` where `Book-Rating`= %s",[x]);
        y=y+list(cursor.fetchall());
       
    return render_template("visualisation.html", arr=y);
@app.route('/visualisation1')
def chart1():
    
    y=[278858,271389,1149480]

    
    return render_template("visualisation1.html", arr=y);

@app.route('/visualisation2')
def chart2():    
    db = MySQLdb.connect("localhost","root","root","books" );
    cursor = db.cursor()
    y=[]
    for x in xrange(1,11):
        c=cursor.execute("select count(*) from `BX-Users` where `age`> %s and age <= %s",[(x-1)*10,(x*10)]);
        y=y+list(cursor.fetchall());
       
    return render_template("visualisation2.html", arr=y);

    

@app.route('/visualisation3')
def chart3():    
    
    y=[1305,1267,1200,1192,1184,1180,1150,1148,1141,1140]
    
    return render_template("visualisation3.html", arr=y);

@app.route('/visualisation4')
def chart4():    
    
    y=[19293,21604,23472,27389,29618,34960,37546,39414,34770,31051];
        
    return render_template("visualisation4.html", arr=y);

@app.route('/visualisation5')
def chart5():    
    
    y=[(35432,'Undo'),(33179,'Revelry'),(24359,'sehr komisch'),(19454,'horn concrto'),(17115,'dog days are over'),(14279,'secrets'),(12392,'aint misbehavin'),(11610,'invalid'),(10794,'catch you baby'),(10515,'you are the one')];
    print y;  
    return render_template("visualisation9.html", arr=y);

@app.route('/visualisation6')
def chart6():
    
    y=[943,1682,100000]

    
    return render_template("visualisation6.html", arr=y);
@app.route('/visualisation7')
def chart7():
    
    y=[670,243]

    
    return render_template("visualisation7.html", arr=y);

@app.route('/visualisation8')
def chart8():    
    print "hello"
    db = MySQLdb.connect("localhost","root","root","movielens" );
    cursor = db.cursor()
    y=[]
    for x in xrange(1,18):
        c=cursor.execute("select count(*),name from users,occupations where users.occupation_id=occupations.id and occupations.id=%s group by name;",[x]);
        y=y+list(cursor.fetchall());
        print y;
       
    return render_template("visualisation8.html", arr=y);