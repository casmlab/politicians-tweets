import json
import yaml
import us
import tweepy
import time
import pickle
import pandas as pd
from git import Repo
from datetime import date
from pathlib import Path
from pprint import pprint

# Available from Twitter API:
#   id/id_str
#   screen_name (handle)
#   twitter_name
#   
# Available from congress-legislators:
#   real_name
#   bioguide
#   district
#   party
#   woman

api_keys_file = open("twitter_api_keys.json", "r")
api_keys = json.load(api_keys_file)["politicsdataba1"]["Politicians Dataset Metadata"]
auth = tweepy.AppAuthHandler(api_keys["api_key"], api_keys["api_secret_key"])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

politicians_tweets_df = pd.DataFrame()

twitters_df = pd.DataFrame(
    columns=[
        "id",
        "id_str",
        "screen_name",
        "twitter_name",
        "real_name",
        "confirmed_account_type",
        "bioguide",
        "office_holder",
        "party",
        "state",
        "district",
        "level",
        "woman",
        "birthday",
        "last_updated"
    ]
)


def add_politicians_tweets_twitter_names():
    global politicians_tweets_df

    politicians_tweets_df = pd.read_json("politicians-tweets/metadata/usa/current.json")

    politicians_tweets_df.rename(columns={"confirmed_politician": "confirmed_account_type"}, inplace=True)
    politicians_tweets_df["id"] = politicians_tweets_df["id"].astype(pd.Int64Dtype())

    # some long ids were getting messed up in id_str, use id
    politicians_tweets_df["id_str"] = politicians_tweets_df["id"].astype(str)

    politicians_tweets_df["confirmed_account_type"] = politicians_tweets_df["confirmed_account_type"].astype(pd.Int64Dtype())
    politicians_tweets_df["screen_name"] = politicians_tweets_df["screen_name"].str.lower()
    politicians_tweets_df["twitter_name"] = pd.NA

    all_screen_names = list(politicians_tweets_df["screen_name"])
    all_screen_names_cpy = all_screen_names.copy()
    users = []
    while all_screen_names_cpy:
        if len(all_screen_names_cpy) > 100:
            cur_screen_names = all_screen_names_cpy[:100]
            all_screen_names_cpy = all_screen_names_cpy[100:]
        else:
            cur_screen_names = all_screen_names_cpy
            all_screen_names_cpy.clear()

        if cur_screen_names:
            users += api.lookup_users(screen_names=cur_screen_names)

    for user in users:
        politicians_tweets_df.loc[politicians_tweets_df["screen_name"] == user.screen_name.lower(), "twitter_name"] = user.name

    # politicians_tweets_df.to_csv("politicians_tweets_df_w_twitter_names.csv")


def get_congress_legislators_screen_names():
    repo_path = Path(Path.cwd(), "congress-legislators")
    repo = Repo(repo_path)
    socials_path = Path("legislators-social-media.yaml")

    collected_screen_names = set()
    screen_names_bioguides = []

    # these commits have typos in the yaml
    typo_commits = {"9ce3d62de9a18aee359a7aef5ce9091dceb4f930",
                    "7c89d42862e0a2ac63355f5038ee8f9d2043e2f9",
                    "15148266b13b303a5ca5b8d43135205cd1f8752b",
                    "2f992891a175463d4a6fdd6f520d1bb779648009",
                    "64cd9d1438211cb9b7a11572b060d18903ed5e61",
                    "93631077380989c797261a3e4a4a7043dd696fea",
                    "8d1661e19122670ea796dc81e7b2babac19e64f5",
                    "0918156b43e9c985a8297f51156e68e849b4b717",
                    "a1810589f6d684ef197404cf91000d876fdbf770",
                    "d4a8a784f452cc16ca2b783f89346ed6fb2c92b4"}

    for commit in repo.iter_commits("master"):
        if commit.hexsha in typo_commits:
            continue

        commit_socials = yaml.load(repo.git.show("{}:{}".format(commit.hexsha, socials_path)), Loader=yaml.CLoader)

        for person in commit_socials:
            if "twitter" not in person["social"]:
                continue

            bioguide = person["id"]["bioguide"]
            screen_name = person["social"]["twitter"].lower()

            if screen_name in collected_screen_names:
                continue

            collected_screen_names.add(screen_name)
            screen_names_bioguides.append((screen_name, bioguide))

    # with open("screen_names_bioguides", "wb+") as f:
    #     pickle.dump(screen_names_bioguides, f)

    return screen_names_bioguides


