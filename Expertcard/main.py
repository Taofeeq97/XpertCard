from elasticsearch import Elasticsearch

# Create an Elasticsearch client with authentication credentials
es = Elasticsearch(['http://localhost:9200'], http_auth=('elastic', '7PeMZZH7haepPZTxMBpP'))

# Specify the index name
index_name = 'expertcard_index'

# Check if the index exists
if es.indices.exists(index=index_name):
    print(f"The index '{index_name}' exists.")
else:
    print(f"The index '{index_name}' does not exist.")
