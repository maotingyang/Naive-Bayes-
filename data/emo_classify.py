#!/usr/bin/env python
# coding: utf-8

# # 中文檢索系統

# 1. TFIDF
# $$TFIDF_{td} = TF_{td} \times log(\frac{N}{DF_t})$$
#     - 所謂TFIDF應分成兩個部分來理解：TF(Term Frequency)以及IDF(Inverted Document Frequency)。
#     - TF(Term Frequency): $TF_{td}$指得是在特定的文章d中特定的字t出現了幾次。這個部分同時，也表示了一個文字在一篇文章的重要性，依但出現越多次，這個字也就越能代表這篇文章。
#     - IDF(Inverted Document Frequency): N指得是總共有機篇文章，$DF_t$中的DF是Document Frequency的意思，DFt則是詞彙t在幾篇文章中出現過。$\frac{DF_t}{N}$也就是所有文章當中，詞彙t在幾篇文章出現過，而其倒數則是Inverted Documnet Index，表著這個詞彙如果在很多文章裏面都出現過，則其重要性會受到懲罰，而取log則只是讓他在分數的影響上比較平滑而已。
#     
#     
# 2. Cosine Similarity
# $$\cos{\theta} = \frac{A \cdot B}{\| {A} \|_2 \| {B} \|_2}$$
#     - if $A = [1,2,0,4]$ and $B = [3,2,1,0]$
#     - $\cos{\theta} = \frac{1 \cdot 3 + 2 \cdot 2 + 0 \cdot 1 + 4 \cdot 0} {\sqrt{1^2+2^2+0^2+4^2} \cdot \sqrt{3^2+2^2+1^2+0^2}}$

# In[15]:
import jieba
import sys
import random
sys.path.append('../dict')

jieba.set_dictionary('../dict/dict.txt.big')  # 如果是使用繁體文字，請記得去下載繁體字典來使用
import numpy as np
import pandas as pd
from collections import Counter
with open('../dict/stops.txt', 'r', encoding='utf8') as f:  # 中文的停用字，我也忘記從哪裡拿到的，效果還可以，繁體字的資源真的比較少，大家將就一下吧
    stops = f.read().split('\n')

# 把情緒資料讀出來，做成dataframe
emo_dict = {'emo':[], 'text':[]}

# 加入正面句
with open('positive.txt', encoding='utf8') as data:
    pos_train_list = data.readlines()
    random.shuffle(pos_train_list)
    for line in pos_train_list[:600]:
        line = line.strip()
        emo_dict['emo'].append(1)
        emo_dict['text'].append(line)
    with open('pos_2_test.txt', 'w', encoding='utf8') as data:
        for line in pos_train_list[600:]:
    	    data.write(line + '\n')
# 加入負面句  
with open('negative.txt', encoding='utf8') as data:
    neg_train_list = data.readlines()
    random.shuffle(neg_train_list)
    for line in neg_train_list[:600]:
        line = line.strip()
        emo_dict['emo'].append(-1)
        emo_dict['text'].append(line)
    with open('neg_2_test.txt', 'w', encoding='utf8') as data:
        for line in neg_train_list[600:]:
    	    data.write(line + '\n')    
df_emo = pd.DataFrame(emo_dict)

#前處理
all_terms = []
def preprocess(item):  ##定義前處理的function
    # 請把將每一行用jieba.cut進行分詞(記得將cut_all設定為True)
    # 同時建立所有詞彙的list(all_terms)
    #=============your works starts===============#
    terms = [t for t in jieba.cut(item, cut_all=True)]  ## 把全切分模式打開，可以比對的詞彙比較多
    all_terms.extend(terms)  ## 收集所有出現過的字
    #==============your works ends================#
    return terms

df_emo['processed'] = df_emo.text.apply(preprocess)

# df_question['processed'] = df_question['question'].apply(preprocess)
# print(df_question.iloc[0])
# # question                                      小孩出生後應於何時申請育兒津貼?
# # ans          1.幼兒家長在戶政事務所完成新生兒出生登記後，即可向所轄區公所社政課提出育兒津貼申請。2.在...
# # processed                  [小孩, 出生, 後, 應於, 何時, 申請, 育兒, 津貼, , ]
# # Name: 0, dtype: object

