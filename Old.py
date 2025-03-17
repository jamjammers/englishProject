import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os
os.system('clear')
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
        
        # print(formatCodes.BOLD+
        #     formatCodes.LTGRAY+
        #     " length: "+
        #     formatCodes.ENDC,
        #     formatCodes.GRAY+
        #     text+
        #     formatCodes.ENDC)

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
    
    def getPrint(self, text):
        out = ""
        out+="Sentiment anlysis (print):"+"\n"

        out+=" text: "+text+"\n"

        out+=" Sentiment Analysis"+"\n"
        out+="  TextBlob:"

        out+="   polarity:     "+holdstr(analysis.polarity(text))+"\n"

        out+="   subjectivity: "+holdstr(analysis.subjectivity(text))+"\n"

        out+="  VADER:"+"\n"

        out+="   positive:     "+holdstr(analysis.vader(text)['pos'])+"\n"

        out+="   neutral:      "+holdstr(analysis.vader(text)['neu'])+"\n"

        out+="   negative:     "+holdstr(analysis.vader(text)['neg'])+"\n"

        out+="   compound:     "+holdstr(analysis.vader(text)['compound'])+"\n"
        return out

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

#THINGS THAT ARE HELPFUL
def replaceTags(text):
        str = ""
        char = ""
        index = 0
        while(index<len(text)):
            while(index<len(text)):
                char = text[index]
                index+=1
                if(char == "<"):
                    break
                str+=char
            while(index<len(text)):
                char = text[index]
                index+=1
                if(char == ">"):
                    break
        return str

def cleanWord(str):
    cleaned = replaceTags(str)
    cleaned = re.sub(r'[^QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm-]', '', cleaned)

    return cleaned

def terminalFormat(text):
    str = ""
    diff = 0
    prev = 0
    index=0
    diff=0
    width=os.get_terminal_size().columns
    while (" " in text[index:]):
        prev = index
        index = text.find(" ", index+1)
        if(index > width+diff):
            str += text[diff:prev] + "\n"
            index = prev
            diff = index+1
    str += text[diff:]
        
    return str

# I'm debating on whether or not I want to remove the hr and p tags   i will not
class HTML:
    file = None
    titles = ["Mrs.", "Mr.", "Dr."] # these are the only ones that I found.
    endSentence = ["!", "?",  ">"] # . (period) is special because of titles
    endWord = ["—", " "] #if you want to do seomthing with this, you're choice ig
    backlog = ""
    def __init__(self, file):
        self.file = file

    def nextBreak(self):
        str = self.__nextBreak()
        # elimiate excess whitespace (newlines, tabs, multiple spaces)
        str = str.replace("\n\n", "¡£çß¥∫ˆ¨∫ß∂˙ß∫ß∫ß∆ß∫ß˙∆∫ß∫ß") #temporarily store paragraph changes
        str = str.replace("\n", " ")
        str = str.replace("¡£çß¥∫ˆ¨∫ß∂˙ß∫ß∫ß∆ß∫ß˙∆∫ß∫ß", "\n\n")
        str = str.replace("\t", " ")
        str = replaceTags(str)
        str = re.sub(r'[ ]+', ' ', str)
        return str

    def __nextBreak(self):
        str = ""
        while(True):
            str+=self.nextChar()
            if("<hr" in str or "<p></p>" in str):
                break
        return str

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
        while(str == "" or str ==" "):
            str = self.__nextSentence().strip()
            str = replaceTags(str)
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
                str = ""
            elif char in self.endSentence:
                break
        if char != ">":
            str+=self.nextChar()

        return str

    def nextWord(self):
        str = ""
        char = ""
        while(True):
            char = self.nextChar()
            if(char == " " or char == "\n" or char == "—"):
                if(re.sub("[]",str)==""):
                    str = ""
                else:
                    break
            str+=char
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

##configuring values (use these to turn of certain outputs)
printSentences = False
printParagraphs = False
printWords = False
plotSentences = False
plotParagraphs = False

printMax =False
plotDia = True

# text = Text(open(r"DallowayJustText.txt", "r"))   
analysis = SentimentAnalysis()    
sentenceHTML = HTML(open(r"Dalloway.html", "r"))
paragraphHTML = HTML(open(r"Dalloway.html", "r"))
wordHTML = HTML(open(r"Dalloway.html", "r"))

breakHTML = HTML(open(r"Dalloway.html", "r"))

sentenceX = []
sentenceVaderCompound = []
sentenceWordCount = []

outputFile = open(r"output.txt", "w")

highSent = 0
lowSent = 0
#for each sentence
for i in range(10000):
    sentence = sentenceHTML.nextSentence()
    
    if(printSentences):
        analysis.print(sentence)
        print(formatCodes.BOLD+formatCodes.GRAY+
            "\n"+"-"*os.get_terminal_size().columns+"\n"+
            formatCodes.ENDC)
    if((analysis.vader(sentence)['compound'])>0):
        highSent+=1
    elif((analysis.vader(sentence)['compound'])<0):
        lowSent+=1
    if(abs(analysis.vader(sentence)['compound'])>=0.75 and printMax):
        print(sentence,"\nSentiment Analysis:", analysis.vader(sentence)['compound'])
        print(formatCodes.BOLD+formatCodes.GRAY+
            "\n"+"-"*os.get_terminal_size().columns+"\n"+
            formatCodes.ENDC)
        # outputFile.write(analysis.getPrint(sentence))
    sentenceX.append(i)
    sentenceVaderCompound.append(analysis.vader(sentence)['compound']+1)
    sentenceWordCount.append(len(sentence.split(" ")))
    # if(i<2):
        # outputFile.write(analysis.getPrint(sentence))
    if("For there she was" in sentence):
        break
