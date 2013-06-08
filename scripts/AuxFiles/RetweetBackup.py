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


	

	# Get Retweet frequencies, i.e. the number of times a user is retweeted in our db
	def RetweetFreq(number):
		RTFreq = open( "RetweetedList.p", "wb" )
		# RTFreqtxt = open('RetweetFreq.txt','w')
		Retweeted = []
		RetweetedFreq = {}
		count = 0
		# make sure the looped list does not contain more elements than there are tweets from the query
		TotalTweets = dbnp.tweets.find({'text' : {'$regex': u'^RT'}}, {'_id':0,'id':1,'text':1, 'place':1}).count()
		if number > TotalTweets:
			number = TotalTweets
		print number
		# Extract mentioned usernames to list
		for post in dbnp.tweets.find({'text' : {'$regex': u'^RT'}}, {'_id':0,'id':1,'text':1, 'place':1})[:number]:
			try:
				mention = re.search('@([A-Za-z0-9_]+)', post['text']).group(0)
				mention = re.sub('@','',mention)
				Retweeted.append(mention)
			except:
				pass
			count += 1
			print count
		# create frequency dictionary from list
		UniqueMentions = set(Retweeted)
		print 'ok'
		a =0
		for user in UniqueMentions:
			RetweetedFreq['{0}'.format(user)]=Retweeted.count(user)
			a += 1
			print a
		# SortFrequencies descending
		RetweetedSorted = sorted(RetweetedFreq.iteritems(), reverse=True, key=operator.itemgetter(1))
		# Dump to file
		pickle.dump(RetweetedSorted, RTFreq)
		# RTFreqtxt.write('{0}'.format(RetweetedSorted[:25]))
		# print RetweetedSorted[:25]
		return RetweetedSorted[:25]


	# Aux function to import serialized file again without error (from pickle libary)
	def OpenSerialization():
		TopList = pickle.load(open('RetweetedList100000.p', 'rb'))[:25]
		CleanedTopList = []
		for i in TopList:
			CleanedTopList.append((re.sub('@','',i[0]), i[1]))
		return CleanedTopList

	ExampleList = ['Koningin_NL']


	# Retrieve tweets in db for top 25 retweeted users
	def GetPopularTweeters(ls):
		# dump file for popular retweeters
		TopRetweeter = open('TopRetweeter.p', 'wb')
		TweetDict = {}
		for i in ls:
			User = i[0]
			TweetDict['{0}'.format(User)]= {}
			TweetDict['{0}'.format(User)]['text']=[]
			TweetDict['{0}'.format(User)]['Retweet_Freq']=i[1]
			for post in dbnp.tweets.find({'user.screen_name' : User}):
				TweetDict[User]['text'].append(post['text'])
				try:
					TweetDict[User]['country']=post['place']['country']
					TweetDict[User]['city']=post['place']['name']
				except:
					pass
				try:
					TweetDict[User]['coords']=post['geo']['coordinates']
				except:
					pass
				try:
					TweetDict[User]['lang']=post['lang']
				except:
					pass
				try:
					TweetDict[User]['followers']=post['user']['followers_count']
					TweetDict[User]['TweetsCount']=post['user']['statuses_count']
					TweetDict[User]['Following']=post['user']['friends_count']
				except:
					pass
		pickle.dump(TweetDict,TopRetweeter)
		print TweetDict
		return TweetDict





	# ------------- Function Calls -------------------------------

	RetweetFreq(1000000)
	# GetPopularTweeters(OpenSerialization())










	