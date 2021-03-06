import json
import datetime
import jieba
import jieba.analyse
import sqlite3
import random

# 把文字前後空格、換行去掉
def preprocess(input_str):
	return input_str.strip()

# 建一個sql資料庫，裡面放正負面句子及其數據
def create_table(cnx,cur):
	cur.execute('DROP TABLE IF EXISTS sentiment_positive_word')
	cur.execute('DROP TABLE IF EXISTS sentiment_negative_word')
	cur.execute('DROP TABLE IF EXISTS sentiment_baseline')
	cur.execute('CREATE TABLE sentiment_positive_word (word,value)')
	cur.execute('CREATE TABLE sentiment_negative_word (word,value)')
	cur.execute('CREATE TABLE sentiment_baseline (positive_document_count,negative_document_count,positive_word_count,negative_word_count)')
	cnx.commit()

# 讀出正、負面文件中蒐集來的句子
def read_data_file(file_name):
	with open(file_name, encoding = 'utf8') as thedoc:
		doc_list = thedoc.readlines()
		output = []
		for doc in doc_list:
			output.append(preprocess(doc))
	random.shuffle(output)		
	return output

def training(positive_file_name,negative_file_name,model_path,user_dic_name=''):
	# 更換結巴的主字典
	# jieba.set_dictionary('../dict/dict.txt.big')
	if user_dic_name != '':
		jieba.load_userdict(user_dic_name)
	pos_data_list = []
	cnx = sqlite3.connect(model_path)
	cur = cnx.cursor()
	create_table(cnx,cur)	# 創建三個table(見create_table函式)
	pos_data_list = read_data_file(positive_file_name)  # 從data/positive.txt 讀出正面句子的list
	neg_data_list = read_data_file(negative_file_name)	# 從data/negative.txt 讀出負面句子的list

#positive
	pos_word_count_dic = {}
	pos_word_count = 0
	for data in pos_data_list[:600]:
		word_list = jieba.cut(data ,cut_all=False)  # 第一種：直接用結巴斷詞
		# word_list = jieba.analyse.extract_tags(data, allowPOS=('a', 'ag', 'v', 'vd', 'y'))  # 第二種：用結巴提取關鍵字
		for word in word_list:
			word = word.strip() 	# 移除string頭尾的空格
			if len(word) > 0:
				if word not in pos_word_count_dic:
					pos_word_count_dic[word] = 0
				pos_word_count_dic[word] += 1
				pos_word_count += 1
	for word in pos_word_count_dic.keys():
		sql = "INSERT INTO sentiment_positive_word (word,value) VALUES (?,?)"
		value = float(pos_word_count_dic[word]+1)/pos_word_count
		cur.execute(sql,(word,value))
	with open('../data/positive_test.txt', 'w', encoding='utf8') as positive_test:  # 寫下測試檔案
		for line in pos_data_list[600:]:
			positive_test.write(line + '\n')
#negative
	neg_word_count_dic = {}
	neg_word_count = 0
	for data in neg_data_list[:600]:
		word_list = jieba.cut(data, cut_all=False)  # 第一種：直接用結巴斷詞
		# word_list = jieba.analyse.extract_tags(data, allowPOS=('a', 'ag', 'v', 'vd', 'y'))  # 第二種：用結巴提取關鍵字
		for word in word_list:
			word = word.strip()
			if len(word) > 0:
				if word not in neg_word_count_dic:
					neg_word_count_dic[word] = 0
				neg_word_count_dic[word] += 1
				neg_word_count += 1
	for word in neg_word_count_dic.keys():
		sql = "INSERT INTO sentiment_negative_word (word,value) VALUES (?,?)"
		value = float(neg_word_count_dic[word]+1)/neg_word_count
		cur.execute(sql,(word,value))
	with open('../data/negative_test.txt', 'w', encoding='utf8') as negative_test:  # 寫下測試檔案
		for line in neg_data_list[600:]:
			negative_test.write(line + '\n')

	sql = "INSERT INTO sentiment_baseline (positive_document_count,negative_document_count,positive_word_count,negative_word_count) VALUES (?,?,?,?)"
	cur.execute(sql,(len(pos_data_list),len(neg_data_list),pos_word_count,neg_word_count))
	cnx.commit()
#pass

if __name__ == '__main__':
	# jieba.load_userdict('dict/ntusd-full.dic')
	training('../data/positive.txt','../data/negative.txt',model_path = '../model/model.db', user_dic_name='../dict/dict.txt.big')
	# 自己測試斷詞
	jieba.load_userdict('../dict/dict.txt.big')
	seg_list = jieba.cut("很不爽", cut_all=True)
	print("Full Mode: " + "/ ".join(seg_list))  # 全模式
