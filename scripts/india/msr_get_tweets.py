
# coding: utf-8

# In[1]:

import json
import os
import pandas as pd
import time
from datetime import datetime, timedelta

# In[2]:


import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


#Added import to handle decahose-like output formatting/compression.
import bz2

#Added imports for command-line arg config file.
import sys
import configparser

#For saving the metadata
import sqlite3
from sqlite3 import Error



def get_latest_tweet_id(screen_name):
    filename = screen_name + '.json'
    df = pd.read_json(os.path.join(config['in_directory'], filename))
    df = df.sort_values(['created_at'])
#     print df.created_at.tolist()[-1]
    return df.id_str.tolist()[-1], df


def get_all_recent_tweets(id_, from_id):
    count = 1
    all_tweets = []
    tweets_json = []
    tweets = api.user_timeline(user_id = id_, count = 200, since_id = from_id, tweet_mode='extended')
    if len(tweets) == 0:
        return []
    tweets_json = [elem._json for elem in tweets]
    all_tweets.extend(tweets_json)
    screen_name = tweets_json[0]['user']['screen_name']
    print('\t', count, len(all_tweets), screen_name)
    while True:
        until_id = all_tweets[-1]['id_str']
        tweets = api.user_timeline(user_id = id_, count = 200, max_id = until_id, since_id = from_id, tweet_mode='extended')
        count += 1
        if len(tweets) == 1:
            break
        tweets_json = [elem._json for elem in tweets]
        all_tweets.extend(tweets_json)
        
        print('\t', count, len(all_tweets), screen_name, until_id, tweets_json[0]['created_at'], tweets_json[-1]['created_at'])
    return all_tweets

def get_all_recent_tweets_w_screen_name(screen_name, from_id):
    count = 1
    all_tweets = []
    tweets_json = []
    tweets = api.user_timeline(screen_name = screen_name, count = 200, since_id = from_id, tweet_mode='extended')
    if len(tweets) == 0:
        return []
    tweets_json = [elem._json for elem in tweets]
    all_tweets.extend(tweets_json)
    print('\t', count, len(all_tweets), screen_name, 'pulling using screen_name')
    while True:
        until_id = all_tweets[-1]['id_str']
        tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = until_id, since_id = from_id, tweet_mode='extended')
        count += 1
        if len(tweets) == 1:
            break
        tweets_json = [elem._json for elem in tweets]
        all_tweets.extend(tweets_json)
        
        print('\t', count, len(all_tweets), screen_name, until_id, tweets_json[0]['created_at'], tweets_json[-1]['created_at'])
    return all_tweets


def get_new_accounts(id_):
    count = 1
    all_tweets = []
    tweets_json = []
    print(id_)
    tweets = api.user_timeline(user_id = int(id_), count = 200, tweet_mode='extended')
    if len(tweets) == 0:
        return []
    tweets_json = [elem._json for elem in tweets]
    all_tweets.extend(tweets_json)
    screen_name = tweets_json[0]['user']['screen_name']
    print('\t', count, len(all_tweets), screen_name)
    while True:
        until_id = all_tweets[-1]['id_str']
        tweets = api.user_timeline(user_id = id_, count = 200, max_id = until_id, tweet_mode='extended')
        count += 1
        if len(tweets) == 1:
            break
        tweets_json = [elem._json for elem in tweets]
        all_tweets.extend(tweets_json)
        
        print('\t', count, len(all_tweets), screen_name, until_id, tweets_json[0]['created_at'], tweets_json[-1]['created_at'])
    return all_tweets


