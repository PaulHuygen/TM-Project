import pymongo as pm 

connection = pm.Connection("zookst11.science.uva.nl", 27017)
dbnp = connection.queensday2013
dbnp.authenticate("read", "only4you")
#logging.info("...connected") 

c=0
for post in dbnp.tweets.find({'text':{'$exists':True}})[:100]:
    c +=1
    print post['text']
    print c

c=0
out = open('tweets.txt','w')
for post in dbnp.tweets.find({'text':{'$exists':True}})[:100]:
    out.write('{0}'.format(post))
    out.write('\n')
 
# for post in dbnp.tweets.find({'geo.coordinates':{'$exists':True}}).sort('created_dt',-1)[:100]:
#     c +=1
#     try:
#     	print post
#     	print post['text']
#     	print "latitude: %f, longitude: %f" % (post["geo"]["coordinates"][0],  post["geo"]["coordinates"][1])
#     	print c
#     except:
#     	pass

for post in dbnp.tweets.find({'geo.coordinates':{'$exists':True},'retweeted':{'$eq':True}}).sort('created_dt',-1)[:1]:
    c +=1
    try:
    	print post['retweeted']
    	print post['text']
    	print "latitude: %f, longitude: %f" % (post["geo"]["coordinates"][0],  post["geo"]["coordinates"][1])
    	print c
    except:
    	pass    
