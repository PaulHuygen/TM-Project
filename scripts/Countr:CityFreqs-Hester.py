#count all tweets
#count tweet with geolocation

import pymongo as pm 

connection = pm.Connection("zookst11.science.uva.nl", 27017) 
dbnp = connection.queensday2013 
dbnp.authenticate("admin", "queensday") 

#To get tweets only with geolocation:
for post in dbnp.tweets.find({"geo.coordinates": {"$exists": True}}):
    print "latitude: %f, longitude: %f" % (post["geo"]["coordinates"][0],  post["geo"]["coordinates"][1])

#get countt weets with geolocation
print dbnp.tweets.find({"geo.coordinates": {"$exists": True}}).count()

#find tweets with specific location

tweet_country={}

for post in dbnp.tweets.find({"place": {"$exists": True}}): #be sure to take this 100 out later!
	if post["place"] is None:continue
	country=post["place"]["country"] # shows the country
	if country in tweet_country:
		tweet_country[country]+=1
	else:
		tweet_country[country]=1


tweet_country

tweet_fullname={}

for post in dbnp.tweets.find({"place": {"$exists": True}})[:100000]: #be sure to take this 100 out later!
	if post["place"] is None:continue
	tweetcity=post["place"]["full_name"]
	incity=False
	try:
		for city in citylist:
			if city.decode('latin1') in tweetcity.decode('latin1'):
				incity=True
				break
		if incity==False:continue
		if city in tweet_fullname:
			tweet_fullname[city]+=1
		else:
			tweet_fullname[city]=1
	except UnicodeEncodeError:continue

tweet_fullname

#take the ones with the lowest counts out! There are weird signs that aren't countries. Also, think of a solution for Netherlands vs. Nederland

    print post["place"]["full_name"] # the name of the location
	print post["place"]["place_type"] # city, etc.

#dump info. cPickle/cpickle
cpickle.dump(tweet_country,"/Users/Hester/Documents/AUC/TextMiningCollectiveIntelligence/countrydict")

#load it
tweet_country=cpickle.load("/Users/Hester/Documents/AUC/TextMiningCollectiveIntelligence/countrydict")


#When we have filled the lists for tweets_etc, we need to do a few things:
#for the bar chart count per country: filter out everything in the list except the name
#of the country (start by filtering everything except dictionary). go through this list of country names, and make a new list (per country)
#if one doesn't exist already.
#per city: only in the Netherlands


#directly let the countries go into a list. 

#list 50 greatest cities Netherlands

citylist=['Amsterdam','Rotterdam','Den Haag','Utrecht','Eindhoven','Tilburg','Groningen','Almere','Breda','Nijmegen','Enschede','Apeldoorn','Haarlem','Arnhem','Amersfoort','Zaanstad','Haarlemmermeer','Den Bosch','Zoetermeer','Zwolle','Maastricht','Leiden','Dordrecht','Dordrecht','Ede','Emmen','Westland','Venlo','Delft','Deventer','Leeuwarden','Alkmaar','Sittard-Geleen','Helmond','Heerlen','Hilversum','Oss','Amstelveen','Súdwest-Fryslân','Hengelo','Purmerend','Roosendaal','Schiedam','Lelystad','Alpen aan den Rijn','Almelo','Leidschendam-Voorburg','Spijkernisse','Hoorn','Gouda','Vlaardingen']




#for values in dict tweet_country:
valuecountry=tweet_country.values()
cleanvaluecountry=[x for x in valuecountry if x>=10]
save_country=tweet_country

for key,value in save_country.items():
	if value==1:
		print key

Do this for value 1,2,3,4,5,6,7,8,9,10

Create a list of these county names. Then just as in code for tweet_country, if country in this list, delete it form save_country
create a chart from the left over country (top 10)


