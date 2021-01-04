import celery_app
from datetime import datetime
from flask import Flask, abort, jsonify, url_for, request, make_response
from flask_cors import CORS, cross_origin
from DataStorage import ElasticConnection

app = Flask(__name__)
CORS(app)
elastic = ElasticConnection()

@app.route('/')
def hello():
    return 'Hello World!'

@app.route("/products", methods = ['GET'])
def products():
    category = request.args.get('category')
    return  make_response(jsonify(elastic.get_products_by_category(category)))

@app.route("/aggregations", methods = ['GET'])
def aggregations():
    return  make_response(jsonify(elastic.get_aggregations()))

@app.route("/add-job", methods = ['POST'])
def add_job():
    aggregation_task_id = celery_app.process_aggregation.delay(datetime.now())
    return make_response(jsonify({'task_id': aggregation_task_id.task_id, 'state': aggregation_task_id.state }))

@app.route('/progress/<task_id>', methods = ['GET'])
def progress(task_id):    
    task = celery_app.get_job_by_id(task_id)
    if task.state == 'PENDING':
        response = {
            'queue_state': task.state,
            'status': 'Process is ongoing...',
            'status_update': url_for('progress', task_id=task.id)
        }
    elif task.state == 'SUCCESS':
        response = {
            'queue_state': task.state,
            'status': 'Process is finished!',
            'status_update': url_for('progress', task_id=task.id)
        }
    else:
         response = {
            'queue_state': task.state,
            'status': 'Check the errors on your logs!',
            'status_update': url_for('progress', task_id=task.id)
        }
    return make_response(jsonify(response))