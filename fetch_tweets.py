import tweepy
import pandas as pd
import time

consumer_key="..."
consumer_secret="..."

filename = "file.csv" # nazwa pliku wyjściowego
sleep = 10 # ile sekund powinnien poczekać z następną iteracją (min. 5)
loops = 10000 # liczba iteracji
query = "eurovision until:2023-05-30 since:2023-05-10" # zapytanie do pobierania tweetów

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret
)

api = tweepy.API(auth)

cols = ['id', 'text', 'user_id', 'user_name']

try:
    df = pd.read_csv(filename)
except: 
    df = pd.DataFrame(columns=cols) 

df.set_index('id')

for i in range(0, loops):
    tweets = api.search_tweets(query, lang="en", count=100)

    for tweet in tweets:
        
        if not any(df['id'] == tweet.id):
            df = pd.concat(
                [
                    df, 
                    pd.DataFrame([[tweet.id, tweet.text,tweet.user.id,tweet.user.screen_name]], columns=cols)
                ],
                ignore_index=True
            )

    df.to_csv(filename, index=False)
    print(len(df.index))
    time.sleep(sleep)