def get_new_accounts_w_screen_name(screen_name):
    count = 1
    all_tweets = []
    tweets_json = []
    tweets = api.user_timeline(screen_name = screen_name, count = 200, tweet_mode='extended')
    if len(tweets) == 0:
        return []
    tweets_json = [elem._json for elem in tweets]
    all_tweets.extend(tweets_json)
    print('\t', count, len(all_tweets), screen_name, 'pulling using screen_name')
    while True:
        until_id = all_tweets[-1]['id_str']
        tweets = api.user_timeline(screen_name = screen_name, count = 200, max_id = until_id, tweet_mode='extended')
        count += 1
        if len(tweets) == 1:
            break
        tweets_json = [elem._json for elem in tweets]
        all_tweets.extend(tweets_json)
        
        print('\t', count, len(all_tweets), screen_name, until_id, tweets_json[0]['created_at'], tweets_json[-1]['created_at'])
    return all_tweets


def get_screen_name(id_):
    return accountsOfInterest[accountsOfInterest.id == id_]['screen_name'].tolist()[0]


def get_recently_pulled_accounts(directory):
    print('Getting recent accounts..')
    pulled_recently = []
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        mtime = os.path.getmtime(path)
        #     print path, mtime
        d = datetime.fromtimestamp(mtime)
        cutoff = datetime.now() - timedelta(days=1)
        if d > cutoff:
            pulled_recently.append(f.split('.json')[0])
    return pulled_recently
        

def get_user_ids():
    files = os.listdir(config['in_directory'])
    user_ids = []
    for f in files:
        df_tweets = pd.read_json(os.path.join(config['in_directory'], f))
        u_id = df_tweets['user'][0]['id']
        user_ids.append(u_id)
    return user_ids


#Write the current the tweets to the Bzip2 compressed JSON file and return the
#ID of the most recent tweet.
def writeOutput(tweets, screenName):
    #Create the output dir for the screen name if necessary
    outDir = os.path.join(config['out_directory'], screenName)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    #Setup the compressed output stream
    compressor = bz2.BZ2Compressor()
    outFilename = os.path.join(outDir, f'tweets.{outFileTimestamp}.bz2')
    outFile = open(outFilename, 'wb')

    latest = None
    latestID = None

    for tweet in tweets:
        jsonStr = json.dumps(tweet)
        output = compressor.compress(f'{jsonStr}\n'.encode())

        if output:
            outFile.write(output)

        #Update the latest tweet for this set of tweets
        timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')

        if latest == None or timestamp > latest:
            latest = timestamp
            latestID = tweet['id_str']


    #Flush any remaining compressed data to the output file and close the stream.
    remaining = compressor.flush()

    if remaining:
        outFile.write(remaining)

    outFile.close()

    return latestID


#Loads the configuration (API keys, in/out dirs from config file).
def getConfig():
    if len(sys.argv) < 2:
        print('Usage: python msr_get_tweets.py <CONFIG_FILE>')
        quit()

    configFile = sys.argv[1]

    if not os.path.exists(configFile):
        print(f'Could not find config file {configFile}')
        quit()

    parser = configparser.ConfigParser()
    parser.read(configFile)
    config = parser['Default']

    return config


#Configures/returns the Twitter API client using the API keys from config.
def getAPIClient(config):
    #Twitter API Keys
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    access_token = config['access_token']
    access_secret = config['access_secret']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
     
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
    return api


#Save the metadata containing the most recent tweet for all users.
def saveMetadata(metadataConn, screenName, tweetID):
    cursor = metadataConn.cursor()
    cursor.execute(f"INSERT OR REPLACE INTO latest(screen_name, latest_tweet_id) VALUES('{screenName}', '{tweetID}');")
    metadataConn.commit()
    cursor.close()


#Get the latest tweet ID for the given screen name from the metadata. Returns None
#if the screen name is not in the DB.
def getLatestTweetID(metadataConn, screenName):
    cursor = metadataConn.cursor()
    cursor.execute(f"SELECT latest_tweet_id FROM latest WHERE screen_name = '{screenName}';")

    row = cursor.fetchone()

    if row != None:
        cursor.close()
        return row[0]

    cursor.close()
    return None