# df_question.head()


# 建立termindex: 將all_terms取出不重複的詞彙，並轉換型別為list(避免順序亂掉)
#=============your works starts===============#
termindex = list(set(all_terms))
#==============your works ends================#


# 建立IDF vector
Doc_Length = df_emo.shape[0]  ## 計算出共有幾篇文章
Idf_vector = []  ## 初始化IDF向量
for term in termindex:  ## 對index中的詞彙跑回圈
    num_of_doc_contains_term = 0  ## 計算有幾篇文章出現過這個詞彙
    for terms in df_emo['processed']:
        if term in terms:
            num_of_doc_contains_term += 1
    idf = np.log(Doc_Length/num_of_doc_contains_term)  ## 計算該詞彙的IDF值
    Idf_vector.append(idf)

# 建立document vector
def terms_to_vector(terms):  ## 定義把terms轉換成向量的function
    ## 建立一條與termsindex等長、但值全部為零的向量(hint:dtype=np.float32)
    # 還記得嗎？termindex為不重複的所有詞集合
    #=============your works starts===============#
    vector = np.zeros_like(termindex, dtype=np.float32)  
    #==============your works ends================#
    
    for term, count in Counter(terms).items():
        # 計算vector上每一個字的tf值
        #=============your works starts===============#
        try:
            vector[termindex.index(term)] = count
        except: 
            pass
        #==============your works ends================#

    # 計算tfidf，element-wise的將vector與Idf_vector相乘
    ## hint: 如果兩個vector的型別都是np.array，把兩條vector相乘，就會自動把向量中的每一個元素成在一起，建立出一條新的向量
    #=============your works starts===============#
    vector = vector * Idf_vector
    #==============your works ends================#
    return vector



df_emo['vector'] = df_emo['processed'].apply(terms_to_vector)  ## 將上面定義的function，套用在每一筆資料的terms欄位上
# df_emo['vector'][:10]
# 0    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 1    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 2    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 3    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 4    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 5    [0.09420893837494694, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 6    [0.28262681512484084, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 7    [0.28262681512484084, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 8    [0.28262681512484084, 0.0, 0.0, 0.0, 0.0, 0.0,...
# 9    [0.28262681512484084, 0.0, 0.0, 0.0, 0.0, 0.0,...
# Name: vector, dtype: object


# In[17]:


from numpy.linalg import norm

def cosine_similarity(vector1, vector2):  ## 定義cosine相似度的計算公式
    # 使用np.dot與norm計算cosine score
    #=============your works starts===============#
    score = np.dot(vector1, vector2)  / (norm(vector1) * norm(vector2))
    #==============your works ends================#
    return score

# sentence1 = df_emo.loc[0]  ##取出第零個的問題
# sentence2 = df_emo.loc[2]  ##取出第二個的問題
# print(sentence1['text'])
# print(sentence2['text'])
# print(cosine_similarity(sentence1['vector'], sentence2['vector']))  ##計算兩者的相似度
# 0.203227847937731


# In[19]:


def retrieve(testing_sentence, return_num=3):  ## 定義出檢索引擎
    # 請使用前面定義的terms_to_vector與preprocess兩個function，計算出testing_sentence的向量
    # 計算其與資料庫每一的問句的相似度
    # 依分數進行排序，找到分數最高的三個句子
    #=============your works starts===============#
    testing_vector = terms_to_vector(preprocess(testing_sentence))  ## 把剛剛的前處理、轉換成向量的function，應用在使用者輸入的問題上
    idx_score_mapping = [(idx, cosine_similarity(testing_vector, vec)) for idx, vec in enumerate(df_emo['vector'])]
    top3_idxs = np.array(sorted(idx_score_mapping, key=lambda x:x[1], reverse=True))[:1, 0]
    #==============your works ends================#
    # print(top3_idxs)
    return df_emo.loc[top3_idxs, ['emo', 'text']]

