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
