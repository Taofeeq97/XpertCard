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
            'profile_picture': {'type': 'text'},  # Update with the appropriate field type
            'role': {'type': 'text'},  # Update with the appropriate field type
            'qr_code': {'type': 'text'},  # Update with the appropriate field type
            'tribe': {'type': 'text'},  # Update with the appropriate field type
            'company_address': {'type': 'text'},  # Update with the appropriate field type
            'city': {'type': 'text'},  # Update with the appropriate field type
            'country': {'type': 'text'},  # Update with the appropriate field type
            'phone_number': {'type': 'text'},  # Update with the appropriate field type
        }
    }
}

# Create the index
response = es.indices.create(index='expertcard', body=index_settings)

# Check if the index creation was successful
if response['acknowledged']:
    print(f"The index 'expertcard' was created successfully.")
else:
    print(f"Failed to create the index '{index_name}'.")
