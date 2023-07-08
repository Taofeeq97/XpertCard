from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', '7PeMZZH7haepPZTxMBpP'))

# Define the index settings and mappings
index_settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings': {
        'properties': {
            'first_name': {'type': 'text'},
            'last_name': {'type': 'text'},
            'email': {'type': 'text'},
            'profile_picture': {'type': 'keyword'},  # Change the type to 'keyword'
            'role': {'type': 'text'},
            'qr_code': {'type': 'keyword'},  # Change the type to 'keyword'
            'tribe': {'type': 'text'},
            'company_address': {'type': 'nested'},  # Change the type to 'nested'
            'city': {'type': 'text'},
            'country': {'type': 'text'},
            'phone_number': {'type': 'text'},
        }
    }
}

# Create the index
response = es.indices.create(index='xpertcards_index', body=index_settings)

# Check if the index creation was successful
if response['acknowledged']:
    print(f"The index 'xpertcards_index' was created successfully.")
else:
    print(f"Failed to create the index 'xpertcards_index'.")
