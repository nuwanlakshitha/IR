from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from sinling import word_splitter, SinhalaTokenizer

app = Flask(__name__)
es = Elasticsearch()
tokenizer = SinhalaTokenizer()

artist_list = ['කී', 'ගායනා කරන', 'ගයන', 'ගායනා','‌ගේ', 'හඩින්', 'කියනා', 'කිව්ව', 'ගායනය', 'ගායනා කළ', 'ගැයූ']
genre_list = ['පැරණි', 'පොප්ස්','පොප්','පරණ','ක්ලැසික්','ක්ලැසිකල්','ඉල්ලීම','චිත්‍රපට','නව', 'යුගල']
lyrics_list = ['ලියා', 'ලියූ', 'ලිව්ව', 'රචනා',  'ලියා ඇති', 'රචිත', 'ලියන ලද','ලියන', 'හදපු', 'ගේයපද', 'රචනය', 'හැදූ', 'ලියන', 'ලියන්න', 'ලියපු']
music_list = ['සංගීතය', 'සංගීතවත්','අධ්‍යක්ෂණය', 'සංගීත', 'නිර්මාණය']
best_list = ['සුපිරි', 'නියම', 'පට්ට', 'හොඳ', 'හොඳම', 'වැඩිපුර', 'වැඩිපුරම', 'සුප්‍රකට', 'ජනප්‍රිය', 'ජනප්‍රියම', 'ප්‍රකට', 'ප්‍රසිද්ධ']

@app.route('/', methods=['GET', 'POST'])
def index():
    q = request.args.get('q')
    if (q is not None):
        q = q.strip()
        sort_results = 25
        best_enabled = False
        search_fields = set()
        word_list = tokenizer.tokenize(q)
        for word in word_list:
            if(word in artist_list):
                search_fields.add('artist^3')
                q=q.replace(word, '')
            elif(word in genre_list):
                search_fields.add('genre^3')
                q=q.replace(word, '')
            elif(word in lyrics_list):
                search_fields.add('lyrics_by^3')
                q=q.replace(word, '')
            elif(word in music_list):
                search_fields.add('music^3')
                q=q.replace(word, '')
            elif(word.isdigit()):
                sort_results = int(word)
                q=q.replace(word, '')
            elif(word in best_list):
                best_enabled = True
                q=q.replace(word, '')
                        
        if(len(search_fields)==0):
            search_fields.add('lyrics^5')
            search_fields.add('artist^4')
            search_fields.add('lyrics_by^2')
            search_fields.add('music^2')

        if(best_enabled):
            resp = es.search(index='songs', doc_type='_doc', body={
                "query": {
                    "multi_match": {
                        "query": q.replace('  ', ''),
                        "fields": list(search_fields)
                    }}, 
                "size": sort_results, 
                "sort" : [{
                    "visits" : { "order" : "desc" }
                }]
            })
        else:
            resp = es.search(index='songs', doc_type='_doc', body={
                "query": {
                    "multi_match": {
                        "query": q.replace('  ', ''),
                        "fields": list(search_fields)
                    }}, 
                "size": sort_results
            })
        return render_template('index.html', q=q, response=resp)
    return render_template('index.html', response='')


if(__name__=='__main__'):
    app.run(host='localhost', port=9874)