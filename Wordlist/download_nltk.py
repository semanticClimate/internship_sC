import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words("english"))