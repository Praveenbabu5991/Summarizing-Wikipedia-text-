# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 23:16:20 2018

@author: Bolt
"""
import re
import bs4 as bs 
import urllib.request
import nltk
import heapq

#fetching data
source=urllib.request.urlopen('https://en.wikipedia.org/wiki/Global_warming').read()

soup = bs.BeautifulSoup(source,'lxml')#lxml is a parser #it will be some what clear than source

text=""

for paragraph in soup.find_all('p'):
    text += paragraph.text
    
    
text=re.sub('\[[0-9]*\]',' ',text)
text=re.sub('\s+',' ',text)
clean_text=text.lower()
clean_text=re.sub('\W',' ',clean_text)
clean_text=re.sub('\d',' ',clean_text)
clean_text=re.sub('\s+',' ',clean_text)
    

sentences=nltk.sent_tokenize(text)

stopwords=nltk.corpus.stopwords.words('english')

#counting the frequency of words
word2count={}

for word in nltk.word_tokenize(clean_text):
    if word not in stopwords:
        if word not in word2count.keys():
            word2count[word]=1
        else:
            word2count[word]+=1
  
#weighted frequency
for key in word2count.keys():
    word2count[key]=word2count[key]/max(word2count.values())
          
#score of each sentence
sent2score={}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sent2score.keys():
                    sent2score[sentence]=word2count[word]
                else:
                    sent2score[sentence]+=word2count[word]
                    
            
best_sentences=heapq.nlargest(5,sent2score,key=sent2score.get)       

for sentence in best_sentences:
    print(sentence)
    

            
            