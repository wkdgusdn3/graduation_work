# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pymysql
import os
import re
import sys
import math
import nltk
import codecs
import operator
from konlpy.tag import Twitter; t=Twitter()

# database 연결
def setDB() :
    host = "128.134.54.31"
    port = 7778
    id = "ejj"
    password = "djwkdwh"
    name = "summary_news"

    db = pymysql.connect(host, id, password, name, port, charset="utf8",  local_infile=True)

    return db




# In[47]:
# content = pymysql.escape_string("20대 국회 출범 직후부터 정치권에서 논의된 ‘국회의원 불체포특권’ 포기 방안이 국회의장 차원에서 마련돼 다음 달부터 본격적인 입법 절차가 진행된다. 국회 관계자는 30일 본지 통화에서 “국회의장 직속 자문 기구인 ‘국회의원 특권 내려놓기 추진위원회’에서 체포동의안 표결 절차의 보완 방안을 사실상 확정했다”며 “이번 9월 정기국회에서 이를 반영한 국회법 개정안이 처리될 것”이라고 했다. 국회의원 불체포특권 포기는 그동안 매 국회 때마다 논의됐으나 의원들의 소극적인 태도로 번번이 법제화되지 못했다. 하지만 여야(與野)가 20대 국회 들어 ‘국회의원 특권 내려놓기 차원’에서 불체포특권 포기 추진을 공개적으로 논의해온 만큼 이번에는 국회 통과 가능성이 있는 것으로 정치권은 전망하고 있다. 추진위가 마련한 보완 방안은 체포동의안이 본회의에 보고된 뒤 24시간 이후 72시간 이내에 처리되지 않으면 바로 다음 개의하는 본회의에 자동 상정해서 표결하도록 하는 것이 골자다. 현행 국회법에는 체포동의안이 본회의에 보고되면 24~72시간 이내에 표결하게 돼 있다. 그러나 이 시간 내에 표결하지 않는 경우에 대한 별도 규정이 없어서 시간이 지나면 체포동의안은 관례적으로 폐기돼왔다. 국회의원들은 그동안 이를 악용해 본회의를 연 채 72시간을 버티는 이른바 ‘방탄 국회’를 열어왔다. 이번 개정안을 통해 불체포특권이 완전히 사라지는 것은 아니다. 헌법에 보장된 국회의원의 특권이기 때문에 체포동의안이 표결에서 부결되면 여전히 국회의원의 체포·구금은 불가능하다.")
# content = pymysql.escape_string(str("20대 국회 출범 직후부터 정치권에서 논의된 ‘국회의원 불체포특권’ 포기 방안이 국회의장 차원에서 마련돼 다음 달부터 본격적인 입법 절차가 진행된다. 국회 관계자는 30일 본지 통화에서 “국회의장 직속 자문 기구인 ‘국회의원 특권 내려놓기 추진위원회’에서 체포동의안 표결 절차의 보완 방안을 사실상 확정했다”며 “이번 9월 정기국회에서 이를 반영한 국회법 개정안이 처리될 것”이라고 했다. 국회의원 불체포특권 포기는 그동안 매 국회 때마다 논의됐으나 의원들의 소극적인 태도로 번번이 법제화되지 못했다. 하지만 여야(與野)가 20대 국회 들어 ‘국회의원 특권 내려놓기 차원’에서 불체포특권 포기 추진을 공개적으로 논의해온 만큼 이번에는 국회 통과 가능성이 있는 것으로 정치권은 전망하고 있다. 추진위가 마련한 보완 방안은 체포동의안이 본회의에 보고된 뒤 24시간 이후 72시간 이내에 처리되지 않으면 바로 다음 개의하는 본회의에 자동 상정해서 표결하도록 하는 것이 골자다. 현행 국회법에는 체포동의안이 본회의에 보고되면 24~72시간 이내에 표결하게 돼 있다. 그러나 이 시간 내에 표결하지 않는 경우에 대한 별도 규정이 없어서 시간이 지나면 체포동의안은 관례적으로 폐기돼왔다. 국회의원들은 그동안 이를 악용해 본회의를 연 채 72시간을 버티는 이른바 ‘방탄 국회’를 열어왔다. 이번 개정안을 통해 불체포특권이 완전히 사라지는 것은 아니다. 헌법에 보장된 국회의원의 특권이기 때문에 체포동의안이 표결에서 부결되면 여전히 국회의원의 체포·구금은 불가능하다.", "utf-8"))
# content = unicode(content, "utf-8")

def __init__() :

    db = setDB()
    cur = db.cursor()

    content = sys.args(1)
    # print(content)

    # In[48]:

    try :
        tokens_ko = t.morphs(content)
        ko = nltk.Text(tokens_ko, name=content)
        wordCounter = ko.vocab()
    except :
        print("error")


    # In[49]:

    keyword = {}

    for key, value in wordCounter.items() :
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
    sentenceRankList.reverse()
    sentenceRankList = sentenceRankList[:3]
    sentenceRankList.sort(key=operator.attrgetter('sentence_seq'))


    # In[63]:

    summary = ''
    for temp in sentenceRankList :
        summary += temp.sentence

    # print(summary)
    return summary



