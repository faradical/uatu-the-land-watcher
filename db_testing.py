import pymongo

# Local DB Connection
local_client = pymongo.MongoClient()
local_DB = local_client.real_estate

# Remote DB Connection
remote_client = pymongo.MongoClient("mongodb://uatu:#watch!@uatu-cluster-shard-00-00.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-01.c4ylx.mongodb.net:27017,uatu-cluster-shard-00-02.c4ylx.mongodb.net:27017/real_estate?ssl=true&replicaSet=atlas-10fsbj-shard-0&authSource=admin&retryWrites=true&w=majority")
remote_DB = remote_client.real_estate

for l_col in local_DB.collection_names():
    print(l_col)
    remote_DB[l_col].insert_many(local_DB[l_col].find())