#Load the metadata database containing the most recent tweet ID for all users.
#We store in a SQLite3 database so we can don't lose the latest tweets for users
#we've already processed if the program crashes or is stopped early.
def loadMetadataDB():
    rootDir = os.path.dirname(os.path.abspath(__file__))
    metaFilename = os.path.join(rootDir, '.metadata')

    try:
        conn = sqlite3.connect(metaFilename)

        #Add the table if neccessary.
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS latest (
                            screen_name text PRIMARY KEY,
                            latest_tweet_id text NOT NULL
                            );  ''')
        cursor.close()
        conn.commit()
        return conn

    except Error as e:
        print(e)
        print(f"ERROR: Couldn't load or create metadata file {metaFilename} to save latest tweet IDs. Terminating.")
        quit()


#Setup the timestamp for the output files. All files for the same run have the same timestamp.
outFileTimestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')

#Load the configuration from command line arg.
config = getConfig()

#Load the metadata containing the latest tweets for all users
metadataDB = loadMetadataDB()

#Setup the api client.
api = getAPIClient(config)


# In[3]:

accountsOfInterest = pd.read_json(config['account_list'])#'/home/anmolpanda/get_tweets_usa/code/all_accounts_20_aug.json')
accountsOfInterest = accountsOfInterest[['id', 'screen_name']].sample(frac=1)

#df = pd.read_csv('/home/anmolpanda/get_tweets_usa/code/high_recall_predicted_set.csv')
accountsOfInterest = accountsOfInterest.dropna().reset_index(drop=True)
print(len(accountsOfInterest))


#current_accounts = get_recently_pulled_accounts(config['out_directory'])
current_accounts = []
# In[7]:
ids = accountsOfInterest.id.tolist()

start = time.time()
error_accounts = {}
count = 0
totalTweets = 0

for id_ in ids:
    try:
        s = get_screen_name(id_)
        id_ = int(id_)

        if s in current_accounts:
            continue
        print(count, s, id_)
        count += 1

        #Get the latest tweet id from the metadata if present for this screen name
        from_id = getLatestTweetID(metadataDB, s)
        
        #Otherwise, the screen name is not in the metadata. Look for new accounts.
        if from_id == None:
            try:
                tweets = get_new_accounts(id_)
            except Exception as e:
                error_accounts[s] = e
                print(e)

                try:
                    tweets = get_new_accounts_w_screen_name(s)
                except Exception as e:
                    continue

            if len(tweets) > 0:
                #Write the output to the compressed file and update the latest tweet ID
                latestTweetID = writeOutput(tweets, s)
                saveMetadata(metadataDB, s, latestTweetID)
                totalTweets += len(tweets)

            continue
        try:
            tweets = get_all_recent_tweets(id_, from_id)
        except Exception as e:
            error_accounts[s] = e
            print(e)

            try:
                tweets = get_all_recent_tweets_w_screen_name(s, from_id)
            except Exception as e:
                continue

        if len(tweets) > 0:
            #Write the output to the compressed file and update the latest tweet ID
            latestTweetID = writeOutput(tweets, s)
            saveMetadata(metadataDB, s, latestTweetID)
            totalTweets += len(tweets)


        else: #If we got here, then we have no tweets to write for this user.
            print(f'\tNo new tweets for {s}')

    except Exception as e:
        print(e)
        error_accounts[s] = e


#Don't produce an output file if we didn't get any new tweets at all.
if totalTweets == 0:
    os.remove(outFilename)


#Close the metadata DB connection.
metadataDB.close()


end = time.time()
df_errors = pd.DataFrame({'screen_name':error_accounts.keys(), 'error': error_accounts.values()})
d = datetime.now().strftime('%Y_%m_%d_%H_%M_%s')
df_errors.to_json(os.path.join(config['error_directory'], 'errors_'+d+'.json'))
print(f'Retrieved a total of {totalTweets} new tweets.')
print(f'Time taken: {end - start} seconds.')



