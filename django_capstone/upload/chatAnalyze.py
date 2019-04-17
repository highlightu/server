from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


'''
1. Load chatlog and words for scoring
2. Do preprocessing by reading one line at one time
3. Store the each result of sentences to a dictionary {time - preprocessed words} in a list
4. Review the list that contains a set of dictionary to score them with labeledwords
5. Store the each result of sentences to a dictionary {time - normalized_score} in a list
6. Return the list when it is called to be executed.
'''


class ChatAnalyze:

    def __init__(self, chatlog, labeledwords):
        self.chatlog = chatlog
        self.labeledwords = labeledwords

    def Preprocessing(self):
        # Lower

        # Stopwords

        # Cleaning

        # Stemming
        ps = PorterStemmer()

    def Scoring(self):

        # Scoring

        # Normalization
        pass

    def Execute(self):

        # Return the list
        pass