print("total: ", i, "\nPositive sentiment: ", highSent, "\nNegative sentiment: ",lowSent)
paragraphX = []
paragraphVaderCompound = []
paragraphWordCount = []

#TODO: paragraph sentence count (split by punctuation but not if title [subtract for each title?])
# for each para
for i in range(10000):
    paragraph = paragraphHTML.nextSentence()
    
    if(printParagraphs):
        analysis.print(paragraph)
        print(formatCodes.BOLD+formatCodes.GRAY+
            "\n"+"-"*os.get_terminal_size().columns+"\n"+
            formatCodes.ENDC)
    
    paragraphX.append(i)
    paragraphVaderCompound.append(analysis.vader(paragraph)['compound']+1)
    paragraphWordCount.append(len(paragraph.split(" ")))
    if("For there she was" in paragraph):
        break

##for each word\
dictionary = {

}
# for i in range(100000000):
#     word = wordHTML.nextWord()
#     cleaned = cleanWord(word)
#     if(printWords):
#         print("word: ", word, "cleaned: ", cleaned)
#         print(formatCodes.BOLD+formatCodes.GRAY+
#             "\n"+"-"*os.get_terminal_size().columns+"\n"+
#             formatCodes.ENDC)
#     print("hi")


####NO CLENLINESS AFTER THIS POINT, I'M NOT SORRY


### output quotes
file = open(r"DallowayJustText.txt", "r")
text = file.read()
start = False
current = "" 
total = []

outputFile = open(r"output.txt", "w")

dialoges = []
diaX = []
diaVaderCompound = []
i=0

numHigh = 0
numLow = 0
bigHigh, bigLow = 0,0
# quotes things
for char in text:
    if(start):
        if(char == "”"):
            current += char
            holdstr = current.replace("\n", " ")
            holdstr = holdstr.replace("\t", " ")
            holdstr = holdstr.replace("<p>", "")
            holdstr = holdstr.replace("</p>", "")
            holdstr = re.sub(r'[ ]+', ' ', holdstr)
            total.append(holdstr)
            i+=1
            if(analysis.vader(holdstr)['compound']>0):
                numHigh+=1
                if(analysis.vader(holdstr)['compound']>=0.75):
                    bigHigh+=1
            elif(analysis.vader(holdstr)['compound']<0):
                numLow+=1
                if(analysis.vader(holdstr)['compound']<=-0.75):
                    bigLow+=1
            diaX.append(i)
            dialoges.append(holdstr)
            diaVaderCompound.append(analysis.vader(holdstr)['compound'])
            start = False
        else:
            current += char
    elif(char == "“"):
        start = True
        current = char
for dia in dialoges:
    withQuotes = analysis.vader(dia)['compound']
    withoutQuotes = analysis.vader(dia.replace("“", "").replace("”", ""))['compound']
    # outputFile.write("artificial increase: "+str(withQuotes-withoutQuotes)+"\n\n")
outputFile.write("\n\n".join(total))
file.close()
print("numHigh: ", numHigh, "\nnumLow: ", numLow, "\ntotal: ", i)
print("bigHigh: ", bigHigh, "\nbigLow: ", bigLow)
if(plotDia):
    ### paragraph

    ## VADER PLOT
    plt.scatter(diaX, diaVaderCompound)

    plt.title('Vader Compound (Dialogue)')
    plt.xlabel('Dialogue')
    plt.ylabel('Vader polarity from -1 to 1')

    plt.ylim(-1, 1)
    plt.xlim(0, len(diaX))

    plt.show()
###take a sentence
seeSentence = False
if seeSentence:
    sentence = input("Enter Sentence:")
    analysis.print(sentence)

####PLOTS

### sentence
if(plotSentences):


    ## text length plot
    plt.bar(sentenceX, sentenceWordCount,width = 1, color = "black")

    plt.title('Word Count (Sentences)')
    plt.xlabel('Sentence')
    plt.ylabel('Word Count')

    plt.xlim(0, len(sentenceX))

    plt.show()

if(plotParagraphs):
    ### paragraph

    ## VADER PLOT
    plt.bar(paragraphX, paragraphVaderCompound, width= 1, color = "black")

    plt.title('Vader Compound (Paragraphs)')
    plt.xlabel('Paragraph')
    plt.ylabel('Vader polarity from 0 to 2')

    plt.ylim(0, 2)
    plt.xlim(0, len(paragraphX))

    plt.show()


    ## text length plot
    plt.bar(paragraphX, paragraphWordCount,width = 1, color="black")

    plt.title('Word Count (Paragraphs)')
    plt.xlabel('Paragraph')
    plt.ylabel('Word Count')

    plt.xlim(0, len(paragraphX))

    plt.show()
