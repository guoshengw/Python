import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors
import datetime

import samples.Shared.config as cfg

config = {
    'ENDPOINT': '',
    'PRIMARYKEY': 'TwTqcL2eQb21pelkAZacrfoqTvtBSvivaZgz3sH7AIze3ivpqxpNOJsM0mfdTb3p8cIhnkiObdqzwrECJLj2bQ==',
    'DATABASE': 'db1',
    'CONTAINER': 'employee'
}


database_link = 'dbs/db1'
collection_link = database_link + '/colls/employee'

client = cosmos_client.CosmosClient(url_connection=config['ENDPOINT'], auth={
                                    'masterKey': config['PRIMARYKEY']})

documentlist = list(client.ReadItems(collection_link, {'maxItemCount':10}))
        
print('Found {0} documents'.format(documentlist.__len__()))
        
for doc in documentlist:
    print('Document Id: {0}'.format(doc.get('id')))