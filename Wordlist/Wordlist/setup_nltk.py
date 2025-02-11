import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')

from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words("english"))