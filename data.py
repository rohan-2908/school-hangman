import pymysql as pms

def setup():				#Sets up the database
	con=pms.connect(host='localhost',user='root',passwd='tiger')
	csr=con.cursor()

	csr.execute('CREATE DATABASE IF NOT EXISTS PlayerData')
	csr.execute('USE PlayerData')
	csr.execute('''CREATE TABLE IF NOT EXISTS players(
			  NAME char(20) NOT NULL,
			  USERID char(20) PRIMARY KEY,
			  PASSWD char(20) NOT NULL,
		  	  WRDS_GUESSED text,
			  NUM_GUESSED int)''')


def cnt():				#Initializes on each execution
	cnt.con=pms.connect(host='localhost',user='root',passwd='tiger',database='PlayerData')
	cnt.csr=cnt.con.cursor()


def DataAdder(PData,old_user=None):				#Adds data to database
	cnt()
	if old_user==None:
		query='INSERT INTO players VALUES("{}","{}","{}","{}",{})'.format(PData['name'],PData['userid'],PData['passwd'],PData['words'],PData['g.num'])
	else:
		query='UPDATE players SET name="{}", userid="{}", passwd="{}", wrds_guessed="{}", num_guessed={} WHERE userid="{}"'.format(PData['name'],PData['userid'],PData['passwd'],PData['words'],PData['g.num'],old_user)
	cnt.csr.execute(query)
	cnt.con.commit()
	cnt.con.close()


def Verifier(passwd):				#Verifies player credentials
	cnt()

	query='SELECT PASSWD FROM players WHERE PASSWD="{}"'.format(passwd)

	cnt.csr.execute(query)
	data=cnt.csr.fetchone()
	cnt.con.close()
	if data: return 'verified'


def UserVeri(userid):				#Verifies user id
	cnt()
	query='SELECT USERID FROM players WHERE userid="{}"'.format(userid)
	cnt.csr.execute(query)
	data=cnt.csr.fetchone()
	if data==None: return ''
	elif userid in data: return 'user exists'


def LoadWord(code,Glist):				#Loads the word from stored words to guess
	import pickle
	from random import choice

	with open('Words.dat',"rb") as word_file:

		for count in range(code+1):
			words=pickle.load(word_file)
			if count==code:
				while True:
					word=choice(words)
					if word not in Glist[code]: return word


def LoadData(userid):				#Loads data from the database
	from ast import literal_eval
	cnt()

	query='SELECT * FROM players WHERE userid="{}"'.format(userid)
	cnt.csr.execute(query)
	data=cnt.csr.fetchone()
	cnt.con.close()

	DinFormat={'name':data[0],'userid':data[1],'passwd':data[2],'words':literal_eval(data[3]),'g.num':data[4]}

	return DinFormat


def LBoard():
	cnt()

	query='''SELECT USERID, NUM_GUESSED FROM players
		 WHERE NUM_GUESSED > 0
		 ORDER BY NUM_GUESSED DESC
		 LIMIT 5'''
	cnt.csr.execute(query)
	final_LB=[]
	while True:
		data=cnt.csr.fetchone()
		if not data: break
		DinFormat={'userid':data[0],'g.num':data[1]}
		final_LB.append(DinFormat)

	return final_LB
