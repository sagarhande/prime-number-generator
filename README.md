# Prime-number-generator
This repository contain a RESTful Flask API for generating prime numbers in range.
I used sqlalchemy as ORM for this API, along with SQLite DB.

## Prerequisites

To run this API you will need _Python 3.8_ along with below liabraries installed<br/>
* Flask==1.1.2<br />
* flask-marshmallow==0.14.0 <br />
* Flask-SQLAlchemy==2.5.1<br />
* Jinja2==2.11.2<br />
* marshmallow==3.13.0<br />
* SQLAlchemy==1.4.22<br />

## Usage

**Before using API you need to create DB  : `flask db_create`**<br /><br />
*Step-1)* Run app.py : `Python app.py`<br />
*Step-2)* Use following endpoints for requests .It will return a JSON . <br />
 * Home Route (GET) : `http://127.0.0.1:5000/`<br />
 * Method-1 (_Naive_) (POST) : `http://127.0.0.1:5000/cal/1/start/end`<br />
 * Method-2 (_Sieve of Eratosthenes_) (POST) : `http://127.0.0.1:5000/cal/2/start/end`<br />
  *Note: Please provide positive integers **start** and **end***<br/>
 * Get all records (GET) : `http://127.0.0.1:5000/records`<br />
 * Clear records from database (DELETE) : `http://127.0.0.1:5000/clear`<br />
  *Please clear DB once you done using*
## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

----------------------
