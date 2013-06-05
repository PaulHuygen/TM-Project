import re
import operator
import pickle
import pymongo as pm 



if __name__ == '__main__' :	
	

	# ----------------------------------------
	# Find the most relevant users by number of retweets
	# dbnp.tweets.find({'text' : {'$regex': u'RT'},'place':{'$ne': None}}, {'id':1,'text':1,'place':1})[:10]:
	# Source for serialization: http://stackoverflow.com/questions/899103/python-write-a-list-to-a-file

	# Connect to database
	connection = pm.Connection("zookst11.science.uva.nl", 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate("read", "only4you")


	RTFreq = open( "RetweetedList.p", "wb" )
	RTFreqtxt = open('RetweetFreq.txt','w')

	# Get Retweet frequencies, i.e. the number of times a user is retweeted in our db
	def RetweetFreq(number):
		Retweeted = {}
		mention = ''
		for post in dbnp.tweets.find({'text' : {'$regex': u'^RT'}}, {'_id':0,'id':1,'text':1, 'place':1})[:number]:
			try:
				mention = re.search('@([A-Za-z0-9_]+)', post['text']).group(0)
				if mention in Retweeted.keys():
					Retweeted['{0}'.format(mention)]+=1
				else: 
					Retweeted['{0}'.format(mention)]=1
			except:
				pass
		RetweetedSorted = sorted(Retweeted.iteritems(), reverse=True, key=operator.itemgetter(1))
		
		pickle.dump(RetweetedSorted, RTFreq)
		# RTFreqtxt.write('{0}'.format(RetweetedSorted[:25]))
		# print RetweetedSorted[:25]
		return RetweetedSorted[:25]

	# Retrieve tweets in db for top 25 retweeted users
	

		


	# ------------- Function Calls -------------------------------

	RetweetFreq(100)










	