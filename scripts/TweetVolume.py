import time
import pymongo as pm 
# import pickle
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


if __name__ == '__main__' :	
	

	# Connect to database
	connection = pm.Connection('zookst11.science.uva.nl', 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate('read', 'only4you')

	# 
	def TweetVolume(number):
		
		# For how to write to CSV-file: http://stackoverflow.com/questions/8685809/python-writing-a-dictionary-to-a-csv-file-with-one-line-for-every-key-value
		writer = csv.writer(open('TweetVol.csv', 'wb'))
		
		# make sure the looped list does not contain more elements than there are tweets from the query
		TotalTweets = dbnp.tweets.find({'text' : {'$ne': None}}).count()
		if number > TotalTweets:
			number = TotalTweets
		print number
		TweetFreq = {}
		c = 0
		# {'$regex': u'^RT'}
		for post in dbnp.tweets.find({'text' : {'$ne': None}}, {'_id':0,'created_at':1})[:number]:
			# For timestampe conversion: http://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
			ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(post['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
			# month = ts[5:7]
			# day = ts[8:10]
			# Hour = ts[11:13]
			TKey = ts[0:13]
			if TKey in TweetFreq.keys():
				TweetFreq['{0}'.format(TKey)]+=1
			else:
				TweetFreq['{0}'.format(TKey)]=1
		for key, value in TweetFreq.items():
			writer.writerow([key, value])
		print TweetFreq
		return TweetFreq



	# ------------- Function Calls -------------------------------

	# TweetVolume(2000000)	



