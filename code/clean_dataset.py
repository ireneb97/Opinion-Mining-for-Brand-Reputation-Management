# -*- coding: utf-8 -*-
import os
import glob
import re
import time
import numpy as np
import pandas as pd
import csv
from tqdm import tqdm        
from colorama import Fore, Style
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
from google_trans_new import google_translator

def clean_text(text, remove_contractions = False, twitter = False):
    regrex_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        "]*", flags=re.UNICODE)
    text = re.sub(regrex_pattern,'',text)
    # removing &amp; character that appers during encoding
    text = re.sub(r'&amp;', '', str(text))
    # removing urls, in twitter all begins with https:t.co 
    if twitter: text = re.sub(r"https?:\/\/[t.co]+\/*[\d|\w]*", '', str(text))
    
    if remove_contractions:
        text = re.sub(r"won\'t", "will not", text)
        text = re.sub(r"can\'t", "can not", text)
        text = re.sub(r"can\'t", "can not", text)
        text = re.sub(r"n\'t", " not", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'s", " is", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'t", " not", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'m", " am", text)
    return text

def preprocessing_text(text, language, twitter = False):
    try:
        stops = set(stopwords.words(language))
        stemming = SnowballStemmer(language)
        pass
    except (OSError, ValueError):
        stops = set(stopwords.words('english'))
        stemming = SnowballStemmer('english')
        pass
    # clear text from emoticons, chinese chars, urls and so on
    text = clean_text(text, language == 'english', twitter) 
    # tokenization
    if twitter:
        question = '?' in text.split('#')[0]
        tk = TweetTokenizer()
        tokens = tk.tokenize(text)
    else: tokens = nltk.word_tokenize(text)
    # all words in lower case and remove stop words and special chars
    tokens = [w.lower() for w in tokens if ((w.isalnum() and not twitter) or (w.isalnum() or '#'in w or '@' in w)) and not w in stops]
    # stemming
    tokens = [stemming.stem(w) for w in tokens]
    return [tokens, question] if twitter else tokens

def standardizing_date(date):
    month_to_number = {'january': '01', 'february': '02', 'march': '03', 'april': '04', 'may': '05', 'june': '06',
                       'july': '07', 'august': '08', 'september': '09', 'october': '10', 'november': '11', 'december': '12'}
    date = date.split(' ')
    date[0] = month_to_number[date[0].lower()]
    if len(date[1]) == 1: date[1] = '0'+date[1]
    resulting_date = date[2]+date[0]+date[1]
    return resulting_date

def computing_score(score):
    score = score.split(' ')[0]
    if score == 'no': return None
    else: return int(float(score))

def verified_purchase_boolean(ver_pur):
    if ver_pur.lower() == 'verified purchase':
        return True
    else:
        return False

def detect_language_from_text(text, title = None):
    text_wout_hashtag = text.split('#')[0]
    if len(text_wout_hashtag) > 0: text = text_wout_hashtag
    if text.isspace() or text == None:
        if title:
            text = title
        else:
            return 'english'
    try:
        text = text[:3000]
        pass
    except Exception:
        return 'english'
    for attempt in range(10):
        try:
            detector = google_translator()
            lang = detector.detect(text)[1]
            return lang
        except Exception as e:
            print(Style.BRIGHT+Fore.RED + '\n  Error: '+ str(e)+ Style.RESET_ALL)
            time.sleep(10)
            continue
        break
    return 'error'

def detecting_upvotes(upvotes):
    upvotes = upvotes.split(' ')[0]
    upvotes = re.sub(",", "", upvotes)
    if upvotes.lower() == 'one':
        return 1
    return int(upvotes)

def is_positive(sia, text: str) -> int:
    """True if text has positive compound sentiment, False otherwise."""
    return 1 if sia.polarity_scores(text)["compound"] > 0 else -1

