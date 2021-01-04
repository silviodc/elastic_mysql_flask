from elasticsearch import Elasticsearch

class ElasticConnection:

    def __init__(self):
        self.es = Elasticsearch(["http://es01:9200","http://es02:9200","http://es03:9200"], maxsize=25)
        
    
    def createIndex(self):
        mapping = {
            "mappings": {
                "properties": {
                    "@timestamp":    { "type": "date" },  
                    "category":  { "type": "text"  }, 
                    "sales": { "type": "integer"  }, 
                    "revenue":   { "type": "float"  }     
                }
            }
        }
        self.es.indices.create(index='aggregation_ecommerce', body=mapping )


    def get_products_by_category(self, category):
        body = {
            "size": 100,
            "query": {
                "bool": {
                    "filter": [ 
                    {
                        "match_phrase": {
                        "category": category
                        }
                    },
                    {
                        "range": {
                        "order_date": {
                            "gte": "now-90d",
                            "lte": "now"
                        }
                        }
                    }
                    ]
                }
            } 
        }
        return self.es.search(index='kibana_sample_data_ecommerce', body=body)["hits"]["hits"]

    def get_aggregations(self):
        body = {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": "now-90d",
                                    "lte": "now"
                                }
                            }
                        }
                    ]
                }
            } 
        }
        return self.es.search(index='aggregation_ecommerce', body=body)["hits"]["hits"]

    def execute_elastic_query(self, query):
        return self.es.search(index='kibana_sample_data_ecommerce', body=query)
    
    def index_elastic(self, data):
        if(not self.es.indices.exists(index='aggregation_ecommerce')):
            self.createIndex()
        for item in data:
            self.es.index(index='aggregation_ecommerce',body=item)