from flask import Flask, jsonify
import primes  # Python file to calculate Primes
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Set up configuration for DB
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Hist.db')

# Initialize database
db = SQLAlchemy(app)
# Creating instance for Serialization(Converting object into textual representation)
ma = Marshmallow(app)


# CLI command to Create Database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


# CLI command to Drop database
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.route('/')
def home():
    return jsonify(
        {'0': 'Choose your algorithm', '1': 'Naive Method', '2': 'Sieve of Eratosthenes'})


# Route to calculate primes
# 1. Naive
# 2. Sieve of Eratosthenes
@app.route('/cal/<int:method>/<string:start>/<string:end>', methods=['POST'])
def calculate(method: int, start: str, end: str):
    try:
        start, end = int(start), int(end)
        if start < 0 or end < 0 or method not in [1, 2]:
            return jsonify('Please provide correct parameters!'), 401
        if start > end:
            start, end = end, start
        t0 = time.time()
        if method == 1:
            method = 'Naive'
            res = primes.PrimeCalculator.method1(start, end)
        else:
            method = 'Sieve of Eratosthenes'
            res = primes.PrimeCalculator.method2(start, end)
        t1 = time.time()
        insert_to_db(method, t0, res, t1, start, end)
        return jsonify(massege=str(res)), 201
    except:
        return jsonify('Please create DB first !'), 404


# Function to insert record into table
def insert_to_db(method, t0, res, t1, start, end):
    new_record = Records(timestamp=str(time.strftime("%D-%H:%M:%S", time.localtime())),
                         start_no=start,
                         end_no=end,
                         time_elapsed=str((t1 * 1000) - (t0 * 1000)),
                         method_chosen=method,
                         result=str(res))

    db.session.add(new_record)
    db.session.commit()


# route to show all records
@app.route('/records', methods=['GET'])
def display_records():
    temp = Records.query.all()
    all_records = records_schema.dump(temp)
    return jsonify(all_records)


# route to clear all records from table Records
@app.route('/clear', methods=['DELETE'])
def clear():
    try:
        db.session.query(Records).delete()
        db.session.commit()
        return jsonify('Database cleared successfully!')
    except:
        db.session.rollback()
        return jsonify('Something went wrong! Please check if database created !'), 404


# Database Models
# creating Records table
class Records(db.Model):
    __tablename__ = 'Records'
    record_no = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String)
    start_no = Column(Integer)
    end_no = Column(Integer)
    time_elapsed = Column(String)
    method_chosen = Column(String)
    result = Column(String)


# Creating indicator for Marshmallow
# To refer fields we looking for serialization
class RecordsSchema(ma.Schema):
    class Meta:
        fields = ('record_no', 'timestamp', 'start_no', 'end_no', 'time_elapsed', 'method_chosen', 'result')


# to show all records created instance
records_schema = RecordsSchema(many=True)

if __name__ == '__main__':
    app.run(debug=True)