def cleaning_amazon_datasets():
    os.chdir("G:\Il mio Drive\Project_Data_Mining\Data\Amazon")
    datasets = [f for f in glob.glob("*.csv")]
    for name_dataset in datasets:
        print("Checking operations on dataset:'"+name_dataset+"'")
        if os.path.exists('./clean_dataset/clean_'+name_dataset):
            cleaning = False
        else:
            cleaning = True
        if os.path.exists('./preprocessed_dataset/preprocessed_'+name_dataset) and not cleaning:
            preprocessing = False
            print('  > Dataset already cleaned and preprocessed')
        else:
            preprocessing = True
        time.sleep(1)
        
        if cleaning:
            with open(name_dataset, encoding='utf-8-sig', errors='replace') as f:
                df = pd.read_csv(f, sep=',', names=['name','score','title','place','date','verified purch','text','upvotes'])
                name = df['name'].to_dict()
                score = df['score'].to_dict()
                title = df['title'].to_dict()
                place = df['place'].to_dict()
                date = df['date'].to_dict()
                ver_purchase = df['verified purch'].to_dict()
                text = df['text'].to_dict()
                upvotes = df['upvotes'].to_dict() 
            new_df = {}
            for i in tqdm(name, desc='Cleaning dataset'):
                if i > 0:
                    new_score = computing_score(score[i])
                    new_date = standardizing_date(date[i])
                    new_ver_pur = verified_purchase_boolean(ver_purchase[i])
                    new_upvotes = detecting_upvotes(upvotes[i])
                    if title[i] == 'title not found': title[i] = None
                    language = detect_language_from_text(text[i], title[i])
                    new_df[i] = [name[i], new_score, title[i], place[i], new_date, new_ver_pur, text[i], new_upvotes, language]
                    time.sleep(1)
               
            with open('./clean_dataset/clean_'+name_dataset, 'wt', encoding='utf-8', newline='') as of:
                writer = csv.writer(of, delimiter = ',')
                writer.writerow(['name','score','title','place','date','verified purch','text','upvotes', 'language'])
                for i in new_df: 
                    writer.writerow(new_df[i])
                    
        if preprocessing:
            with open('./clean_dataset/clean_'+name_dataset, encoding='utf-8-sig', errors='replace') as f:
                df = pd.read_csv(f, sep=',', names=['name','score','title','place','date','verified purch','text','upvotes', 'language'])
                df = df.replace({np.nan: None})
                name = df['name'].to_dict()
                score = df['score'].to_dict()
                title = df['title'].to_dict()
                place = df['place'].to_dict()
                date = df['date'].to_dict()
                ver_purchase = df['verified purch'].to_dict()
                text = df['text'].to_dict()
                upvotes = df['upvotes'].to_dict()
                language = df['language'].to_dict()
            new_text = {}
            new_title = {}
            ids = {}
            for i in tqdm(text, desc='Preprocessing dataset'):
                if i > 0:
                    ids[i] = i
                    if title[i]: new_title[i] = ' '.join(preprocessing_text(title[i], language[i]))
                    else: new_title[i] = None
                    if text[i]: new_text[i] = ' '.join(preprocessing_text(text[i], language[i]))
                    else: new_text[i] = None
                    
            with open('./preprocessed_dataset/preprocessed_'+name_dataset, 'wt', encoding='utf-8', newline='') as of:
                writer = csv.writer(of, delimiter = ',')
                writer.writerow(['id','name','score','title','place','date','verified purch','text','upvotes', 'language'])
                for i in text: 
                    if i > 0 and (new_title[i] or new_text[i]): 
                        writer.writerow([ids[i], name[i], score[i], new_title[i], place[i], date[i], ver_purchase[i], new_text[i], upvotes[i], language[i]])

