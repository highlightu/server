from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter, OrderedDict
from .repeatReplacer import RepeatReplacer
# from sklearn.preprocessing import normalize
import operator
import re


'''
1. Load chatlog and words for scoring
2. Do preprocessing by reading one line at one time
3. Store the each result of sentences to a dictionary {time - preprocessed words} in a list
4. Review the list that contains a set of dictionary to score them with labeledwords
5. Store the each result of sentences to a dictionary {time - normalized_score} in a list
6. Return the list when it is called to be executed.
'''

# How to Use
'''
    labeldwords = ['a set of lists of words']
    f = open("test.txt", 'rt', encoding='UTF8')
    chatanlyze = ChatAnalyze(f, labeldwords)
    score = chatanlyze.Preprocessing()
    result = chatanlyze.Scoring(score)
    sectined_result = ca.Sectioned_Scoring(result, 5)
    cand = chatanlyze.makeCandidateList(histogram=sectined_result,
                                    numOfMaximumHighlight=10,
                                    delay=1000,
                                    videoLen=19000)
'''


class ChatAnalyze:

    # chatlog <== file = open("test.txt", 'rt', encoding='UTF8')
    # labeledwords <== list
    # table_time = list()
    # table_data = list()
    # Final_Result = dict()

    def __init__(self, chatlog, labeledwords):

        # server setting
        import nltk
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')

        self.chatlog = chatlog
        self.labeledwords = labeledwords
        self.table_time = list()
        self.table_data = list()
        self.Final_Result = dict()
        self.Sectioned_Result = dict()

    def Preprocessing(self):
        # Line by Line seperating
        while True:
            line = self.chatlog.readline().lower()

            if not line:
                break

            timeline, data = line.split(" ", maxsplit=1)
            self.table_time.append(timeline)
            self.table_data.append(data)

        score = [0]*len(self.table_time)

        return score

    def Scoring(self, score):
        ps = PorterStemmer()
        iteration = 0

        # Stopwords and Replacer
        stopWords = set(stopwords.words('english'))
        replacer = RepeatReplacer()

        # Append most common top 10 Term freqency to labeled words
        filtered_sentence = []
        for eachData in self.table_data:

            words = word_tokenize(eachData)
            output = []
            for check in words:
                # repeat word delete
                check = replacer.replace(check)
                check = re.sub(r'[^\w]', '', check)
                output.append(check)

            for w in output:
                if w not in stopWords and not w.isdigit():
                    filtered_sentence.append(w)

        # Delete "" [Exception Handling]
        counts = Counter(filtered_sentence)
        del counts[""]

        # Sort by counts.value ( most freqent words )
        counts = OrderedDict(counts.most_common())
        i = 0

        # Check if the most freqent word is in labelwords
        # if yes, skip and check next one
        # if no, append it
        while iteration < 10:
            if list(counts.keys())[i] not in self.labeledwords:
                self.labeledwords.append(list(counts.keys())[i])
                i += 1
                iteration += 1
            else:
                i += 1
        print("[Label words]")
        print(self.labeledwords, end="\n")

        # Scoring
        for eachData in self.table_data:
            words = word_tokenize(eachData)
            target_score = 0

            for word in words:
                if(ps.stem(word) in self.labeledwords):
                    target_score += 1

            score[self.table_data.index(eachData)] = target_score

        # Result
        result = sorted(Counter(self.table_time).items())
        index = 0

        for eachResult in result:
            # How many times chats appeared in same time
            iteration = eachResult[1]

            sum = 0
            for i in range(iteration):
                sum += score[i+index]

            self.Final_Result[eachResult[0]] = sum
            index += iteration

        return self.Final_Result

    # finalresult = dict(), section = int (how many sector you want in timeline)
    def Sectioned_Scoring(self, finalresult, section):

        result = list()

        # Finalresult (dict) to result (list)
        for key, value in finalresult.items():
            temp = [key, value]
            result.append(temp)

        for eachResult in result:
            sum = 0

            # Check if section is over or not.
            if (result.index(eachResult) + section) <= len(result):
                startindex = result.index(eachResult)
                sumList = result[startindex: startindex + section]

                for eachsumList in sumList:
                    sum += eachsumList[1]

                self.Sectioned_Result[eachResult[0]] = sum
            else:
                return normalizing(self.Sectioned_Result)


def normalizing(Sectioned_Result):
    # Normalization
    max_sum = max(Sectioned_Result.items(),
                  key=operator.itemgetter(1))[1]

    for key, value in Sectioned_Result.items():
        Sectioned_Result[key] = value / max_sum

    return Sectioned_Result

    # How to use this class
if __name__ == '__main__':
    labeldwords = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
                   'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']
    f = open("test.txt", 'rt', encoding='UTF8')
    chatanlyze = ChatAnalyze(f, labeldwords)
    score = chatanlyze.Preprocessing()
    result = chatanlyze.Scoring(score)
    sectined_result = chatanlyze.Sectioned_Scoring(result, 5)

    # print(cand)
