import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

import matplotlib.pyplot as plt
import os
from SentimentAnalysis import SentimentAnalysis

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

analysis = SentimentAnalysis()

###Things
splitWord = [" ", "—"]
splitSentence = [".", "!", "?"]

##I'm Lazy lol
text = open(r"Dalloway.html", "r").read()

cleanText = text
cleanText = cleanText.replace("\n\n", "¡¡ººBREAKºº¡¡") #temporarily store paragraph changes
cleanText = cleanText.replace("\n", " ")
cleanText = cleanText.replace("¡¡ººBREAKºº¡¡", "\n")
cleanText = cleanText.replace("\t", " ")

# cleanText = cleanText.replace("<p></p>", "ƒƒ©©PARAGRAPHSPLIT©©ƒƒ") #store full breaks
cleanText = cleanText.replace("<p></p>", " ") #store full breaks

# cleanText = cleanText.replace("<p class=\"poem\"></p>", "ƒƒ©©POEMSPLIT©©ƒƒ") #store poem breaks
cleanText = cleanText.replace("<p class=\"poem\"></p>", " ") #store poem breaks

# cleanText = re.sub(r'<hr[^><]*>', 'ƒƒ©©PARAGRAPHSPLIT©©ƒƒ', cleanText)
cleanText = re.sub(r'<hr[^><]*>', ' ', cleanText)

cleanText = replaceTags(cleanText)
cleanText = re.sub(r'[ ]+', ' ', cleanText)

output = open("cleanedText.txt", "w")
# output.write(cleanText)


wordArray = re.split(r"[ —]", cleanText)
temp = []
for i in range(len(wordArray)):
    text = wordArray[i]
    text = re.sub(r'[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-]', '', text)

    text = text.replace("\n", " ").strip()
    text = re.sub(r'[ ]+', ' ', text)
    if(text != ""):
        temp.append(text)
wordArray = temp

#sentence

sentenceArray = []
prevEnd = 0
quote = False
temp = ""
for reg in re.finditer(r"((?<!Dr)(?<!Mrs)(?<!Mr)(?<!\.)\.|!|\?)( |\n|<)", cleanText):
    start, end = reg.span()
    if("“" in cleanText[prevEnd:end] and "”" not in cleanText[prevEnd:end]):
        quote = True
        temp = cleanText[prevEnd:end]
        continue
    elif(quote and "”" in cleanText[prevEnd:end]):
        temp = cleanText[prevEnd:end]

        quote = False
        text = temp
        text = text.replace("\n", " ").strip()
        text = re.sub(r'[ ]+', ' ', text)
        sentenceArray.append(text)
        temp=""
        prevEnd = end
    elif(not(quote)):
        text = cleanText[prevEnd:end]
        text = text.replace("\n", " ").strip()
        text = re.sub(r'[ ]+', ' ', text)
        sentenceArray.append(text)
        prevEnd = end

##FREQ
showFrequency = False
if(showFrequency):
    wordFreq = {}
    for word in wordArray:
        word = word.lower()
        if(word not in wordFreq.keys()):
            wordFreq[word] = 1
        else:
            wordFreq[word] += 1

    sortDict = dict(sorted(wordFreq.items(), key=lambda item: -item[1]))
    print(sortDict)
    for(word, count) in sortDict.items():
        output.write(word + ": " + str(count) + "\n")

##EDGE FOR SENTIMENT
showExtremeSentiment = False
if(showExtremeSentiment):
    print(sentenceArray)
    output.write("\n\n".join(sentenceArray))
    for sentence in sentenceArray:
        sentiment = analysis.vader(sentence)['compound']
        if(abs(sentiment) > 0.75):
            output.write(sentence + "\nSentiment: "+str(sentiment)+"\n\n")

##min max for sentiment
showMinMaxSentiment = False
if(showMinMaxSentiment):
    high, low, neutral, total, bigHigh, bigLow = 0,0,0,0, 0, 0
    for sentence in sentenceArray:
        sentiment = analysis.vader(sentence)['compound']
        if((sentiment) > 0):
            high+=1
            if(sentiment >= 0.75):
                bigHigh+=1
        elif((sentiment) < 0):
            low+=1
            if(sentiment <= -0.75):
                bigLow+=1
        else:
            neutral+=1
        total+=1
    print("High: ", high, "\nLow: ", low, "\nNeutral: ", neutral, "\nTotal: ", total)
    print("Big High: ", bigHigh, "\nBig Low: ", bigLow)


##sentiment bar chart
showSentimentBarChart = False
if(showSentimentBarChart):
    sentimentX = []
    sentimentY = []
    i = 0
    for sentence in sentenceArray:
        i+=1
        sentimentX.append(i)

        sentimentY.append(analysis.vader(sentence)['compound'])
    plt.bar(sentimentX, sentimentY, width = 1, color = "black")

    plt.title('Polarity of Sentiment Analysis (Sentences)')
    plt.xlabel('Sentence')
    plt.ylabel('Polarity')

    plt.xlim(0, len(sentimentX))
    plt.ylim(-1,1)
    plt.show()

##sentiment without quotes
showSentimentNoQuotes = False
if(showSentimentNoQuotes):
    pos, neg, neu, total, bigPos, bigNeg = 0,0,0,0, 0, 0
    for sentence in sentenceArray:
        if not("“" in sentence or "”" in sentence):
            polarity = analysis.vader(sentence)['compound']
            if(polarity > 0):
                pos+=1
                if(polarity >= 0.75):
                    bigPos+=1
            elif(polarity < 0):
                neg+=1
                if(polarity <= -0.75):
                    bigNeg+=1
            else:
                neu+=1
            total+=1
    print("Positive: ", pos, "\nNegative: ", neg, "\nNeutral: ", neu, "\nTotal: ", total)
    print("Big Positive: ", bigPos, "\nBig Negative: ", bigNeg)

##polar non-quote count
showPolarNonquote = True
if(showPolarNonquote):
    polarQ, npolarQ, polarNQ, npolarNQ = 0, 0, 0, 0
    for sentence in sentenceArray:
        polar = abs(analysis.vader(sentence)['compound'])>=0.75
        quote = "“" in sentence or "”" in sentence
        polarQ += polar and quote
        npolarQ += not(polar) and quote
        polarNQ += polar and not(quote)
        npolarNQ += not(polar) and not(quote)
    print("Polar Quote: ", polarQ, "\nNon-Polar Quote: ", npolarQ, "\n")
    print("Polar Non-Quote: ", polarNQ, "\nNon-Polar Non-Quote: ", npolarNQ)

