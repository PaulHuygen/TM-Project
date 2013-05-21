AUC TMCI

hesinga
CollectiveIntelligence

outside of python, sudo easy_install twitter 
(control c to stop downloading tweets)

from twitter import *

ot='630128264-FAWYUYkMRCZzJVX4Lxim94QdcxqIkMaPoPCNGNmd'
os='xnvkrDAhKMOoBL71v4qPRGHjML58yIv9M1M7aSTdw0'
ck='lWBnOiWvfCAW8ZeBPw'
cs='D55XxKwB5tNc8alTZpcJOzOYXSQq6zyvg5cOWEPyc'

twitter_search=Twitter(auth=OAuth(ot,os,ck,cs))


#for tweet in t.statuses.sample(): 
#	print tweet



#for count,tweet in enumerate(t.statuses.sample()):
#	if "text" in tweet:
#		print tweet["text"]
#	if count>5:
#		break






#2.1

def getTweets(username):
	Tweetdictionary={}
	count=0
	oldesttweet=0
	for tweet in twitter_search.statuses.user_timeline(screen_name=username,count=200):
		Tweetdictionary[tweet["id"]]=tweet["text"]
		count +=1
		oldesttweet=tweet["id"]
		if count>600:
			break
	while count<600:
		for tweet in twitter_search.statuses.user_timeline(screen_name=username,count=200, max_id=oldesttweet):
			Tweetdictionary[tweet["id"]]=tweet["text"]
			count +=1
			oldesttweet=tweet["id"]
			if count>600:
				break
		return Tweetdictionary

getTweets("rihanna")

#2.2

import re
from ttp import ttp
p=ttp.Parser()
tweetDict=getTweets('rihanna')

def filterTweets(tweetDict):
  tweetDict2={}
  for tweetid, tweettext in tweetDict.iteritems():
    result=p.parse(tweettext)
    cleanedtweet=tweettext
    for user in result.users:
      cleanedtweet=re.sub(re.escape(user)," ",cleanedtweet)
    for url in result.urls:
      cleanedtweet=re.sub(re.escape(url)," ",cleanedtweet)
    cleanedtweet=re.sub('#'," ", cleanedtweet)
    cleanedtweet=re.sub('@'," ", cleanedtweet)
    cleanedtweet=re.sub(r"\s+"," ", cleanedtweet)
    cleanedtweet=cleanedtweet.lower()
    tweetDict2[tweetid]=cleanedtweet
  return tweetDict2

#This function cleans the tweets. That is to say, the usernames, urls, and 'strange' symbols
#are escaped, and replaced by spaces. At the end all letters are set to lower case only.

#assignemtn 2.3
import collections

def wordcount(text):
	counts=collections.defaultdict(lambda:0)
	for word in re.split("\W+",text):
		counts[word]+=1
	return counts 

def createWordTable(tweets):
	out=open("table.txt","w")
	wordlist=set()
	Tweetlist=filtertweets(tweets))
	for tweetid,tweettext in Tweetlist.iteritems():
		for word in re.split("\W+",tweettext):
			wordlist.add(word)
	wordlist=list(wordlist)
	for tweetid,tweettext in Tweetlist.iteritems():
		tweetcounts=wordcount(tweettext)
		out.write(tweetid)
		for word in wordlist:
			out.write("\t{0}".format(tweetcounts[word]))
		out.write("\n")
			print tweetcounts[word]




