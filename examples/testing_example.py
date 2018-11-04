#coding=utf-8
import sys
sys.path.append('../src')
import testing

testing.load_training_data('../model/model.db','../dict/dict.txt.big')
result = testing.test_sentance('麵條都是軟的`,真難吃')
if result['pos'] > result['neg']:
	print ('positive')
elif result['neg'] > result['pos']:
	print ('negative')
else:
	print ('neutral')
result = testing.test_sentance('服務生優質的服務，讓我備受愛戴眾所皆知，唯有老爺路卡菲可以這樣對我，感受到如此對待，我願和普羅大眾分享。')
if result['pos'] > result['neg']:
	print ('positive')
elif result['neg'] > result['pos']:
	print ('negative')
else:
	print ('neutral')
