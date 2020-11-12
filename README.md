# Q-Exchange - Search engine aggregator of various Q&A forums

A Search Engine Aggregator of various communities & forums like Stack Overflow, various StackExchange sites & other sites like AskUbuntu and the programming forums on Reddit.
- It would crawl information from websites like Stack Overflow, Math Overflow & Chemistry stack exchange.
- Search for a term, get questions posted across different Stack Exchange communities.
- Results are ranked according to relevance & vote score of a question.
- Useful for users to visualise what various communities are talking about a trend.

## To Run
- Set up python (python3) venv and install dependencies in requirements.txt
```
python3 -m venv ./venv 
pip install -r requirements.txt
```

- Configure and run `main.py` under crawlers directory
    - You can also run crawlers/main.py if you're on Windows or if you're running it from an IDE.

- Or test by running from crawlers directory
`scrapy crawl stack`
    - To render output to a json file
    `scrapy crawl stack -o items.json -t json`
    -  `stack` crawls all stackexchange websites. It can be replaced by the following for scraping specific sites too:
        - `stackoverflow` (use as `scrapy crawl stackoverflow` and so on)
        - `unix`
        - `stack-other`
        - `reddit` (crawls r/webdev, r/programming)
         
#### Depth of crawl
- crawlers/stack/settings.py contains a variable `STACK_DEEP_CRAWL` to control the depth of crawling stack-exchange websites (By default only the excerpts to the questions are retrieved, the entire description can be extracted by setting the value to `True`).
- Setting it to `True` might result in a temporary IP ban if too many links are crawled.

#### Persistence support
_crawlers/temp/_ contains jsonlist output with spider-name and timestamps after a spider finishes crawling.

However you can start with persistence support that does not wait for the spiders to complete.
To start a spider with persistence support enabled, run it like this:

`scrapy crawl stack -s JOBDIR=crawls/stack-1`

Then, you can stop the spider safely at any time (by pressing Ctrl-C or sending a signal), and resume it later by issuing the same command:

`scrapy crawl stack -s JOBDIR=crawls/stack-1`

### Searching

Run ```query.py```
    
    $ chmod +x query.py
    $ ./query.py

### For Solr

![alt text](screenshots/add_docs_from_terminal.png?raw=true)
![alt text](screenshots/add_docs_from_ui.png?raw=true)
![alt text](screenshots/query_index.png?raw=true)
