import json

mood_dict = {}

with open('negative.txt') as negative_text:
    for line in negative_text:
        mood_dict[ line ] = -1

with open('positive.txt') as positive_text:
    for line in positive_text:
        mood_dict       