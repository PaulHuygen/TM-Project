import sys
import nltk

f=open("myfile.txt")
text=f.read().lower()
f.close()

print "finished reading"

tokens=nltk.word_tokenize(text)
clean_tokens=[]

wordfile=open("wordfile.txt",'w')

print "sdfsd"

fd=nltk.FreqDist(tokens)
for token in fd:
	if fd[token]>50 and token not in nltk.corpus.stopwords.words('dutch') and token not in nltk.corpus.stopwords.words('english') and token.isalpha():
		wordfile.write(token.encode("utf-8") + ':' + str(fd[token]))

wordfile.close()






