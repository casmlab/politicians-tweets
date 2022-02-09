# Twitter U.S.and India Politicians dataset

The Twitter U.S. and Indian Politicians dataset is provided for use by University of Michigan faculty, students, and their collaborators. The data is stored on Turbo at `/nfs/turbo/politweets` and is structured like the [Twitter Decahose for U-M](https://github.com/CSCAR/twitter-decahose).

# Requesting Access

## UM faculty, staff, and students
[Go here to apply for access](https://midas.umich.edu/twitter-politicians-data-set/). MIDAS will review your application, send you a copy of the memorandum of understanding between you and MIDAS that explains the date use terms.

The process for gaining access to the dataset is similar to the [Twitter Decahose Data](https://midas.umich.edu/twitter-decahose-data/). 

## Interested folks at other institutions

Email [politics-database@umich.edu](mailto:politics-database@umich.edu) with some information about your project, your timeline, and the specific data you are interested in using. We are actively developing datasets and access procedures for researchers at other institutions, but we will likely not have formal systems in place until late summer 2022. 

# Using the Data

[CSCAR's tutorials for the Twitter Decahose](https://github.com/caocscar/twitter-decahose-pyspark) are a great place to start. This data is similarly structured though it includes a different set of users.

# What's in the Data

We collect tweets posted by politicians in the U.S. and India and save the JSON provided by the Twitter API. Lists of politicians are generated by [NivaDuck](https://dl.acm.org/doi/epdf/10.1145/3400806.3400830), software developed at Microsoft Research - India for automatically identifying accounts that belong to politicians.  

As of **April 21, 2021**, the data includes:

* USA
	- Number of accounts: 9608 (8994 with state metadata; all current MCs with complete metadata)
* India
	- Number of political Twitter handles: 33074 (27300 with party metadata, 16027 with state metadata)

## Data Collection Process

Two scripts run daily, one each for India and the U.S., to pull new tweets posted everyday by each politician in the respective lists. For India, the list of accounts includes journalists, media outlets, celebrities, and influencers. The same set for the U.S. is still being compiled and the accounts will be updated in the future.

You can view the scripts for collection in the `scripts` folder.

## Data Structure

Data is stored in two folders, one each for India (`/nfs/turbo/politweets/india`) and the U.S. (`/nfs/turbo/politweets/usa`). Inside each, there are three folders: `~/tweets_par/`, `~/logs/`, `~/errors/`. The `~/tweets_par/` directory contains one sub-directory for each account being tracked, named for the user's public screen_name. For example, `/nfs/turbo/politweets/usa/tweets_par/realDonaldTrump/` contains tweets from former President Donald Trump. Inside every user's (politician's) directory, there are multiple compressed JSON files.

## Twitter User Metadata 

We are manually checking all accounts NivaDuck identified and will provide periodic metadata updates.

* [Current list of U.S. Accounts](metadata/usa/current.json)
* [Current list of India Accounts](metdata/india/current.json)

### Metadata Fields

See the [codebook](https://github.com/casmlab/politicians-tweets/blob/main/metadata/usa/usa-metadata-codebook.csv) for a list of metadata fields, descriptions, variable types, valid values, etc.

Here's an example of the minimum metadata:

|    | id         | id_str     | screen_name     | confirmed_account_type | state      | twitter_name         | real_name     | bioguide | office_holder | party | district | level | woman | birthday | last_updated |
|----|------------|------------|-----------------|------------------------|------------|----------------------|---------------|----------|---------------|-------|----------|-------|-------|----------|--------------|
| 0  | 986781648  | 986781648  | jeffsessions    | 1                      | Alabama    | Jeff Sessions        |               |          |               |       |          |       |       |          | 4/20/21      |
| 29 | 1155335864 | 1155335864 | repdonaldpayne  | 1                      | New Jersey | Rep. Donald Payne Jr | Donald Payne  | P000604  | 1             | 1     | 10       | 3     | FALSE | 12/17/58 | 4/20/21      |
| 74 | 2970462034 | 2970462034 | repkathleenrice | 1                      | New York   | Kathleen Rice        | Kathleen Rice | R000602  | 1             | 1     | 4        | 3     | TRUE  | 2/15/65  | 4/20/21      |

Archived metadata files are available in the `metadata` folder as well.

# Contributors

[Anmol Panda](mailto:anmolp@umich.edu) and [Armand Burks](arburks@umich.edu) wrote the scripts to collect and archive Tweets using the Twitter Public API (via [tweepy](https://www.tweepy.org/)). [Libby Hemphill](mailto:libbyh@umich.edu) generated this documentation and manages the team who collect and update data and metadata. [Evan Parres](mailto:evparres@umich.edu) handles metadata updates, and [Najmin Ahmed](mailto:nnahmed@umich.edu) manually verified many state labels for 2020 election candidates.

Funding for the staff and infrastructure were provided by

* [Michigan Institute for Data Science](https://midas.umich.edu/)
* [Advanced Research Computing - Technology Services](https://arc.umich.edu/)
* [Assoc. Professor Libby Hemphill](https://www.si.umich.edu/people/libby-hemphill)

We are grateful to [Ballot Ready](https://www.ballotready.org/) for providing data on political candidates in the U.S.

# How to Cite/Acknowledge the Data

## Acknowledge the Dataset Providers

If you use the data, please cite the NivaDuck paper (bibtex below) and include the following acknowledgment:

> The Twitter U.S.and India Politicians dataset is supported by [the Michigan Institute for Data Science](https://midas.umich.edu/), [Advanced Research Computing - Technology Services](https://arc.umich.edu/), and [Consulting for Statistics, Computing & Analytics Research](https://cscar.research.umich.edu/), and [Dr. Libby Hemphill's](https://www.si.umich.edu/people/libby-hemphill) research group in the [School of Information](https://www.si.umich.edu/).

## Cite the NivaDuck paper

### BibTeX

```
@inproceedings{
10.1145/3400806.3400830,
author = {Panda, Anmol and Gonawela, A’ndre and Acharyya, Sreangsu and Mishra, Dibyendu and Mohapatra, Mugdha and Chandrasekaran, Ramgopal and Pal, Joyojeet},
title = {NivaDuck - A Scalable Pipeline to Build a Database of Political Twitter Handles for India and the United States},
year = {2020},
isbn = {9781450376884},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3400806.3400830},
doi = {10.1145/3400806.3400830},
abstract = {We present a scalable methodology to identify Twitter handles of politicians in a given region and test our framework in the context of Indian and US politics. The main contribution of our work is the list of the curated Twitter handles of 18500 Indian and 8000 US politicians. Our work leveraged machine learning-based classification and human verification to build a data set of Indian politicians on Twitter. We built NivaDuck, a highly precise, two-staged classification pipeline that leverages Twitter description text and tweet content to identify politicians. For India, we tested NivaDuck’s recall using Twitter handles of the members of the Indian parliament while for the US we used state and local level politicians in California state and San Diego county respectively. We found that while NivaDuck has lower recall scores, it produces large, diverse sets of politicians with precision exceeding 90 percent for the US dataset. We discuss the need for an ML-based, scalable method to compile such a dataset and its myriad use cases for the research community and its wide-ranging utilities for research in political communication on social media. },
booktitle = {International Conference on Social Media and Society},
pages = {200–209},
numpages = {10},
keywords = {united states, india, archive, twitter, politics},
location = {Toronto, ON, Canada},
series = {SMSociety'20}
}
```

### APA 7th


>Panda, A., Gonawela, A., Acharyya, S., Mishra, D., Mohapatra, M., Chandrasekaran, R., & Pal, J. (2020). NivaDuck - A Scalable Pipeline to Build a Database of Political Twitter Handles for India and the United States. International Conference on Social Media and Society, 200–209. https://doi.org/10.1145/3400806.3400830


# Reporting Issues and Getting Help

Use [issues](https://github.com/casmlab/politicians-tweets/issues) to report bugs and request changes to the collection process or metadata. We will not be providing hands-on help with the data, but we will try to answer questions if they come up. You can direct questions to [politics-database@umich.edu](mailto:politics-database@umich.edu).
