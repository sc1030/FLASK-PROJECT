import os
import time
import tweepy
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt
from tweepy.errors import TooManyRequests

# Set up your Twitter API v2 credentials (Bearer Token)
bearer_token= ""

client = tweepy.Client(bearer_token=bearer_token)

def analyze_sentiment(keyword, retries=5):
    tweet_data = []
    positive = negative = neutral = 0

    for _ in range(retries):
        try:
            tweets = client.search_recent_tweets(
                query=keyword,
                max_results=50,
                tweet_fields=["created_at", "text", "lang"]
            )

            if tweets.data:
                for tweet in tweets.data:
                    if tweet.lang != "en":
                        continue
                    text = tweet.text
                    polarity = TextBlob(text).sentiment.polarity
                    if polarity > 0:
                        sentiment = 'positive'
                        positive += 1
                    elif polarity < 0:
                        sentiment = 'negative'
                        negative += 1
                    else:
                        sentiment = 'neutral'
                        neutral += 1
                    tweet_data.append([tweet.created_at, text, sentiment])

            os.makedirs('static/images', exist_ok=True)
            generate_pie_chart(positive, negative, neutral)

            return tweet_data

        except TooManyRequests as e:
            reset_time = int(e.response.headers.get('x-rate-limit-reset', time.time() + 60))
            sleep_time = max(reset_time - int(time.time()) + 1, 60)
            print(f"Rate limit exceeded. Retrying after {sleep_time} seconds...")
            time.sleep(sleep_time)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return None

def save_to_csv(tweet_data):
    with open('result.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Tweet', 'Sentiment'])
        writer.writerows(tweet_data)

def generate_pie_chart(positive, negative, neutral):
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.savefig('static/images/plot1.png')
    plt.close()

if __name__ == "__main__":
    keyword = input("Enter a keyword to analyze: ")
    tweet_data = analyze_sentiment(keyword)

    if tweet_data:
        save_to_csv(tweet_data)
        print("Analysis complete. CSV and chart saved.")
    else:
        print("No data available due to rate limits or other errors.")