import os
import json
import time
from os import environ
from celery import Celery, states
from celery.result import AsyncResult
from DataStorage import ElasticConnection
import logging

celery = Celery('flask-app', 
        backend=f"rpc://{environ.get('RABBITMQ_USERNAME')}:{environ.get('RABBITMQ_PASSWORD')}@{environ.get('RABBITMQ_URL')}/",
        broker=f"amqp://{environ.get('RABBITMQ_USERNAME')}:{environ.get('RABBITMQ_PASSWORD')}@{environ.get('RABBITMQ_URL')}/")

logger = logging.getLogger()

def get_job_by_id(job_id):
    return AsyncResult(job_id, app=celery)

@celery.task(bind=True)
def process_aggregation(self, date):
    logger.info(f"Processing my cool payload {date}")
    time.sleep(20)
    elastic = ElasticConnection()
    with open(os.path.join('statistics','sales_by_category.json'), 'r') as file:
        query = json.load(file)
        result = elastic.execute_elastic_query(query)
        result = transform_elastic_payload(result)
        elastic.index_elastic(result)
        logger.info(f"Process done!")

def transform_elastic_payload(payload):
    result = []
    for item in payload["aggregations"]["group_date"]["buckets"]:
        date = item["key_as_string"]
        for group in item["group_category"]["buckets"]:
            category = {"@timestamp":date, "category": group["key"],
             "sales": group["doc_count"], "revenue": group["3h_sum"]["value"]}
            result.append(category)
    return result
    