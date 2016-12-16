#Create a cluster
curl -X POST -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters" -d ""

#Cluster ID = sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97

#Check cluster availability
curl -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97"

#Upload configuration
curl -X POST -H "Content-Type: application/zip" -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97/config/solrconfig" --data-binary @solrconfig.zip

#Associate collection
curl -X POST -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97/solr/admin/collections" -d "action=CREATE&name=intent_collection&collection.configName=solrconfig"

#Insert Documents
curl -X POST -H "Content-Type: application/json" -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97/solr/intent_collection/update" --data-binary @/home/parth/Documents/IBM-Watson/intent.json

#Train ranker
curl -X POST -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" -F training_data=@/home/parth/Documents/IBM-Watson/intent.csv -F training_metadata="{\"name\":\"My ranker\"}" "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/rankers"

#Ranker ID 76643bx23-rank-1409

#Get ranker info
curl -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu"  "https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/rankers/76643bx23-rank-1409"

python ./train.py -u "196f0283-d44c-4442-9346-66b3e3c43315":"lrInT1KDztFu" -i /home/parth/Documents/IBM-Watson/intent.csv -c sc4dd74cd3_a04b_4440_8b15_1cf3bdca5e97 -x intent_collection -n "My ranker"
