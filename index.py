# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, session, jsonify, redirect
from os import urandom
import pymysql, os
import sys
import subprocess
import re
import math
import nltk
import codecs
import operator
from konlpy.tag import Twitter; t=Twitter()

app = Flask(__name__)
app.secret_key = urandom(16)

host = "128.134.54.31"
id = "ejj"
port = 7778
password="djwkdwh"
name="summary_news"

db = pymysql.connect(host, id, password, name, port, charset="utf8")

# default route
@app.route('/')
def index():
	return redirect(url_for('main'))

# main page
@app.route('/main')
def main():
	if('email' in session): # 세션 성공
		return render_template('main.html', is_authenticated=True,
				email=session['email'], seq=session['seq'])
	else: # 세션 실패
		return render_template("main.html")

# 뉴스 검색 page
@app.route('/news_search')
def searchNews():
	return render_template("news_search.html")		

# 뉴스 요약 page
@app.route('/news_summary')
def summaryNews():
	return render_template("news_summary.html")		

@app.route('/search', methods=['POST'])
def search():

	keyword = request.form.get("keyword")

	cur = db.cursor()

	cur.execute("SELECT * FROM crawling_news_new WHERE content LIKE '%" + keyword + "%'")
	rows = cur.fetchall()

	for i in rows :
		print(i[0])

	return jsonify({"status": "success", "rows" : rows})

@app.route('/searchSummaryResult', methods=['POST'])
def searchSummaryResult():

	seq = request.form.get("seq")

	cur = db.cursor()

	cur.execute("SELECT * FROM (SELECT * FROM sentence_rank_5 WHERE document_seq = %s ORDER BY count LIMIT 0, 3) AS subQuery ORDER BY sentence_seq" %(seq))
	rows = cur.fetchall()
	for i in rows :
		print(i)

	return jsonify({"status": "success", "rows" : rows})


def summary(content) :

	print(1)
	try :
		tokens_ko = t.morphs(content)
		ko = nltk.Text(tokens_ko, name=content)
		word_counter = ko.vocab()
	except :
		print("error")

	print(2)

	keyword = {}

	for key, value in word_counter.items() :
	    if len(bytes(key, 'utf-8')) > 5 :
	        keyword[key] = value


	# In[50]:

	class TFIDF :
	    keyword = None
	    tf = None
	    idf = None
	    tfIdf = None
	    
	class SentenceRank :
	    sentence_seq = None
	    sentence = None
	    tfidf = None
	    count = None
	    
	def getTotalDocumentCount() :
	    query = "select count(distinct document_seq) from nltk_new_seq"
	    cur.execute(query)

	    result = cur.fetchall()
	    
	    return result[0][0]


	# In[51]:

	def calTF(count, totalCount) :
	    return count/totalCount

	def calIDF(keyword) :
	    return math.log(totalDocumentCount/count[keyword])


	# In[52]:

	totalDocumentCount = getTotalDocumentCount()

	cur.execute('select * from nltk_count')
	result = cur.fetchall()
	count = {}
	for a in result :
	    count[pymysql.escape_string(a[0]).upper()] = a[1]


	# In[53]:

	totalKeywordCount = 0
	tfidfList = []
	for key, value in keyword.items() :
	    totalKeywordCount += value

	for key, value in keyword.items() :
	    tfidf = TFIDF()
	    tfidf.keyword = pymysql.escape_string(key)
	    tfidf.tf = calTF(value, totalKeywordCount)
	    tfidf.idf = calIDF(key)
	    tfidf.tfidf = tfidf.tf * tfidf.idf
	    tfidfList.append(tfidf)


	# In[59]:

	tfidfList.sort(key=operator.attrgetter('tfidf'))
	tfidfList.reverse()


	# In[60]:

	sentences = [(i+'다.').strip() for i in content.split('다.') if i is not '']
	sentenceRankList = []

	count = 0;
	for sentence in sentences :
	    sum_temp = 0
	    count_temp = 0
	    if sentence == '다.':
	        continue        
	    for oneword in tfidfList:
	        count_temp += sentence.count(oneword.keyword)
	        sum_temp += sentence.count(oneword.keyword)*oneword.tfidf
	    sentenceRank = SentenceRank()
	    sentenceRank.sentence_seq = count
	    sentenceRank.sentence = sentence
	    sentenceRank.tfidf = sum_temp
	    sentenceRank.count = count_temp
	    sentenceRankList.append(sentenceRank)
	        
	#     print('%s\t%s\t%s\t%s\n' %(str(count),pymysql.escape_string(sentence),str(sum_temp),str(count_temp)))
	    count += 1


	# In[61]:

	sentenceRankList.sort(key=operator.attrgetter('count'))
	for temp in sentenceRankList :
	    print(str(temp.count) + " " + str(temp.sentence_seq))
	sentenceRankList.reverse()
	sentenceRankList = sentenceRankList[:3]
	sentenceRankList.sort(key=operator.attrgetter('sentence_seq'))


	# In[63]:

	summary = ''
	for temp in sentenceRankList :
	    summary += temp.sentence

	return summary


@app.route('/summaryUserNews', methods=['POST'])
def summaryUserNews() :
	content = request.form.get("content")
	print(content)

	# os.system("news_summary.py %s" %(content))
	# summaryNews = subprocess.check_output('news_summary.py ' + content, shell=False)
	# summaryNews = subprocess.check_output('news_summary.py', shell=False)
	# print(summaryNews)
	summary(content)

	return jsonify({"summaryNews" : summaryNews['summary']})

if __name__ == "__main__": 
	app.run(debug=True)
	# app.run(host="0.0.0.0", port=5000)
