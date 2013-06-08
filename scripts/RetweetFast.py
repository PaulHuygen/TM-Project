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


	

	# Get Retweet frequencies, i.e. the number of times a user is retweeted in the dataset.
	def RetweetFreq(number):
		RTFreq = open( "RetweetedList.p", "wb" )
		RTFreqtxt = open('RetweetFreq.txt','w')
		Retweeted = {}
		RetweetedUsers = []
		mention = ''
		count = 0
		# make sure the looped list does not contain more elements than there are tweets from the query
		TotalTweets = dbnp.tweets.find({'text' : {'$regex': u'^RT'}}, {'_id':0,'id':1,'text':1, 'place':1}).count()
		if number > TotalTweets:
			number = TotalTweets
		print number
		for post in dbnp.tweets.find({'text' : {'$regex': u'^RT'}}, {'_id':0,'id':1,'text':1, 'place':1})[:number]:
			try:
				mention = re.search('@([A-Za-z0-9_]+)', post['text']).group(0)
				mention = re.sub('@','',mention)
				if mention in Retweeted.keys():
					Retweeted['{0}'.format(mention)]+=1
				else: 
					Retweeted['{0}'.format(mention)]=1
			except:
				pass
			count += 1
			print count
		RetweetedSorted = sorted(Retweeted.iteritems(), reverse=True, key=operator.itemgetter(1))
		pickle.dump(RetweetedSorted, RTFreq)
		# RTFreqtxt.write('{0}'.format(RetweetedSorted[:25]))
		# print RetweetedSorted[:25]
		return RetweetedSorted[:25]


	# Aux function to import serialized file again without error (from pickle libary)
	# Returns a list of usernames (without @) and their RT frequencies. Input integer 
	# prescribes minimum retweet frequency.
	def OpenSerialization(number):
		TopList = pickle.load(open('RetweetedList757000backup.p', 'rb'))
		CleanedTopList = []
		for i in TopList:
			if i[1] > number:
				CleanedTopList.append((re.sub('@','',i[0]), i[1]))
		print len(CleanedTopList)
		return CleanedTopList

	ExampleList = ['Koningin_NL']


	# Retrieve additional information (e.g. tweet texts, location, etc.) for 
	# highly retweeted users. This is an optimized version that retrieves all user information
	# collectively by looping over a pre-generated list of all the usernames. This sped up the 
	# computation by orders of magnitude, which was crucial to obtain users for RT frequency down to 10.
	def GetPopularTweeters(ls):
		# dump file for popular retweeters
		TopRetweeter = open('TopRetweeterFast.p', 'wb')
		TweetDict = {}
		UserList = []
		User = ''
		for i in ls:
			TweetDict['{0}'.format(i[0])]= {}
			TweetDict['{0}'.format(i[0])]['text']=[]
			TweetDict['{0}'.format(i[0])]['Retweet_Freq']=i[1]
			TweetDict['{0}'.format(i[0])]['TweetsCount']=0
			UserList.append(i[0])
		# counter 
		c=0
		for post in dbnp.tweets.find({'user.screen_name' : {'$in':UserList}}):
			User = post['user']['screen_name']	
			TweetDict[User]['text'].append(post['text'])
			TweetDict[User]['TweetsCount']+=1
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
				TweetDict[User]['TotalTweetsCount']=post['user']['statuses_count']
				TweetDict[User]['Following']=post['user']['friends_count']
			except:
				pass
			c+= 1
			print c
		pickle.dump(TweetDict,TopRetweeter)
		print TweetDict.items()[:1]
		return TweetDict



	# ------------- Function Calls -------------------------------

	# RetweetFreq(1000000)
	GetPopularTweeters(OpenSerialization(10))
	# OpenSerialization(10)
	
# pickle.load(open('TopRetweeter_top25.p', 'rb'))
# pickle.load(open('RetweetedList_complete.p', 'rb'))
# pickle.load(open('TopRetweeter-100retweets.p', 'rb'))
# pickle.load(open('TopRetweeterFast-10retweets.p', 'rb'))
# pickle.load(open('SentimentAnalysis-19000-nl-geo-TextExists-NA.p', 'rb'))








	