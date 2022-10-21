from flask import Flask, request, make_response
import json
import apihelpers as apih
import dbhelpers as dbh

app = Flask(__name__)
# from philosophers table in the database
# this procedures doesnt need any data so we go right to using the  logic of the procedure. 
@app.get('/api/philosopher')
def get_philosopher():
    results = dbh.run_statement('CALL get_philosopher()')

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500)  

@app.post('/api/philosopher')
def new_philosopher():
    is_valid = apih.check_endpoint_info(request.json, ['name', 'bio', 'date_of_birth', 'date_of_death', 'img_url'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL new_philosopher(?,?,?,?,?)', [request.json.get('name'), request.json.get('bio'), request.json.get('date_of_birth'), request.json.get('date_of_death'), request.json.get('img_url'), ])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500) 

# from quote table in the database

@app.get('/api/qoute')
def get_qoute_info():
    is_valid = apih.check_endpoint_info(request.args, ['id'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    
    results = dbh.run_statement('CALL get_qoute_info(?)', [request.args.get('id')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500)        

@app.post('/api/qoute')
def new_qoute():
    is_valid = apih.check_endpoint_info(request.json, ['philosopher_id', 'content'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)

    results = dbh.run_statement('CALL new_qoute(?,?)', [request.json.get('philosopher_id'), request.json.get('content')])

    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps('sorry error', default=str), 500)

app.run(debug=True)