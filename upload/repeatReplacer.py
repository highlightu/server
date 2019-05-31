import re
from nltk.corpus import wordnet

givepatterns = [ (r'won\'t', 'will not'),(r'\'s', ' is'),(r'\d',' would'),(r'don\'t', 'do not')]

class RegexpReplacer(object):
    def __init__(self):
        self.patterns = givepatterns
    
    def replace(self, text):
        for (raw, rep) in self.patterns:
            regex = re.compile(raw)
            text = regex.sub(rep,text)
        return text

class RepeatReplacer(object):

    def __init__(self):
        self.regex = re.compile(r'(\w*)(\w)\2(\w*)')
        self.repl = r'\1\2\3'

    def replace(self,word):
        if wordnet.synsets(word):
            return word
    
        loop_res = self.regex.sub(self.repl, word)
    
        if (word == loop_res):
            return loop_res
        else:
            return self.replace(loop_res)
    