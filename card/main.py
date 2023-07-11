from elasticsearch import Elasticsearch

client = Elasticsearch(
    hosts=['http://localhost:9200'],
    http_auth=('elastic', '7PeMZZH7haepPZTxMBpP')
)

# Get a list of project indexes
response = client.indices.get_alias(index="myproject_*")
print('heyyy')
indexes = list(response.keys())
print(indexes)
# Delete each index
for index in indexes:
    response = client.indices.delete(index=index, ignore=[400, 404])
    if response['acknowledged']:
        print(f"The index {index} was deleted successfully.")
    else:
        print(f"Failed to delete the index {index}.")
