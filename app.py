from flask import Flask, jsonify
import primes  # Our own Python file to calculate Primes
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
        {'massage ': 'Choose your algorithm', 'method-1': 'Naive Method', 'method-2': 'Sieve of Eratosthenes'})


# Route for method2 i.e. Naive method
@app.route('/method1/<int:start>/<int:end>', methods=['POST'])
def naive_method(start: int, end: int):
    if start > end:
        start, end = end, start
    method = 'Naive Method'
    t0 = time.time()
    res = primes.PrimeCalculator.method1(start, end)
    t1 = time.time()
    insert_to_db(method, t0, res, t1, start, end)
    return jsonify(massege=str(res)), 201


# Route for method2 i.e. Sieve of Eratosthenes method
@app.route('/method2/<int:start>/<int:end>', methods=['POST'])
def efficient_method(start: int, end: int):
    if start > end:
        start, end = end, start
    method = 'Sieve of Eratosthenes method'
    t0 = time.time()
    res = primes.PrimeCalculator.method2(start, end)
    t1 = time.time()
    insert_to_db(method, t0, res, t1, start, end)
    return jsonify(str(res)), 201


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


@app.route('/clear', methods=['DELETE'])
def clear():
    try:
        db.session.query(Records).delete()
        db.session.commit()
        return jsonify('Database cleared successfully!')
    except:
        db.session.rollback()
        return jsonify('Something went wrong!')


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