def cleaning_twitter_datasets():
    os.chdir("G:\Il mio Drive\Project_Data_Mining\Data\Twitter")
    datasets = [f for f in glob.glob("*.csv")]
    for name_dataset in datasets: 
        start_cleaning = 0
        mode = 'wt'
        with open(name_dataset, encoding='utf-8-sig', errors='replace') as f:
            df = pd.read_csv(f, sep=',', names=['username','datatime', 'tweet_text', 'retweeted_text', 'likes', 'retweets', 'comments'])
            df = df.replace({np.nan: None})
            name = df['username'].to_dict()
            date = df['datatime'].to_dict()
            text = df['tweet_text'].to_dict()
            retweet_text = df['retweeted_text'].to_dict()
            likes = df['likes'].to_dict()
            retweets = df['retweets'].to_dict()
            comments = df['comments'].to_dict() 
        print("Checking operations on dataset:'"+name_dataset+"'")
        if os.path.exists('./clean_dataset/clean_'+name_dataset):
            with open('./clean_dataset/clean_'+name_dataset, encoding='utf-8-sig', errors='replace') as f:
                df_clean = pd.read_csv(f, sep=',', names=['username','datatime', 'tweet_text', 'retweeted_text', 'likes', 'retweets', 'comments', 'language'])
                if len(name) == len(df_clean['username']): cleaning = False
                else:
                    cleaning = True
                    start_cleaning = len(df_clean['username']) - 1
                    mode = 'a'
                    print('  > Start cleaning from line '+str(start_cleaning + 1))
        else:
            cleaning = True
        if os.path.exists('./preprocessed_dataset/preprocessed_'+name_dataset) and not cleaning:
            preprocessing = False
            print('  > Dataset already cleaned and preprocessed')
        else:
            preprocessing = True
        time.sleep(1)
        
        if cleaning:
            with open('./clean_dataset/clean_'+name_dataset, mode, encoding='utf-8', newline='') as of:
                writer = csv.writer(of, delimiter = ',')
                if mode == 'wt': writer.writerow(['username','datatime', 'tweet_text', 'retweeted_text', 'likes', 'retweets', 'comments', 'language'])
                for i in tqdm(name, desc='Cleaning dataset'):
                    if i > start_cleaning:
                        if not name[i] or name[i].isspace(): name[i] = 'unknown'
                        new_date = re.split('T',date[i])[0]
                        new_date = re.sub("-", "", new_date)
                        language = detect_language_from_text(text[i])
                        if language == 'error':
                            print(Style.BRIGHT+Fore.RED +'\nFatal error: the computation has been stopped'+ Style.RESET_ALL)
                            return
                        writer.writerow([name[i], new_date, text[i], retweet_text[i], likes[i], retweets[i], comments[i], language])
                        time.sleep(1)
                    
        if preprocessing:
            with open('./clean_dataset/clean_'+name_dataset, encoding='utf-8-sig', errors='replace') as f:
                df = pd.read_csv(f, sep=',', names=['username','datatime', 'tweet_text', 'retweeted_text', 'likes', 'retweets', 'comments', 'language'])
                df = df.replace({np.nan: None})
                name = df['username'].to_dict()
                date = df['datatime'].to_dict()
                text = df['tweet_text'].to_dict()
                retweet_text = df['retweeted_text'].to_dict()
                likes = df['likes'].to_dict()
                retweets = df['retweets'].to_dict()
                comments = df['comments'].to_dict() 
                language = df['language'].to_dict()
            
            # initializing sentiment analyzer
            try:
                sia = SentimentIntensityAnalyzer()
                pass
            except LookupError:
                nltk.download('vader_lexicon')
                sia = SentimentIntensityAnalyzer()
                pass 
            
            new_text = {}
            new_retweet_text = {}
            question = {}
            new_tweet_no_ash = {}
            new_retweet_no_ash = {}
            sentiment_analysis = {}
            for i in tqdm(text, desc='Preprocessing dataset'):
                if i > 0:
                    if retweet_text[i]: 
                        new_retweet_text[i] = ' '.join(preprocessing_text(retweet_text[i], language[i], True)[0])
                        new_retweet_no_ash[i] = re.sub(r"[#|@]+[\d|\w]*", '', str(new_retweet_text[i]))
                    else: 
                        new_retweet_text[i] = retweet_text[i]
                        new_retweet_no_ash[i] = retweet_text[i]
                    new_text[i], question[i] = preprocessing_text(text[i], language[i], True)
                    new_text[i] = ' '.join(new_text[i])
                    new_tweet_no_ash[i] = re.sub(r"[#|@]+[\d|\w]*", '', str(new_text[i]))
                    if question[i]:
                        sentiment_analysis[i] = 0
                    else: sentiment_analysis[i] = is_positive(sia, text[i])
                    
            with open('./preprocessed_dataset/preprocessed_'+name_dataset, 'wt', encoding='utf-8', newline='') as of:
                writer = csv.writer(of, delimiter = ',')
                writer.writerow(['username', 'datatime', 'tweet_text', 'retweeted_text', 'likes', 
                                 'retweets', 'comments', 'language', 'is a question', 'tweet wout hashtag', 
                                 'retweet wout hashtag', 'sentiment analysis'])
                for i in text: 
                    if i > 0: writer.writerow([name[i], date[i], new_text[i], new_retweet_text[i], 
                                               likes[i], retweets[i], comments[i], language[i], question[i], 
                                               new_tweet_no_ash[i], new_retweet_no_ash[i], sentiment_analysis[i]])

if __name__ == '__main__':
    cleaning_amazon_datasets()
    cleaning_twitter_datasets()