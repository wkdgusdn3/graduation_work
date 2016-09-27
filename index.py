# -*- coding: utf-8 -*-

from flask import Flask, url_for, render_template, request, session, jsonify, redirect
from os import urandom
import pymysql, os

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

if __name__ == "__main__": 
	app.run(debug=True)
	# app.run(host="0.0.0.0", port=5000)
