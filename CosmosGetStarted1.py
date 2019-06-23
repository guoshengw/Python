from pydocumentdb import document_client

uri = ''
key = 'TwTqcL2eQb21pelkAZacrfoqTvtBSvivaZgz3sH7AIze3ivpqxpNOJsM0mfdTb3p8cIhnkiObdqzwrECJLj2bQ=='

client = document_client.DocumentClient(uri, {'masterKey': key})

db_id = 'db1'
db_query = "select * from r where r.id = '{0}'".format(db_id)
db = list(client.QueryDatabases(db_query))[0]
db_link = db['_self']

coll_id = 'employee'
coll_query = "select * from r where r.id = '{0}'".format(coll_id)
coll = list(client.QueryCollections(db_link, coll_query))[0]
coll_link = coll['_self']

docs = client.ReadDocuments(coll_link)
print(list(docs))

