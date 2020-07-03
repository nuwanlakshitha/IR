# import json

# with open('../scrape/songs.json', 'r', encoding='utf8') as fd:
#     jsonFile = json.load(fd)

# songs_to_es = []
# i = 1
# for song in jsonFile:
#     # songs_to_es = []
#     songs_to_es.append({
#         'index': {
#             '_index': 'songs',
#             '_id': str(i)
#             }
#     })
#     song['visits'] = int(song['visits'].replace(',', ''))
#     songs_to_es.append(song)
#     i += 1

# with open('songs_to_es.json', 'w', encoding='utf8') as out:
#     json.dump(songs_to_es, out, indent=0, ensure_ascii=False,)


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
