# Q-Exchange - Search engine aggregator of various Q&A forums

A Search Engine Aggregator of various communities & forums like Stack Overflow, Math Overflow, Chemistry stack exchange & other sites like AskUbuntu and the programming forums on Reddit.
- It would crawl information from websites like Stack Overflow, Math Overflow & Chemistry stack exchange.
- Search for a term, get questions posted across different Stack Exchange communities.
- Results are ranked according to relevance & vote score of a question.
- Useful for users to visualise what various communities are talking about a trend.

## To Run
- Set up python3 venv and install dependencies in requirements.txt
```
python -m venv ./venv
pip install -r requirements.txt
```
- Test by running from stack directory
`scrapy crawl stack`
    - To render output to a json file
    `scrapy crawl stack -o items.json -t json`

### Pausing and Resuming Crawls
To enable persistence support you just need to define a job directory through the JOBDIR setting. This directory will be for storing all required data to keep the state of a single job (i.e. a spider run). It’s important to note that this directory must not be shared by different spiders, or even different jobs/runs of the same spider, as it’s meant to be used for storing the state of a single job.
    
#### How to use it
To start a spider with persistence support enabled, run it like this:

`scrapy crawl stack -s JOBDIR=crawls/stack-1`

Then, you can stop the spider safely at any time (by pressing Ctrl-C or sending a signal), and resume it later by issuing the same command:

`scrapy crawl stack -s JOBDIR=crawls/stack-1`