from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import formatCodes
from textblob import TextBlob

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
            self.polarity(text))

        print(formatCodes.DARKCYAN+
            "   subjectivity: "+
            formatCodes.ENDC, 
            self.subjectivity(text))

        print(formatCodes.BOLD+
            "  VADER:"+
            formatCodes.ENDC)

        print(formatCodes.GREEN+
            "   positive:     "+
            formatCodes.ENDC, 
            self.vader(text)['pos'])

        print(formatCodes.YELLOW+
            "   neutral:      "+
            formatCodes.ENDC, 
            self.vader(text)['neu'])

        print(formatCodes.RED+
            "   negative:     "+
            formatCodes.ENDC, 
            self.vader(text)['neg'])

        print(formatCodes.PURPLE+
            "   compound:     "+
            formatCodes.ENDC, 
            self.vader(text)['compound'])
    
    def getPrint(self, text):
        out = ""
        out+="Sentiment anlysis (print):"+"\n"

        out+=" text: "+text+"\n"

        out+=" Sentiment Analysis"+"\n"

        out+="  TextBlob:"
        out+="   polarity:     "+str(self.polarity(text))+"\n"
        out+="   subjectivity: "+str(self.subjectivity(text))+"\n"
        
        out+="  VADER:"+"\n"
        out+="   positive:     "+str(self.vader(text)['pos'])+"\n"
        out+="   neutral:      "+str(self.vader(text)['neu'])+"\n"
        out+="   negative:     "+str(self.vader(text)['neg'])+"\n"
        out+="   compound:     "+str(self.vader(text)['compound'])+"\n"

        return out
