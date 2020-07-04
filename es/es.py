import json

out = open('songs_to_es.json', 'w',encoding='utf-8')

with open('../scrape/songs.json',encoding='utf-8') as json_in:
    docs = json.loads(json_in.read())
    i = 1
    for doc in docs:
        doc['visits'] = int(doc['visits'].replace(',',''))
        out.write('%s\n' % json.dumps({'index': {'_index': 'songs', '_id': str(i)}}))
        out.write('%s\n' % json.dumps(doc, indent=0,ensure_ascii=False).replace('\n', ''))
        i+=1
