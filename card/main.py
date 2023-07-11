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
            'profile_picture': {'type': 'keyword'},
            'role': {'type': 'text'},
            'qr_code': {'type': 'keyword'},
            'tribe': {'type': 'text'},
            'company_address': {'type': 'nested'},
            'phone_number': {'type': 'text'},
            'card_type' : {'type': 'text'},
            'is_active': {'type': 'boolean'},
            'is_deleted': {'type': 'boolean'},
            'created_date': {'type': 'datetime'},
            'updated_date': {'type': 'datetime'}
        }
    }
}

# Create the index
response = es.indices.create(index='xpert_card_index', body=index_settings)

# Check if the index creation was successful
if response['acknowledged']:
    print(f"The index xpert_card_index was created successfully.")
else:
    print(f"Failed to create the index 'xpert_card_index'.")
