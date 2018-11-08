#coding=utf-8
import sys
sys.path.append('../src')
import testing

testing.load_training_data('../model/ntusd_model.db','../dict/ntusd-full.dic')  # 換字典這裡要改
result = testing.test_sentance('咖啡很難喝')
if result['pos'] > result['neg']:
	print ('您開心我們也開心！期待很快能再見到您！')
elif result['neg'] > result['pos']:
	print ('對不起，似乎讓您有不好的體驗，隨即贈送折價券給您！')
else:
	print ('您的意見我們收到了，感謝您的稱讚和指教，我們會繼續努力，隨即贈送折價券給您！')
result = testing.test_sentance('我今天吃得滿開心')
if result['pos'] > result['neg']:
	print ('您開心我們也開心！期待很快能再見到您！')
elif result['neg'] > result['pos']:
	print ('對不起，似乎讓您有不好的體驗，隨即贈送折價券給您！')
else:
	print ('您的意見我們收到了，感謝您的稱讚和指教，我們會繼續努力，隨即贈送折價券給您！')
