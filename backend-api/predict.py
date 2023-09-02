import torch
import torch.nn as nn
import transformers
from transformers import BartTokenizer, BartForConditionalGeneration

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import regex as re
import unidecode
import contractions


stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):

    # to lower case
    text = text.lower()

    # remove accents
    text = unidecode.unidecode(text)

    # remove html tags
    html_pattern = r'<.*?>'
    without_html = re.sub(pattern=html_pattern, repl=' ', string=text)

    # remove urls
    url_pattern = r'https?://\S+|www\.\S+'
    without_urls = re.sub(pattern=url_pattern, repl=' ', string=without_html)
    
    # remove contractions
    without_contractions = contractions.fix(without_urls)

    # remove punctuation
    punct_pattern = r'[^\w\s]'
    without_punct = re.sub(pattern=punct_pattern, repl=' ', string=without_contractions)

    # remove extra spaces
    space_pattern = r'\s+'
    without_spaces = re.sub(pattern=space_pattern, repl=' ', string=without_punct)

    # remove stop words
    word_tokens = word_tokenize(without_spaces)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    # lemmatize
    lemmatized = [lemmatizer.lemmatize(w) for w in filtered_sentence]

    return ' '.join(lemmatized)

def sentiment(s):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(s)
    dct = {
        "pos_sentiment": score["pos"],
        "neg_sentiment": score["neg"],
        "neu_sentiment": score["neu"],
    }
    return dct

def summary(input_text):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large')

    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large')

    # Tokenize input text
    input_ids = tokenizer.encode(clean_text(input_text), return_tensors='pt')

    # Generate text
    output = model.generate(input_ids, max_length=50, num_beams=5, early_stopping=True)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    senti = sentiment(generated_text)

    return generated_text, senti["pos_sentiment"], senti["neg_sentiment"], senti["neu_sentiment"]
    