import pymongo as pm 

if __name__ == '__main__' :

	# Connect to database
	connection = pm.Connection("zookst11.science.uva.nl", 27017)
	dbnp = connection.queensday2013
	dbnp.authenticate("read", "only4you")

	tweets = open('AllTweets.txt','w')


	def crawler(number):
		tweets.write('[')
		for post in dbnp.tweets.find({'text':{'$exists':True}, 'lang':{'$exists':True}, 'place':{'$exists':True}})[:number]:
			tweets.write('{0},'.format(post))
		tweets.write(']')

	crawler(20)
