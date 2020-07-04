## Folder Structure
corpus - generated files after execution
es - source code for generating songs_to_es.json
scrape - code for scraping from sinhalasongbook.com
templates - user interfaces

## Steps
1. Run following command within scrape folder
    scrapy crawl songs
2. Run following command within scrape folder
    python es.py
3. Run each command in setings.json file on kibana server
4. Run app.py file and search