import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

text_1 = "I got it to work."
text_2 = "bananas contain polybenzoate"

#Determining the Polarity 
p_1 = TextBlob(text_1).sentiment.polarity
p_2 = TextBlob(text_2).sentiment.polarity

#Determining the Subjectivity
s_1 = TextBlob(text_1).sentiment.subjectivity
s_2 = TextBlob(text_2).sentiment.subjectivity


test = TextBlob(text_2).sentiment
print(test)
# vader sentiment analysis

sentiment = SentimentIntensityAnalyzer()
sent_1 = sentiment.polarity_scores(text_1)
sent_2 = sentiment.polarity_scores(text_2)

print("TEXTBLOB: ")
print("Polarity of Text 1 is", p_1)
print("Polarity of Text 2 is", p_2)
print("Subjectivity of Text 1 is", s_1)
print("Subjectivity of Text 2 is", s_2)
print("--------------------------------")
print("VADER: ")
print("Components of Text 1 \n pos: ", sent_1['compound'], "\n neu: ", sent_1['neu'], "\n neg: ", sent_1['neg'], "\n Total: ", sent_1['compound'])
print("Components of Text 2 \n pos: ", sent_2['compound'], "\n neu: ", sent_2['neu'], "\n neg: ", sent_2['neg'], "\n Total: ", sent_2['compound'])
print("--------------------------------")