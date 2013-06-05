# AUC - Text Mining and Collective Intelligence
# Final Project: Coronation on Twitter
# Leonard Wein

import re
import pymongo as pm 

if __name__ == '__main__' :

	# Connect to database
	connection = pm.Connection("zookst11.science.uva.nl", 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate("read", "only4you")

	# Function that gets tweets from the database and writes them to a text file in a list format.
	def SaveTweets(number):	
		out = open('tweets.txt','w')
		TweetList = []
		for post in dbnp.tweets.find({'text':{'$exists':True}})[:number]:
			TweetList.append(post)
		out.write('{0}'.format(TweetList))

	# Function that gets tweets from the database and writes them to a text file in a list format.
	def CheckLanguages(number):	
		for post in dbnp.tweets.find({'text':{'$exists':True}})[:number]:
			try:
				print post['lang']
			except:
				pass
    	
	# Function to grab all tweet id's and corresponding tweet texts from the database. Outputs it in a text-file.
	def GetTweetTexttxt(number):
		TweetTXT = open('TweetTexts.txt','w')
		for post in dbnp.tweets.find({'lang':'nl'})[:number]:
			try:
				TweetTXT.write('{0}'.format(post['id']))
				TweetTXT.write('\t{0}'.format(post['lang'].encode('utf-8')))
				TweetTXT.write('\t{0}'.format(post['text'].encode('utf-8').lower()))
				TweetTXT.write('\n')
			except:
				pass


	# Function to grab all tweet id's and corresponding tweet texts from the database. Outputs it in a text-file.
	def GetTweetTextDict(number):
		TweetTokens = open('TweetDict.txt','w')
		TweetDict = {}
		for post in dbnp.tweets.find({'text':{'$exists':True}, 'lang':'nl'})[:number]:
			TweetID = post['id']
			TweetText = CleanTweet(post['text'].encode('utf-8').strip()).split()
			TweetDict[TweetID] = TweetText
		TweetTokens.write('{0}'.format(TweetDict))
		return TweetDict

	# auxiliary function to clean tweet from hyperlinks and loose numbers
	def CleanTweet(tweet):
		cleanedTweet = tweet
		cleanedTweet = re.sub('(http://)[a-zA-Z0-9]*.[a-zA-Z0-9/]*(.[a-zA-Z0-9]*)?', '', cleanedTweet) # remove links
		cleanedTweet = re.sub('[0-9]', '', cleanedTweet) # remove pure numbers
		return cleanedTweet




	# ------------- Function Calls -------------------------------

	#GetTweetTextDict(400)
	# SaveTweets(10)
	




