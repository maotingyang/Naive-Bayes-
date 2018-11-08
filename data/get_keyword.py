import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

# USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

# parser = OptionParser(USAGE)
# parser.add_option("-k", dest="topK")
# opt, args = parser.parse_args()


# if len(args) < 1:
#     print(USAGE)
#     sys.exit(1)

# file_name = args[0]

# if opt.topK is None:
#     topK = 10
# else:
#     topK = int(opt.topK)
key_word_list = []
content = open('negative.txt', 'rb').readlines()
for line in content:
    tags = jieba.analyse.extract_tags(line)
    for word in tags:
        key_word_list.append(word)

print("結果" + '='*50)
print(key_word_list)
print(len(key_word_list))
# print(",".join(tags))

