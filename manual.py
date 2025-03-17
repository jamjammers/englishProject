from SentimentAnalysis import SentimentAnalysis as SA
import matplotlib.pyplot as plt

analysis = SA()
while True:
    sentence = input("what sentence would you like to analyze? (type: \"END\" to end)")
    if sentence == "END":
        break
    analysis.print(sentence)
