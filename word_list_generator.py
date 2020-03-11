import re
from collections import Counter


def generate_word_list(json_dict):
    myWords = ""
    stopWordSet = set()

    for line in open("stopwords_en.txt", "r"):
        stopWordSet.add(line.replace('\n', ''))

    # print(stopWordSet)
    for x in json_dict['articles']:
        if x['title'] != '' and x['title'] is not None:
            myWords += x['title'].lower()
    # myWords = myWords.translate(string.punctuation)
    result = re.split('\W+', myWords)
    c = Counter(result)
    wordListTemp = c.copy()
    for key in c:
        if key.lower() in stopWordSet or key.isdigit():
            wordListTemp.pop(key)

    L = sorted(wordListTemp.items(), key=lambda item: item[1], reverse=True)
    L = L[:30]
    max = L[0][1]
    wordList = []
    for eachSet in L:
        wordList.append({"word":eachSet[0],"size":int(eachSet[1]*50/max)})
    # 操作json
    # print(wordList)
    return wordList