# 自我測試
with open('pos_2_test.txt', encoding='utf8') as data:
    pos_data = data.readlines()
    pos_all = len(pos_data)
    pos_valid = 0
    pos_false = 0
    for line in pos_data:
        if retrieve(line)['emo'].values[0] == 1:
            pos_valid += 1
        else:
            pos_false += 1
    print("正向句正確率：{:.2f}%，正向句錯誤率：{:.2f}%".format(pos_valid/pos_all*100,pos_false/pos_all*100))         

with open('neg_2_test.txt', encoding='utf8') as data:
    neg_data = data.readlines()
    neg_all = len(neg_data)
    neg_valid = 0
    neg_false = 0
    for line in neg_data:
        if retrieve(line)['emo'].values[0] == -1:
            neg_valid += 1
        else:
            neg_false += 1                
    print("負向句正確率：{:.2f}%，負向句錯誤率：{:.2f}%".format(neg_valid/neg_all*100,neg_false/neg_all*100))
    for line in neg_data[:20]:
        print(retrieve(line)[['emo','text']]) 

# Float64Index([100.0, 111.0, 321.0], dtype='float64')


# # # Use Scikit learn

# # In[27]:


# from sklearn.feature_extraction.text import TfidfVectorizer


# # In[28]:


# tfidf = TfidfVectorizer()
# # 使用tfidf.fit_transform將轉換df_question['processed']為vector
# #=============your works starts===============#
# df_question['sklearn_vector'] = list(tfidf.fit_transform(df_question['processed'].apply(lambda x:" ".join(x)).values).toarray())
# #==============your works ends================#

# print(df_question.loc[:10, 'sklearn_vector'].apply(sum).values)
# # [2.54619627 2.54619627 1.95695906 3.12409736 2.19106254 2.74144953
# #  3.82923767 2.54569516 3.4163518  2.98088982 2.35528293]


# # In[29]:


# def sklearn_retrieve(testing_sentence, return_num=3):  ## 定義出檢索引擎
#     # 請使用前面定義的tfidf.transform與preprocess兩個function，計算出testing_sentence的向量
#     # 注意tfidf.transform必須是兩個維度的array
#     # 且out為sparse metric，必需.toarray()轉換為一般np.array()
#     # 計算其與資料庫每一的問句的相似度
#     # 依分數進行排序，找到分數最高的三個句子
#     #=============your works starts===============#
#     testing_vector = tfidf.transform([" ".join(preprocess(testing_sentence))]).toarray()[0]
#     idx_score_mapping = [(idx, cosine_similarity(testing_vector, vec)) for idx, vec in enumerate(df_question['sklearn_vector'])]
#     top3_idxs = np.array(sorted(idx_score_mapping, key=lambda x:x[1], reverse=True))[:3, 0]
#     #==============your works ends================#
#     return df_question.loc[top3_idxs, ['question', 'ans']]

# print(retrieve("老人年金")['question'])
# print(sklearn_retrieve("老人年金")['question'])
# # 100.0    我已經年滿65歲領有國民年金老人年金及基本保證年金3628元，因家境清寒還可以再申請中低收入...
# # 111.0                            新竹市老人一般可領老人津貼6628元，該如何申請？
# # 321.0           國民年金保險被保險人如果是家庭收入較低者，國民年金保險費是否可以減免？補助標準為何？
# # Name: question, dtype: object
# # 100.0    我已經年滿65歲領有國民年金老人年金及基本保證年金3628元，因家境清寒還可以再申請中低收入...
# # 111.0                            新竹市老人一般可領老人津貼6628元，該如何申請？
# # 321.0           國民年金保險被保險人如果是家庭收入較低者，國民年金保險費是否可以減免？補助標準為何？
# # Name: question, dtype: object


# # In[30]:


# print(retrieve("托育")['question'])
# print(sklearn_retrieve("托育")['question'])


# # In[31]:


# print(retrieve("補助")['question'])
# print(sklearn_retrieve("補助")['question'])


# # In[32]:


# print(retrieve("救助")['question'])
# print(sklearn_retrieve("救助")['question'])