# Retrieves metadata directly related to politicians' Twitter accounts from the "legislators-social-media.json"
# and the Twitter API. Puts metadata into dict mapping bioguides to Twitter data and writes it to a json.
def get_congress_legislators_twitter_data():
    global twitters_df

    screen_names_bioguides = get_congress_legislators_screen_names()

    # with open("screen_names_bioguides", "rb") as f:
    #     screen_names_bioguides = pickle.load(f)

    # get users 100 at a time to avoid rate limits
    screen_names_bioguides_cpy = screen_names_bioguides.copy()
    users = []
    while screen_names_bioguides_cpy:
        if len(screen_names_bioguides) > 100:
            screen_names = [user[0] for user in screen_names_bioguides_cpy[:100]]
            screen_names_bioguides_cpy = screen_names_bioguides_cpy[100:]
        else:
            screen_names = [user[0] for user in screen_names_bioguides_cpy]
            screen_names_bioguides_cpy.clear()
        
        if screen_names:
            users += api.lookup_users(screen_names=screen_names)

    for twitter in screen_names_bioguides:
        screen_name = twitter[0]
        bioguide = twitter[1]

        try:
            user = next(user for user in users if user.screen_name.lower() == screen_name)
            id_ = user.id
            id_str = str(user.id)
            twitter_name = user.name
        # user not found
        except StopIteration:
            id_ = pd.NA
            id_str = pd.NA
            twitter_name = pd.NA

        new_row = {
            "id": id_,
            "id_str": id_str,
            "screen_name": screen_name,
            "twitter_name": twitter_name,
            "confirmed_account_type": 1,
            "bioguide": bioguide
        }

        twitters_df = twitters_df.append(new_row, ignore_index=True)


    # twitters_df.to_json("congress_legislators_twitters.json")


# Adds non-Twitter metadata to dict mapping bioguides to metadata.
def add_congress_legislators_metadata():
    global twitters_df

    # with open("congress_legislators_twitters.json", "r") as f:
    #     twitters_df = pd.read_json(f)

    with open("congress-legislators/legislators-historical.yaml", "r") as f:
        congress_legislators = yaml.load(f, Loader=yaml.CLoader)
    with open("congress-legislators/legislators-current.yaml", "r") as f:
        congress_legislators += yaml.load(f, Loader=yaml.CLoader)

    party_codes = {
        "Democratic": 1,
        "Democrat": 1,
        "Republican": 2,
        "Green": 3,
        "Libertarian": 4,
        "Independent": 5
    }

    for person in congress_legislators:
        real_name = person["name"]["first"] + " " + person["name"]["last"]

        bioguide = person["id"]["bioguide"]

        if bioguide not in twitters_df["bioguide"].values:
            continue

        # look at their most recent term to find the state, party, and if they're currently serving
        most_recent_term = person["terms"][-1]

        term_end = most_recent_term["end"]
        if date.fromisoformat(term_end) < date.today():
            office_holder = 2
        else:
            office_holder = 1

        if "party" in most_recent_term:
            party = party_codes[most_recent_term["party"]]
        else:
            party = pd.NA

        state_code = most_recent_term["state"]
        state = str(us.states.lookup(state_code))

        if most_recent_term["type"] == "rep":
            district = int(most_recent_term["district"])
        else:
            district = 99

        # everyone in congress-legislators is a federal official
        level = 3
        
        woman = person["bio"]["gender"] == "F"

        birthday = person["bio"]["birthday"]

        metadata_cols = ["real_name", "bioguide", "office_holder", "party", "state", "district", "level", "woman", "birthday"]
        metadata = [real_name, bioguide, office_holder, party, state, district, level, woman, birthday]

        twitters_df.loc[twitters_df["bioguide"] == bioguide, metadata_cols] = metadata

    # twitters_df.to_json("congress_legislators_twitters_2.json")


def add_entries_to_politicians_tweets():
    global twitters_df
    global politicians_tweets_df

    # with open("congress_legislators_twitters_2.json", "r") as f:
    #     twitters_df = pd.read_json(f)

    twitters_df["id"] = twitters_df["id"].astype(pd.Int64Dtype())
    twitters_df["confirmed_account_type"] = twitters_df["confirmed_account_type"].astype(pd.Int64Dtype())

    politicians_tweets_df = politicians_tweets_df.merge(twitters_df,
                                                        on=["id", "id_str", "screen_name", "confirmed_account_type", "state", "twitter_name"],
                                                        how="outer")

    politicians_tweets_df["last_updated"] = date.isoformat(date.today())


if __name__ == "__main__":
    add_politicians_tweets_twitter_names()
    get_congress_legislators_twitter_data()
    add_congress_legislators_metadata()
    add_entries_to_politicians_tweets()

    politicians_tweets_df.to_json("current.json")
    politicians_tweets_df.to_csv("current.csv")
    politicians_tweets_df.to_excel("current.xlsx")
