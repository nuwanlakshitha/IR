## Folder Structure
1. corpus - generated files after execution
2. es - source code for generating songs_to_es.json
3. scrape - code for scraping from sinhalasongbook.com
4. templates - user interfaces

## Steps
1. Run 'scrapy crawl songs' command within scrape folder
    
2. Run 'python es.py' command within scrape folder
    
3. Run each command in setings.json file on kibana server

4. Run app.py file and search