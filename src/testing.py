#coding=utf-8
import json
import datetime
import jieba
import jieba.analyse
import math
import sqlite3
from decimal import *

pos_sentiment_dic = {}
neg_sentiment_dic = {}
pos_word_count = 0
neg_word_count = 0
pos_prior = 0
neg_prior = 0

def load_training_data(model_path,user_dic_name=''):
	if user_dic_name != '':
		jieba.load_userdict(user_dic_name)
	global pos_sentiment_dic
	global neg_sentiment_dic
	global pos_word_count
	global neg_word_count
	global pos_prior
	global neg_prior
	cnx = sqlite3.connect(model_path)
	cur = cnx.cursor()
	cur.execute('SELECT word,value FROM sentiment_positive_word')
	results = cur.fetchall()
	for result in results:
		pos_sentiment_dic[result[0]] = result[1]
	cur.execute('SELECT word,value FROM sentiment_negative_word')
	results = cur.fetchall()
	for result in results:
		neg_sentiment_dic[result[0]] = result[1]
	cur.execute('SELECT positive_word_count,negative_word_count,positive_document_count,negative_document_count FROM sentiment_baseline',)
	result = cur.fetchone()
	pos_word_count = int(result[0])
	neg_word_count = int(result[1])
	positive_document_count = float(result[2])
	negative_document_count = float(result[3])
	pos_prior = positive_document_count/(negative_document_count+positive_document_count)
	neg_prior = negative_document_count/(negative_document_count+positive_document_count)

def test_sentance(input_sentence):
	word_list = jieba.cut(input_sentence.strip(), cut_all=True) # 第一種：直接用結巴斷詞 
	# word_list = jieba.analyse.extract_tags(input_sentence)  # 第二種：用結巴提取關鍵字
	#print ','.join(word_list).encode('utf-8')
	pos_result = math.log(pos_prior)
	neg_result = math.log(neg_prior)
	# temp_list = []
	test_list = {}   # 我拿來看內部數據的字典
	for word in word_list:
		word = word.strip()
		if len(word) > 0:
			# temp_list.append(word)
			if word in pos_sentiment_dic:
				# print(word+"有收錄在正面字典，值是", math.log(pos_sentiment_dic[word]))
				pos_result += math.log(pos_sentiment_dic[word])
				test_list[word+"是正面"] = pos_result  #test
			else:
				# print(pos_word_count)
				# print(word+"沒收錄在正面字典", math.log(float(1)/pos_word_count))
				pos_result += math.log(float(1)/pos_word_count)				
				test_list[word+"是正面"] = pos_result  #test
			if word in neg_sentiment_dic:
				# print(word+"有收錄在負面字典,值是", math.log(neg_sentiment_dic[word]))
				neg_result += math.log(neg_sentiment_dic[word])  # 1.8是我平衡正負資料數量差異的權重
				test_list[word+"是負面"] = neg_result  #test
			else:
				# print(word+"沒收錄在負面字典", math.log(float(1)/neg_word_count))				
				neg_result += math.log(float(1)/neg_word_count)
				test_list[word+"是負面"] = neg_result  #test
	#print ','.join(temp_list).encode('utf-8')
	# print("測試" + "="*50)  # 測試
	# for word in test_list:
	# 	print( word, ":", test_list[word] )
	# print("正負" + "="*50)
	# print( 'pos', pos_result , 'neg' , neg_result )
	return {'pos':pos_result,'neg':neg_result }

if __name__ == '__main__':
	# 自己測試斷詞
	load_training_data('../model/model.db', user_dic_name='../dict/dict.txt.big')
	with open('../data/positive_test.txt', encoding='utf8') as posi:
		positive_list = posi.readlines()
		posi_all = len(positive_list)
		posi_true = 0
		posi_false = 0
		for line in positive_list:
			pos_dict = test_sentance(line)
			if pos_dict.get('pos') - pos_dict.get('neg') > 0:
				posi_true += 1
			else:
				posi_false += 1
		print("正面句子預測成功率：{:2f}，失敗率{:2f}".format(posi_true/posi_all*100,posi_false/posi_all*100 ))
	
	with open('../data/negative_test.txt', encoding='utf8') as nega:
		negative_list = nega.readlines()
		nega_all = len(negative_list)
		nega_true = 0
		nega_false = 0
		for line in negative_list:
			neg_dict = test_sentance(line)
			if neg_dict.get('pos') - neg_dict.get('neg') > 0:
				nega_false += 1
			else:
				nega_true += 1
		print("負面句子預測成功率：{:2f}，失敗率{:2f}".format(nega_true/nega_all*100,nega_false/nega_all*100 ))				