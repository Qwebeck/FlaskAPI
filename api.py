from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'
# set to true if i will need to handle adition, deletion of object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


    
class FileProcessingThread(threading.Thread):
    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data
        
    def run(self):
        

        for test in self.data['data']: 
            new_test = Test(test_timestamp=int(test['timestamp']), test_value = int(test['value']))
            db.session.add(new_test)
        print('Data is added')
        db.session.commit()

class Test(db.Model):
    __tablename__ = "Tests"
    id = db.Column(db.Integer ,primary_key = True)
    test_value = db.Column(db.Integer)
    # Data is store as timestamp, because test in example datafile were given as timestamps, so they should be used as timestamps.
    # In order to see test data in human-readble format -- specify pass this option as an argument to client
    test_timestamp = db.Column(db.Integer)

# First method will call for existence of Test instance. Than in case if there are no such tables - vreate a new one,
# otherwise nothing will be created
db.create_all()


@app.route('/getAll',methods=['GET'])
def get_all():
    tests = Test.query.all()
    output = []
    for test in tests:
        test_dict = {
            'timestamp':test.test_timestamp,
            'value':test.test_value
        }
        output.append(test_dict)
    
    res = {'message':'ok','data':output}
    if len(output) == 0:
        res = {'message':'Table is empty'} 
    
    return jsonify(res)

@app.route('/getOne/:<test_id>',methods=['GET'])
def get_one(test_id):
    test = Test.query.filter_by(id=test_id).first()
    if not test:
        return jsonify({'message':'No tests found !'})
    output = {
            'message':'ok',
            'data':[
            {'timestamp':test.test_timestamp,
            'value':test.test_value
    }]}
    return jsonify(output)


@app.route('/addOne',methods=['POST'])
def add_one():
    data = request.get_json()
    # Check if file of multiple json elements was send to endpoint
    if 'data' in data.keys():
       
        thread = FileProcessingThread(data)

        thread.start()
    return jsonify({'message':'Success !'})

@app.route('/deleteOne/:<test_id>',methods=['DELETE'])
def delete_one(test_id):
    test = Test.query.filter_by(id=test_id).first()
    if not test:
        return jsonify({'message':'No tests found !'})
    
    db.session.delete(test)
    db.session.commit()
    return jsonify({'message':'The test has been deleted !'})

@app.route('/drop',methods=['DELETE'])
def drop():
    db.drop_all()
    return jsonify({'message':'Table has been deleted !'})

if __name__ == '__main__':
   
    app.run(debug=True)