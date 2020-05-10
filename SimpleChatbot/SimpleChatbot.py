# String Matching with Boyer Moore
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


class SimpleChatbot:

    answere=''

    def lastOccur(self, pattern):
        last = [-1]*128
        for i in range(len(pattern)):
            last[ord(pattern[i])] = i
        return last

    def bm(self, text, pattern):
        last = self.lastOccur(pattern)
        n = len(text)
        m = len(pattern)
        i = 0
        while(i<=n-m) :
            j = m-1
            while(j>=0 and pattern[j] == text[i+j]):
                j = j-1
            if j<0:
                return i
            else :
                i = i+ max(1, j-last[ord(text[i+j])])
        return -1

    def bm2(self, text, pattern):
        n = len(text)
        checker = -1
        txt = text
        pat = pattern.split(" ")
        counter = 0
        percentage = 0
        for p in pat:
            checker = self.bm(txt,p)
            if(checker != -1):
                counter += 1
                percentage = percentage + len(p) +1
                if(len(txt)> checker):
                    txt = txt[checker + 1::]
        return percentage*100/n

    def dataFromFile(self, file_location):
        file = open(file_location, 'r')
        data = []
        for lines in file :
            line = lines.replace('\n', '').split(" || ")
            data.append([line[0],line[1]])
        return data

    def __init__(self, input,file_location):
        data=self.dataFromFile(file_location)
        stopword = StopWordRemoverFactory().create_stop_word_remover()
        stemmer = StemmerFactory().create_stemmer()
        input=stopword.remove(input.lower())
        input=stemmer.stem(input)
        valid = 0
        for i in range(len(data)):
            kal = stopword.remove(data[i][0].lower())
            kal = stemmer.stem(kal)
            if (self.bm(input.lower(), kal.lower()) != -1):
                if (valid == 0):
                    percent  = len(input)*100/len(kal)
                    # print("Confidence1 : " + str(percent))
                    if (percent > 80):
                        self.answere = data[i][1]
                    valid = 1
            else:
                if valid == 0:
                    if(self.bm2(input.lower(),kal.lower()) >= 80):
                        # print("Confidence2 : " + str(bm2(input.lower(), kal.lower())))
                        self.answere = data[i][1]
                        valid = 1
    def getAnswere(self):
        if(self.answere == ""):
            return 'saya tidak mengerti maksud anda'
        else:
            return self.answere
