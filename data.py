import pymysql as pms
from efx import Printer

def setup():				#Sets up the database
	con=pms.connect(host='localhost',user='root',passwd='tiger')
	csr=con.cursor()

	csr.execute('CREATE DATABASE IF NOT EXISTS PlayerData')
	csr.execute('USE PlayerData')
	csr.execute('''CREATE TABLE IF NOT EXISTS players(
			  NAME char(10) NOT NULL,
			  USERID char(10) PRIMARY KEY,
			  PASSWD char(15) NOT NULL,
		  	  WRDS_GUESSED text,
			  NUM_GUESSED int)''')


def connect():				#Initializes on each execution
	connect.con=pms.connect(host='localhost',user='root',passwd='tiger',database='PlayerData')
	connect.csr=connect.con.cursor()


def DataAdder(PData,old_user=None):				#Adds data to database
	connect()
	if old_user==None: query='INSERT INTO players VALUES("{}","{}","{}","{}",{})'.format(PData['name'],PData['userid'],PData['passwd'],PData['words'],PData['g.num'])
	else: query='UPDATE players SET name="{}", userid="{}", passwd="{}", wrds_guessed="{}", num_guessed={} WHERE userid="{}"'.format(PData['name'],PData['userid'],PData['passwd'],PData['words'],PData['g.num'],old_user)
	connect.csr.execute(query)
	connect.con.commit()
	connect.con.close()


def Verifier(userid,passwd):				#Verifies player credentials
	connect()

	query='SELECT USERID, PASSWD FROM players WHERE USERID="{}" AND PASSWD="{}"'.format(userid,passwd)

	connect.csr.execute(query)
	data=connect.csr.fetchone()
	connect.con.close()
	if data: return 'verified'


def UserVeri(userid):				#Verifies user id
	connect()
	query='SELECT USERID FROM players WHERE userid="{}"'.format(userid)
	connect.csr.execute(query)
	data=connect.csr.fetchone()
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
	connect()

	query='SELECT * FROM players WHERE userid="{}"'.format(userid)
	connect.csr.execute(query)
	data=connect.csr.fetchone()
	connect.con.close()

	DinFormat={'name':data[0],'userid':data[1],'passwd':data[2],'words':literal_eval(data[3]),'g.num':data[4]}

	return DinFormat


def LBoard():
	connect()

	query='''SELECT USERID, NUM_GUESSED FROM players
		 WHERE NUM_GUESSED > 0
		 ORDER BY NUM_GUESSED DESC
		 LIMIT 5'''
	connect.csr.execute(query)
	final_LB=[]
	while True:
		data=connect.csr.fetchone()
		if not data: break
		DinFormat={'userid':data[0],'g.num':data[1]}
		final_LB.append(DinFormat)

	return final_LB
