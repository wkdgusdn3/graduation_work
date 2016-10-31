# -*- coding: utf-8 -*-

from flask import *
from os import urandom
import pymysql, os
import sys
import subprocess
import re
import math
import nltk
import codecs
import operator
from konlpy.tag import Twitter

app = Flask(__name__)
app.secret_key = urandom(16)

host = "128.134.54.31"
id = "ejj"
port = 7778
password="djwkdwh"
name="summary_news"

@app.before_request
def before_request():
	g.db = pymysql.connect(host, id, password, name, port, charset="utf8")

@app.teardown_request
def teardown_request(exception):
	g.db.close()

t=Twitter()

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
@app.route('/search')
def search():
	return render_template("search.html")		

# 뉴스 요약 page
@app.route('/summary')
def summary():
	return render_template("summary.html")		

@app.route('/searchNews', methods=['POST'])
def searchNews():

	keyword = request.form.get("keyword")

	cur = g.db.cursor()

	cur.execute("SELECT * FROM crawling_news_new WHERE title LIKE '%" + keyword + "%'")
	rows = cur.fetchall()

	# for i in rows :
	# 	print(i[0])

	return jsonify({"status": "success", "rows" : rows})

@app.route('/searchSummaryResult', methods=['POST'])
def searchSummaryResult():

	seq = request.form.get("seq")

	cur = g.db.cursor()

	cur.execute("SELECT * FROM (SELECT * FROM sentence_rank_5 WHERE document_seq = %s ORDER BY count LIMIT 0, 3) AS subQuery ORDER BY sentence_seq" %(seq))
	rows = cur.fetchall()
	# for i in rows :
	# 	print(i)

	return jsonify({"status": "success", "rows" : rows})


@app.route('/summaryUserNews', methods=['POST'])
def summaryNews() :
	cur = g.db.cursor()
	content = request.form.get("content")
	
	try :
	    tokens_ko = t.morphs(content)
	    ko = nltk.Text(tokens_ko, name=content)
	    word_counter = ko.vocab()
	except :
	    print("error")

	keyword = {}

	for key, value in word_counter.items() :
	    if len(bytes(key, 'utf-8')) > 5 :
	        keyword[key] = value

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

	def calTF(count, totalCount) :
	    return count/totalCount

	def calIDF(keyword) :
	    return math.log(totalDocumentCount/count[keyword])

	totalDocumentCount = getTotalDocumentCount()

	cur.execute('select * from nltk_count')
	result = cur.fetchall()
	count = {}
	for a in result :
	    count[pymysql.escape_string(a[0]).upper()] = a[1]

	totalKeywordCount = 0
	tfidfList = []
	for key, value in keyword.items() :
	    totalKeywordCount += value

	for key, value in keyword.items() :
		try :
		    tfidf = TFIDF()
		    tfidf.keyword = pymysql.escape_string(key)
		    tfidf.tf = calTF(value, totalKeywordCount)
		    tfidf.idf = calIDF(key)
		    tfidf.tfidf = tfidf.tf * tfidf.idf
		    tfidfList.append(tfidf)
		except Exception as e:
			print(str(e))

	tfidfList.sort(key=operator.attrgetter('tfidf'))
	tfidfList.reverse()

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
	        
	    count += 1

	sentenceRankList.sort(key=operator.attrgetter('count'))
	sentenceRankList.reverse()
	sentenceRankList = sentenceRankList[:3]
	sentenceRankList.sort(key=operator.attrgetter('sentence_seq'))

	summary = ''
	for temp in sentenceRankList :
	    summary += temp.sentence + "<br><br>"

	# print(summary)

	return jsonify({"summaryNews" : summary})

if __name__ == "__main__": 
	# app.run(debug=True)
	# app.run()
	app.run(host="0.0.0.0", port=5000)
