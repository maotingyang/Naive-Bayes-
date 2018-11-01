#coding=utf-8
import sys
sys.path.append('../src')
import testing

testing.load_training_data('../model/model.db','../dict/dict.txt.big')
result = testing.test_sentance('餓扁了')
if result['pos'] > result['neg']:
	print ('positive')
elif result['neg'] > result['pos']:
	print ('negative')
else:
	print ('neutral')
result = testing.test_sentance('天')
if result['pos'] > result['neg']:
	print ('positive')
elif result['neg'] > result['pos']:
	print ('negative')
else:
	print ('neutral')
