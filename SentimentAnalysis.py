import re

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
class formatCodes:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    DARKBLUE = '\033[34m'
    PURPLE = '\033[35m'
    
    LTGRAY = '\033[37m'
    GRAY = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class SentimentAnalysis:
    vaderSentiment = None
    text = None
    def __init__(self):
        self.vaderSentiment = SentimentIntensityAnalyzer()
    
    def polarity(self, text):
        return TextBlob(text).sentiment.polarity
    
    def subjectivity(self, text):
        return TextBlob(text).sentiment.subjectivity
    
    def vader(self, text):
        return self.vaderSentiment.polarity_scores(text)
    
    def print(self, text):
        print(formatCodes.CYAN+
            formatCodes.BOLD +
            "Sentiment anlysis (print):"+ 
            formatCodes.ENDC)

        print(formatCodes.BOLD+
            formatCodes.LTGRAY+
            " text: "+
            formatCodes.ENDC,
            formatCodes.GRAY+
            text+
            formatCodes.ENDC)

        print(formatCodes.BOLD+
            formatCodes.LTGRAY+
            " Sentiment Analysis"+
            formatCodes.ENDC)
        print(formatCodes.BOLD+
            "  TextBlob:"+
            formatCodes.ENDC)

        print(formatCodes.BLUE+
            "   polarity:     "+
            formatCodes.ENDC, 
            analysis.polarity(text))

        print(formatCodes.DARKCYAN+
            "   subjectivity: "+
            formatCodes.ENDC, 
            analysis.subjectivity(text))

        print(formatCodes.BOLD+
            "  VADER:"+
            formatCodes.ENDC)

        print(formatCodes.GREEN+
            "   positive:     "+
            formatCodes.ENDC, 
            analysis.vader(text)['pos'])

        print(formatCodes.YELLOW+
            "   neutral:      "+
            formatCodes.ENDC, 
            analysis.vader(text)['neu'])

        print(formatCodes.RED+
            "   negative:     "+
            formatCodes.ENDC, 
            analysis.vader(text)['neg'])

        print(formatCodes.PURPLE+
            "   compound:     "+
            formatCodes.ENDC, 
            analysis.vader(text)['compound'])

class Text:
    file = None
    titles = ["Mrs", "Mr", "Dr"] # these are the only ones that I found.
    endPunctuation = ["! ", "? ", "; ", ": "] # . (period) is special because of titles
    punctuation = [", ", "(", ")", "[", "]", "{", "}", "<", "--"] #if you want to do seomthing with this, you're choice ig
    backlog = ""
    def __init__(self, file):
        self.file = file
    #These are slightly broken, so... TODO: fix them
    def nextParagraph(self, n = 1):
        num = n
        str = ""

        sentence = self.nextSentence()
        str += sentence.replace("\n", "")
        while(num>0):

            sentence = self.nextSentence()
            if("\n" in sentence):
                self.backlog = sentence.replace("\n", "")
                break
            str += sentence

        return str
    
    def nextSentence(self, n = 1):
        num = n
        str = ""
        if(self.backlog != ""):
            str += self.backlog
            num-=1
            self.backlog = ""
        while(num>0):
            word = self.nextWord()
            for char in self.endPunctuation:
                if char in word:
                    num-=1
            if "." in word and not(word.replace(". ", "") in self.titles):
                num-=1
            str += word
        return str
    
    def nextWord(self, n = 1):
        num = n
        str = ""
        char = " "
        while(("\n" in char or " " in char)):
            char = self.file.read(1)
        str+=char
        while(num>0):
            char = self.file.read(1)
            # break if the character is a punctionation
            str += char
            for char in self.punctuation:
                if(char in str):
                    num-=1
                    break
            for char in self.endPunctuation:
                if(char in str):
                    num-=1
                    break
            if (". " in str and not(str in self.titles)):
                num-=1
            if(" " in str):
                num-=1
        return str
    
    def nextChar(self):
        return self.file.read(1)

# — is 2 word, - is 1 word

