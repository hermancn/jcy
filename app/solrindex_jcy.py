from pymongo import MongoClient
from mysolr import Solr
from bson.objectid import ObjectId
from bson.json_util import dumps


HOST = '127.0.0.1'
PORT = 27017
SERVER = 'http://localhost:8983/solr/monitor'


def index():
    client = MongoClient(host=HOST, port=PORT)
    db = client['crawl']
    coll = db['web']

    server = Solr(SERVER)
    max_indexed_id = get_max_indexed_id(server)
    if not max_indexed_id:
        max_indexed_id = ObjectId('000000000000')
    else:
        max_indexed_id = ObjectId(max_indexed_id)

    sites = get_host_name()

    step = 100
    count = 0

    jdocs = []
    for row in coll.find({'_id': {'$gt': max_indexed_id}}).sort([('_id',1)]):
        jdoc = {}
        jdoc['id'] = str(row['_id'])
        if len(jdocs) == 0:
            start = row['_id']
        jdoc['url'] = row['curi:url']

        jdoc['site'] = sites[get_url_domain(row['curi:url'])]

        jdoc['ip'] = row['curi:ip']
        if 'curi:processed_at' in row:
            jdoc['processed_at'] = row['curi:processed_at']
        if 'content_type' in row:
            jdoc['content_type'] = row['content_type']
        if 'content_length' in row:
            jdoc['content_length'] = row['content_length']
        if 'class_key' in row:
            jdoc['class_key'] = row['class_key']
        if 'host' in row:
            jdoc['host'] = row['host']
        if 'curi:request' in row:
            jdoc['request'] = row['curi:request']
        if 'content:headers' in row:
            jdoc['headers'] = row['content:headers']
        if 'text' in row:
            jdoc['text'] = row['text']
        if 'title' in row:
            jdoc['title'] = row['title']
        if 'parse:keywords' in row:
            jdoc['keywords'] = row['parse:keywords']
        if 'parse:content-encoding' in row:
            jdoc['content_encoding'] = row['parse:content-encoding']
        if 'content:raw_data' in row:
            jdoc['raw_data'] = row['content:raw_data']

        jdocs.append(jdoc)
        count = count + 1

        if len(jdocs) >= step:
            end = row['_id']
            xx = server.update(jdocs)
            server.commit()
            print xx
            jdocs = []
            print('commit %d documents. %s to %s'  % (count, start, end))

    if len(jdocs) > 0:
        server.update(jdocs)
        server.commit()


def get_max_indexed_id(solr):
    response = solr.search(q='*:*', sort='id desc', rows=1, start=0)
    if response.documents and len(response.documents) > 0:
        doc = response.documents[0]['id']
        return doc
    return None


def del_all_index(server):
    server = Solr(server)
    server.delete_by_query('*:*')
    server.commit()


def get_max_id(cursor):
    max = cursor.find().sort({"_id":-1}).limit(1)
    # min = cursor.find().sort({"_id":-1}).limit(-1)
    return max


def get_host_name():
    site_dict = {}
    import codecs
    with codecs.open('site_match.text', 'rb', encoding='utf-8') as f:
        for line in f.readlines():
            temp = line.split()
            if len(temp) == 2:
                site_dict[temp[1]] = temp[0]

    return site_dict

def get_url_domain(url):
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain


if __name__ == '__main__':
    del_all_index(SERVER)
    # print(get_max_indexed_id(Solr(SERVER)))

    index()
    # import uniout
    # r = get_host_name()
    # print r
