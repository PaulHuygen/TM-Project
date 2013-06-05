import re
import pymongo as pm 
from bson.son import SON

if __name__ == '__main__' :

	# Connect to database
	connection = pm.Connection("zookst11.science.uva.nl", 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate("read", "only4you")

	# ----------------------------------------
	# Basic Statistics run directly on MongoDB database using count(), aggregate() and regex() commnads

	
	def stats():
		print 'Total number of tweets'
		print dbnp.tweets.find().count()
		print 'Total number of retweeted tweets'
		print dbnp.tweets.find({'text' : {'$regex': u'^RT'}}).count()
		print 'Number of valid tweets defined as containing text, language indication, and place information'
		print dbnp.tweets.find({'text':{'$exists':True}, 'lang':{'$exists':True}, 'place':{'$exists':True}}).count()
		print 'Number of Dutch language tweets in db'
		print dbnp.tweets.find({"lang": "nl"}).count()
		print 'Number of English language tweets in db'
		print dbnp.tweets.find({"lang": "en"}).count()
		print 'Number of tweets in db without language indication'
		print dbnp.tweets.find({"lang": "en"}).count()
		print 'Language Stats'
		print dbnp.tweets.aggregate([
			{"$group": {"_id": "$lang", "count": {"$sum": 1}}},
			{"$sort": SON([("count", -1), ("_id", -1)])}])['result']
		print 'Country Stats'
		print dbnp.tweets.aggregate([
					{"$group": {"_id": "$place.country", "count": {"$sum": 1}}},
					{"$sort": SON([("count", -1), ("_id", -1)])}])['result']
		print 'City Stats'
		print dbnp.tweets.aggregate([
					{"$group": {"_id": "$place.name", "count": {"$sum": 1}}},
					{"$sort": SON([("count", -1), ("_id", -1)])}])['result']
		print 'Number of Retweets'
		print dbnp.tweets.find({'text' : {'$regex': u'RT'}}).count()





	# ------------- Function Calls -------------------------------

	# stats()