# I'm debating on whether or not I want to remove the hr and p tags
class HTML:
    file = None
    titles = ["Mrs.", "Mr.", "Dr."] # these are the only ones that I found.
    endSentence = ["!", "?",  ">"] # . (period) is special because of titles
    endWord = ["—", " "] #if you want to do seomthing with this, you're choice ig
    backlog = ""
    def __init__(self, file):
        self.file = file
    
    def endOfParagraph(self):
        str = self.__endOfParagraph()
        # elimiate excess whitespace (newlines, tabs, multiple spaces)
        str = str.replace("\n", " ")
        str = str.replace("\t", " ")
        str = str.replace("<p>", "")
        str = str.replace("</p>", "")
        str = re.sub(r'[ ]+', ' ', str)
        return str
    
    def __endOfParagraph(self):
        str=""
        while(True):
            str+=self.nextChar()
            if("</p>" in str):
                break
        return str
    
    def nextParagraph(self):
        str = self.__nextParagraph()
        # elimiate excess whitespace (newlines, tabs, multiple spaces)
        str = str.replace("\n", " ")
        str = str.replace("\t", " ")
        str = str.replace("<p>", "")
        str = str.replace("</p>", "")
        str = re.sub(r'[ ]+', ' ', str)
        return str
    
    def __nextParagraph(self):
        str = ""

        while(True):
            tag = self.nextTag()
            if("<p>" in tag):
                str += tag
                break
            elif("<hr>" in tag):
                return "<p></p>"
        while(True):
            str+=self.nextChar()
            if("</p>" in str):
                break
        return str
    
    def nextSentence(self):
        str = ""
        while(str == "" or str == " "):
            str = self.__nextSentence().strip()
            print(str)
            # elimiate excess whitespace (newlines, tabs, multiple spaces)
            str = str.replace("\n", " ")
            str = str.replace("\t", " ")
            str = str.replace("p>", "")
            str = str.replace("/", "")
            str = str.replace("<", "")
            str = re.sub(r'[ ]+', ' ', str)
        return str
    
    def __nextSentence(self):
        str = ""
        char= ""
        while(True):
            char=self.nextChar()
            str+=char
            if char == ".":
                for title in self.titles:
                    if title == str[len(str)-len(title):]:
                        break
                else:
                    break
            if str == "<p>" or str == "</p>":
                print("rs",str)
                str = ""
            elif char in self.endSentence:
                break
        if char != ">":
            str+=self.nextChar()

        return str
    
    def nextTag(self):
        str = ""
        char = ""
        while(True):
            char = self.file.read(1)
            if(char == "<"):
                str+=char
                break
        while(True):
            char = self.file.read(1)
            str+=char
            if(char == ">"):
                break
        return str

    def nextChar(self):
        return self.file.read(1)


text = Text(open(r"DallowayJustText.txt", "r"))   
analysis = SentimentAnalysis()    

html = HTML(open(r"Dalloway.html", "r"))
xAxis = []
VaderCompoundY = []
wordCountY = []
for i in range(10000):
    sentence = html.nextSentence()
    analysis.print(sentence)
    print(formatCodes.BOLD+formatCodes.GRAY+
        "\n------------------------------------------------\n"+
        formatCodes.ENDC)
    xAxis.append(i)
    VaderCompoundY.append(analysis.vader(sentence)['compound']+1)
    wordCountY.append(len(sentence.split(" ")))
    if("For there she was" in sentence):
        break
# print("end")
# x axis values

# labels for bars

# plotting a bar chart
plt.bar(xAxis, VaderCompoundY,
        width = 1)

# naming the x-axis
plt.xlabel('sentence in the book')
# naming the y-axis
plt.ylabel('text blob judged polarity from 0 to 2')
# plot title
plt.title('Vader Compound Through out the first '+str(len(xAxis))+' sentences')
# set upper and lower bounds
plt.ylim(0, 2)
plt.xlim(0, len(xAxis))
# function to show the plot
plt.show()

plt.bar(xAxis, wordCountY,
        width = 1)

# naming the x-axis
plt.xlabel('sentence in the book')
# naming the y-axis
plt.ylabel('sentence length')
# plot title
plt.title('text length Through out the first '+str(len(xAxis))+' sentences')
# set upper and lower bounds
# plt.ylim(0, 2)
plt.xlim(0, len(xAxis))
# function to show the plot
plt.show()
