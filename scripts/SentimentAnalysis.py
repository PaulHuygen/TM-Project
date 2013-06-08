# -*- coding: utf-8 -*-
# AUC - Text Mining and Collective Intelligence
# Final Project: Coronation on Twitter
# Leonard Wein

import re
import pickle
import pymongo as pm 
import nltk
from string import punctuation
from collections import Sequence
import os.path
import operator


if __name__ == '__main__' :

	# Connect to database
	connection = pm.Connection('zookst11.science.uva.nl', 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate('read', 'only4you')


	# Function retrieves informatino for users according to query criteria, conducts keyword
	# frequency and sentiment analysis.
	def SentimentAnalysis(number):	
		out = open('SentimentAnalysis.p', 'wb')
		TweetList = []
		tweetNo = dbnp.tweets.find({'text' : {'$regex': u'^RT'},'lang':'nl','geo':{'$ne':None}}).count()
		if number > tweetNo: number = tweetNo
		print number
		c=0
		# '$regex': u'^RT'
		# '$ne': None
		for post in dbnp.tweets.find({'text' : {'$regex': u'^RT'},'lang':'nl','geo':{'$ne':None}},{'id':1,'text':1,'place':1,'user':1,'geo':1})[:number]:
			# cPost = CleanedPost -> limit post dictionary to important parts
			cPost={}
			cPost['id']=post['id']
			cPost['text']=post['text']

			TokenizedText = TokenizeTweet(post['text'])
			cPost['tokenizedText']=TokenizedText
			# Freqs = nltk.FreqDist(TokenizedText)
			cPost['WordFreqs']=nltk.FreqDist(TokenizedText)
			Sentiment = SentimentAnalysisAux(TokenizedText)
			cPost['SentimentValue']= Sentiment[1]
			cPost['Sentiment']=Sentiment[0]

			cPost['screen_name']=post['user']['screen_name']
			# Try/Except required to avoid KeyErrors 
			try:
				cPost['user_location']=post['user']['location']
				cPost['country_code']=post['place']['country_code']
				cPost['place_type']=post['place']['place_type']
				cPost['city']=post['place']['name']
			except:
				pass
			try:
				cPost['geo_coords']=post['geo']['coordinates']
			except:
				pass
			try:
				cPost['time_zone']=post['user']['time_zone']
				cPost['followers_count']=post['user']['followers_count']
				cPost['statuses_count']=post['user']['statuses_count']
			except:
				pass
			TweetList.append(cPost)
			c+=1
			print c
		pickle.dump(TweetList, out)
		print TweetList[:1]
		return TweetList

	# auxiliary function to clean tweet (e.g. hyperlinks, punctuation, numbers, lower-case, etc.)
	# remove stopwords, check for correctnes and return list of tokens.
	def TokenizeTweet(tweet):
		cleanedTweet = re.sub('(@\w*)', '', tweet) # remove mentions and make lowercase
		cleanedTweet = re.sub('(http://)[a-zA-Z0-9]*.[a-zA-Z0-9/]*(.[a-zA-Z0-9]*)?', '', tweet) # remove links
		cleanedTweet = re.sub('[0-9]', '', cleanedTweet) # remove pure numbers
		cleanedTweet = re.sub('RT', '', cleanedTweet) # remove RT
		cleanedTweet = cleanedTweet.lower() # make lower-case
		for p in list(punctuation):
				cleanedTweet=cleanedTweet.replace(p,'')
		tokens = nltk.word_tokenize(cleanedTweet)
		cleanTokens = []
		for tok in tokens:
			if tok.isalpha() and tok not in nltk.corpus.stopwords.words('dutch'):
				cleanTokens.append(tok)
		return cleanTokens


	# Create a sentiment dictionary containing all Dutch words and their sentiments. 
	# This lexicon is stored using Pickle and hence this function only has to be called once. 
	# The resulting dictionary is called from file for subesquent analyses.
	lexicon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sentiment_lexicon_nl.txt')
	def CreateSentimentDictionary():
		out = open('SentimentDictionary.p', 'wb')
		with open(lexicon_path) as f:
			sentiment = {}
			for ln in f:
				if ln[0] == '#':
					continue
				w, signs = ln.strip().split(None, 1)
				pos, neg = signs.count('+'), signs.count('-')
				sentiment[w] = (pos / 4., neg / 4.)
		pickle.dump(sentiment,out)
		return sentiment


	# Takes List of Tokens and runs sentiment analysis (dutch only) 
	def SentimentAnalysisAux(tokens):
		lexicon = pickle.load(open('SentimentDictionary.p', 'rb'))
		SentimentVal = 0
		ExistCheck = 0
		for tok in tokens:
			SentimentCalc=0
			try:
				pos, neg = lexicon['{0}'.format(tok)]
				SentimentCalc = pos-neg
				if pos or neg != 0: ExistCheck+=1
			except:
				pass
			SentimentVal = SentimentVal + SentimentCalc
		if ExistCheck == 0:
			sentimentName = 'NA'
		elif SentimentVal == 0:
			sentimentName = 'neutral'
		elif SentimentVal < 0:
			sentimentName = 'negative'
		elif SentimentVal > 0:
			sentimentName = 'positive'
		print (sentimentName,SentimentVal)	
		return (sentimentName,SentimentVal)


	def countSentiments():
		SentimentDict = pickle.load(open('SentimentAnalysis-19000-nl-geo-TextExists-NA.p', 'rb'))
		SentCount = {}
		SentCount['NA']=0
		SentCount['neutral']=0
		SentCount['positive']=0
		SentCount['negative']=0
		for i in SentimentDict:
			if i['Sentiment']=='NA':
				SentCount['NA']+=1
			elif i['Sentiment']=='positive':
				SentCount['positive']+=1
			elif i['Sentiment']=='negative':
				SentCount['negative']+=1
			elif i['Sentiment']=='neutral':
				SentCount['neutral']+=1
		print SentCount
		return SentCount

	# Calculate keywords (by frequency) for positive and negative tweets
	def SentimentKeywords():
		SentimentDict = pickle.load(open('SentimentAnalysis-19000-nl-geo-TextExists-NA.p', 'rb'))
		negTweet = {}
		posTweet = {}

		for i in SentimentDict:
			if i['Sentiment']=='positive':
				for t in i['WordFreqs']:
					if t not in posTweet.keys():
						print t
						print i['WordFreqs'][t]
						posTweet[u'{0}'.format(t)]=i['WordFreqs'][u'{0}'.format(t)]
					else:
						posTweet[u'{0}'.format(t)]+=i['WordFreqs'][u'{0}'.format(t)]
			if i['Sentiment']=='negative':
				for t in i['WordFreqs']:
					if t not in negTweet.keys():
						negTweet[u'{0}'.format(t)]=i['WordFreqs'][u'{0}'.format(t)]
					else:
						negTweet[u'{0}'.format(t)]+=i['WordFreqs'][u'{0}'.format(t)]
		negTweetSort = sorted(negTweet.iteritems(), reverse=True, key=operator.itemgetter(1))
		posTweetSort = sorted(posTweet.iteritems(), reverse=True, key=operator.itemgetter(1))
		print negTweetSort[:10]
		print posTweetSort[:10]
		return negTweetSort[:10]
		return posTweetSort[:10]


			





	# ------------- Function Calls -------------------------------
	
	# Sampel Token-List for SentimentAnalysisAux()
	# sample = ['aanfluiting', 'aangeklaagde','aangenaam','aangeslagen','aangeven','aanhouder','aankleding']
	# SentimentAnalysisAux(sample)

	# Run at the beginning to create Sentiment Dictionary
	# CreateSentimentDictionary()

	# Runs Sentiment Analysis for specified number of tweets.
	# SentimentAnalysis(1000000)

	# countSentiments()
	SentimentKeywords()
	

	
	




