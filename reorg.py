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

sentenceArray = re.split(r"((?<!Dr)(?<!Mrs)(?<!Mr)(?<!\.)\.|!|\?)( |\n|<)",cleanText)
output.write("\n\n".join(sentenceArray))

prevEnd = 0
for reg in re.finditer(r"((?<!Dr)(?<!Mrs)(?<!Mr)(?<!\.)\.|!|\?)( |\n|<)", cleanText):
    # print(reg.span()) 
    start, end = reg.span()
    # print(cleanText[prevEnd:end])
    text = cleanText[prevEnd:end]

    text = text.replace("\n", " ").strip()
    text = re.sub(r'[ ]+', ' ', text)
    analysis.print(text)

    prevEnd = end
wordArray = re.sub(r"[^qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-]",re.split(r"[ —]", cleanText))

# print(sentenceArray)